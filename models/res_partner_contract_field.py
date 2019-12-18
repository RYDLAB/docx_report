from odoo import fields, models


class ContractField(models.Model):
    _name = "res.partner.contract.field"
    _description = "Contract Field"

    name = fields.Char(string="Name", required=True, translate=True,)
    technical_name = fields.Char(
        string="Technical Name", help="Name uses in template", required=True,
    )
    description = fields.Char(string="Description", translate=True, default="",)
