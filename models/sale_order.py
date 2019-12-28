from odoo import api, fields, models

from ..utils import MODULE_NAME


class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery_time = fields.Integer(string="Delivery Time", default=45,)
    contract_annex_id = fields.Many2one(
        "res.partner.contract.annex", string="Contract Annex", readonly=True,
    )
    # Extend default field
    payment_term_id = fields.Many2one(
        "account.payment.term",
        domain=lambda self: [("id", "in", self._get_payment_terms())],
    )

    @api.multi
    def _get_payment_terms(self):
        ref = self.env.ref
        terms = (
            ref("{}.payment_term_prepaid".format(MODULE_NAME)).id,
            ref("{}.payment_term_postpayment".format(MODULE_NAME)).id,
            ref("{}.payment_term_partial_2".format(MODULE_NAME)).id,
            ref("{}.payment_term_partial_3".format(MODULE_NAME)).id,
        )
        return terms
