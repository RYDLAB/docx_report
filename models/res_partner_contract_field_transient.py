from odoo import fields, models


class ContractFieldTransient(models.TransientModel):
    _name = "res.partner.contract.field.transient"
    _description = "Contract Field Transient"

    _contract_wizard_id = fields.Many2one(
        'res.partner.contract.wizard',
        string='Contract',
        readonly=True,
    )
    contract_field_id = fields.Many2one(
        "res.partner.contract.field",
        string="Field",
    )
    technical_name = fields.Char(
        related="contract_field_id.technical_name",
        string="Technical Name",
        readonly=True,
    )
    name = fields.Char(
        related="contract_field_id.name",
        string="Name",
        readonly=True,
    )
    description = fields.Char(
        related="contract_field_id.description",
        string="Description",
        readonly=True,
    )
    value = fields.Char(
        string="Value",
        default="",
    )
