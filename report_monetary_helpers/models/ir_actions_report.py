from logging import getLogger

from odoo import api, models

from ..utils.num2words import num2words_, num2words_currency
from ..utils.format_number import format_number

_logger = getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    @api.model
    def _get_rendering_context(self, docids, data):
        data = super()._get_rendering_context(docids, data)
        data.update(
            {
                "number2words": num2words_,
                "currency2words": num2words_currency,
                "format_number": format_number,
            }
        )
        return data
