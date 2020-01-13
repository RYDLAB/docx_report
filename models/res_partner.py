from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    name_write = fields.Char(
        string="Name (in contracts)",
        help="This name uses in contracts",
    )
    name_genitive = fields.Char(string="Name Genitive",)
    name_initials = fields.Char(string="Name Initials",)
    function_genitive = fields.Char(string="Function Genitive",)  # TODO: have no use of this
    client_contract_ids = fields.One2many(
        "res.partner.contract", "partner_id", string="Contracts",
    )
    contract_count = fields.Integer(
        compute="_compute_contract_count", string="# of contracts"
    )
    full_address = fields.Char(
        compute="_compute_full_address"
    )  # Check for res.partner.contact_address in base/res
    street_actual = fields.Many2one("res.partner", string="Actual Address",)
    representative_id = fields.Many2one(
        "res.partner", string="Representative", help="Person, who represents company"
    )
    representative_document = fields.Char(
        string="Representative acts on the basis of", help="Parent Case",
    )
    signature = fields.Binary(string="Client signature")
    phone_whatsapp = fields.Char(
        string="WhatsApp", help="If a contact have a WhatsApp number",
    )
    phone_telegram = fields.Char(
        string="Telegram", help="If a contact have a Telegram number or identifier",
    )

    @api.depends("street", "street2", "city", "state_id", "zip", "country_id")
    def _compute_full_address(self):
        for record in self:
            data = filter(
                None,
                map(
                    lambda s: s and s.strip(),
                    [
                        record.zip,
                        record.street,
                        record.street2,
                        record.country_id.name,
                        record.city,
                    ],
                ),
            )
            record.full_address = ", ".join(data)

    @api.one
    @api.depends("self.client_contract_ids")
    def _compute_contract_count(self):
        self.contract_count = len(self.client_contract_ids)
