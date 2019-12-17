from odoo import api, fields, models


class ContractOrderAnnex(models.Model):
    _name = "res.partner.contract.annex"
    _description = "Contract Order Annex"

    name = fields.Char(string="Name", help="The Number of Annex")
    order_ids = fields.One2many("sale.order", "contract_annex_id", string="Order")
    contract_id = fields.Many2one(
        "res.partner.contract", string="Contract", readonly=True
    )

    @api.model
    def create(self, values):
        record = super().create(values)

        # Compute name if there is no custom name
        if not record.name:
            contract_number = record.contract_id.name
            annex_number = len(record.contract_id.contract_annex_ids.ids)

            record.name = "{contract}--{annex}".format(
                contract=contract_number, annex=annex_number
            )

        return record
