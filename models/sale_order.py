from odoo import api, fields, models

from ..utils import MODULE_NAME


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # TODO: exists original field "commitment_date".
    delivery_time = fields.Integer(
        string="Delivery Time",
        default=45,
    )
    contract_annex_id = fields.Many2one(
        comodel_name="res.partner.contract.annex",
        string="Contract Annex",
        compute="get_contract_annex_id",
    )
    contract_annex_ids = fields.One2many(
        comodel_name="res.partner.contract.annex",
        inverse_name="order_id",
        string="Annex for this Sale order",
        help="Technical field for binding with contract annex\n"
        "In form this link showed in 'contract_annex_id' field.",
    )

    # Extend default field for showing payment terms created by this module only.
    payment_term_id = fields.Many2one(
        comodel_name="account.payment.term",
        domain=lambda self: [("id", "in", self._get_payment_terms())],
    )

    def _get_payment_terms(self):
        terms = [
            self.env.ref("{}.{}".format(MODULE_NAME, external_id)).id
            for external_id in (
                "payment_term_prepaid",
                "payment_term_postpayment",
                "payment_term_partial_2",
                "payment_term_partial_3",
            )
        ]
        return terms

    @api.onchange("contract_annex_ids")
    def get_contract_annex_id(self):
        if self.contract_annex_ids:
            self.contract_annex_id = self.contract_annex_ids[0].id
        else:
            self.contract_annex_id = False
