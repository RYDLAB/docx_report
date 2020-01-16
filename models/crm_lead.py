from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    cost_price = fields.Integer(string="Cost Price", default=0)
