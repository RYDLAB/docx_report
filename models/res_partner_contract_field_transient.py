from odoo import api, fields, models


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
        string="Technical Name",
    )
    name = fields.Char(
        string="Name",
    )
    description = fields.Char(
        string="Description",
    )
    value = fields.Char(
        string="Value",
        default="",
    )

    @api.model
    def create(self, values):
        res = super().create(values)

        res.technical_name = res.contract_field_id.technical_name
        res.name = res.contract_field_id.name
        res.description = res.contract_field_id.description

        return res
