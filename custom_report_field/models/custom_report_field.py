import logging

from odoo import api, exceptions, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval, test_python_expr

from odoo.addons.report_monetary_helpers.utils.format_number import format_number

_logger = logging.getLogger(__name__)


class CustomReportField(models.Model):
    _name = "custom.report.field"
    _description = "Custom report field"
    _order = "sequence"

    ir_actions_report_id = fields.Many2one(
        "ir.actions.report",
        string="Report",
    )
    sequence = fields.Integer(
        string="Sequence",
    )
    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
    )
    technical_name = fields.Char(
        string="Technical Name",
        help="Name for using in templates",
        required=True,
    )
    default_value = fields.Text(
        string="Default value",
        help="This field is a Python expression that can use the same variables as"
        " the 'code' field in the server action, except moment that the computation"
        " result should be assigned into the 'value' variable."
        "Also available method 'format_number' for formatting numbers representation in report. Returns number as string.",
    )
    description = fields.Char(
        string="Description",
        help="Description for this field to be showed in fields list in verify wizard.",
        translate=True,
        default="",
    )
    required = fields.Boolean(
        string="Required",
        help="If checked, it will not be possible to generate a document without a default value.",
        default=False,
    )
    visible = fields.Boolean(
        string="Visible",
        help="To show this field in fields list in verify wizard\n"
        "User can change showed field's values in wizard.",
        default=True,
    )

    @api.constrains("default_value")
    def _check_default_value(self):
        for rec in self.filtered("default_value"):
            msg = test_python_expr(expr=rec.default_value.strip(), mode="exec")
            if msg:
                raise ValidationError(msg)

    def _get_eval_context(self, action=None):
        eval_context = self.env["ir.actions.actions"]._get_eval_context(action=action)
        eval_context.update(self.env.context)
        model_name = action.model_id.sudo().model
        model = self.env[model_name]
        record = None
        records = None
        _logger.error(
            f"\n\n\nself._context:\n{self._context}\nself.env.context:\n{self.env.context}\n\n\n"
        )
        if self._context.get("active_model") == model_name and self._context.get(
            "active_id"
        ):
            record = model.browse(self._context["active_id"])
        if self._context.get("active_model") == model_name and self._context.get(
            "active_ids"
        ):
            records = model.browse(self._context["active_ids"])
        eval_context.update(
            {
                # orm
                "env": self.env,
                "model": model,
                # Exceptions
                "Warning": exceptions.Warning,
                "UserError": exceptions.UserError,
                # record
                "record": record,
                "records": records,
                # utils
                "format_number": format_number,
            }
        )
        return eval_context

    def compute_value(self, report_rec):
        _eval_context = self._get_eval_context(report_rec)
        _logger.error(f"\n\n\n_eval_context:\n{_eval_context}\n\n\n")
        safe_eval(self.default_value.strip(), _eval_context, mode="exec", nocopy=True)
        return (
            _eval_context["value"]
            if _eval_context.get("value", "key absent") != "key absent"
            else ""
        )
