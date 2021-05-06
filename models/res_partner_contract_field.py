from odoo import fields, models


class ContractField(models.Model):
    _name = "res.partner.contract.field"
    _description = "Contract Field"
    _order = "sequence"

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
    description = fields.Char(
        string="Description",
        help="Description for this field to be showed in fields list in print form creation wizard.",
        translate=True,
        default="",
    )
    sequence = fields.Integer(
        string="Sequence",
    )
    visible = fields.Boolean(
        string="Visible",
        help="To show this field in fields list in print form creation wizard\n"
        "User can change showed field's values in wizard.",
        default=True,
    )
