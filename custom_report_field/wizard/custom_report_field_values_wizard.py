import logging

from odoo import _, api, fields, models
from odoo.addons.web.controllers.main import clean_action
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CustomReportFieldValuesWizard(models.TransientModel):
    _name = "custom.report.field.values.wizard"
    _description = "Custom report values field verify wizard"

    ir_actions_report_id = fields.Many2one(
        "ir.actions.report",
        string="Report",
    )
    field_values_ids = fields.One2many(
        comodel_name="custom.report.field.values.wizard.line",
        inverse_name="wizard_id",
        string="Custom report field values",
    )

    def _check_records_amount(self):
        """
        Checks source records for report generation. If more than one - raise error.
        """
        active_model = self._context.get("active_model")
        if active_model:
            record_id = self.env[active_model].browse(self._context.get("active_id"))
            record_ids = self.env[active_model].browse(self._context.get("active_ids"))
            records_for_report = record_id | record_ids
            if len(records_for_report) > 1:
                raise ValidationError(
                    'Reports with custom fields do not supports bunch report generation.\nReceived records of model "{}":\n{}'.format(
                        active_model,
                        [
                            "{} (id: {})".format(
                                rec.mapped("name")[0], rec.mapped("id")[0]
                            )
                            for rec in records_for_report
                        ],
                    )
                )

    @api.onchange("ir_actions_report_id")
    def _onchange_ir_actions_report_id(self):
        self._check_records_amount()
        custom_values_for_report = self.env["custom.report.field"].search(
            [
                ("ir_actions_report_id", "=", self.ir_actions_report_id.id),
                ("visible", "=", True),
            ]
        )
        self.field_values_ids = [
            (
                6,
                False,
                self.env["custom.report.field.values.wizard.line"]
                .create(
                    [
                        {
                            "name": field_rec.name,
                            "value": field_rec.compute_value(self.ir_actions_report_id),
                            "technical_name": field_rec.technical_name,
                            "description": field_rec.description,
                        }
                        for field_rec in custom_values_for_report
                    ]
                )
                .ids,
            )
        ]

    def get_report(self):
        self.ensure_one()
        cleaned_report = False
        action_id = self.ir_actions_report_id.id
        ctx = dict(self._context)
        ctx.update({"report_values_validated": True})
        report = self.env["ir.actions.report"].sudo().browse([action_id]).read()
        if report:
            cleaned_report = clean_action(report[0], env=self.env)
            cleaned_report["context"] = ctx
            _logger.error(
                f"""\n\n\nAfter 'clean_action:' self._context:\n{self._context}\nctx:\n{ctx}
                cleaned_report['context']: {cleaned_report.get('context')}\n\n\n"""
            )
        return cleaned_report


class CustomReportFieldValuesWizardLine(models.TransientModel):
    _name = "custom.report.field.values.wizard.line"
    _description = "Custom report values field verify wizard"

    wizard_id = fields.Many2one(
        "custom.report.field.values.wizard",
    )

    name = fields.Char(
        string="Name",
    )
    value = fields.Char(
        string="Value",
    )
    technical_name = fields.Char(
        string="Technical Name",
    )
    description = fields.Char(
        string="Description",
    )
