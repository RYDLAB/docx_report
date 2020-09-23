from odoo import fields, models


class ContractFieldTransient(models.TransientModel):
    _name = "res.partner.contract.field.transient"
    _description = "Contract Field Transient"

    _contract_wizard_id = fields.Many2one(
        "res.partner.contract.wizard",
        string="Contract",
        readonly=True,
    )
    contract_field_id = fields.Many2one(
        "res.partner.contract.field",
        string="Field",
    )
    name = fields.Char(
        related="contract_field_id.name",
        string="Name",
        readonly=True,
    )
    technical_name = fields.Char(
        related="contract_field_id.technical_name",
        string="Technical Name",
        readonly=True,
    )
    description = fields.Char(
        related="contract_field_id.description",
        string="Description",
        readonly=True,
    )
    visible = fields.Boolean(
        related="contract_field_id.visible",
    )
    value = fields.Char(
        string="Value",
        default="",
    )
