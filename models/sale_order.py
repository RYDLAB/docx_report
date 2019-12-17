from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    contract_annex_id = fields.Many2one(
        "res.partner.contract.annex", string="Contract Annex", readonly=True
    )
