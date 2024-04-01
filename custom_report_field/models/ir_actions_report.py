from logging import getLogger

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    custom_report_field_ids = fields.One2many(
        comodel_name="custom.report.field",
        inverse_name="ir_actions_report_id",
        string="Custom report fields",
    )
    validate_custom_report_field = fields.Boolean(
        compute="_compute_validate_custom_report_field"
    )

    @api.depends("custom_report_field_ids")
    def _compute_validate_custom_report_field(self):
        self.validate_custom_report_field = bool(
            self.custom_report_field_ids.filtered("visible")
        )

    def _get_readable_fields(self):
        return super()._get_readable_fields() | {
            "validate_custom_report_field",
        }

    def get_custom_report_field_values(self):
        """
        Returns: dict with computed custom fields values.
        """
        # Bunch reports creation not supported for a while.
        self.ensure_one()
        report_custom_field_ids = self.env["custom.report.field"].search(
            [("ir_actions_report_id", "=", self.id)]
        )
        custom_report_field_values = {}
        for field_rec in report_custom_field_ids:
            field_value = field_rec.compute_value(self)
            if field_rec.required and not field_value:
                raise UserError(
                    """Required custom field %s of the report is not filled. It's value: %s.
                Fill it or remove "required" attribute if this value is ok."""
                    % (field_rec.name, field_value)
                )
            custom_report_field_values[field_rec.technical_name] = field_value
        return custom_report_field_values

    @api.model
    def _get_rendering_context(self, docids, data):
        """
        Redefined here to add custom report fields in context.
        :param docids: source documents IDs list
        :param data: dict containing current context
        :return: dict, updated context.
        """
        data = super()._get_rendering_context(docids, data)
        data.update(self.get_custom_report_field_values())
        return data
