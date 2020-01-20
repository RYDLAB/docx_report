from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    cost_price = fields.Monetary(string="Cost Price", default=0)
    currency_id = fields.Many2one(related="company_id.currency_id", string="Currency", readonly=True)
