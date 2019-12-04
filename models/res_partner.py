from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    bank_account = fields.Many2one(
        'res.partner.bank',
        string='Bank account'
    )
    client_contract_ids = fields.One2many(
        'res.partner.contract',
        'partner_id',
        string='Contracts',
        help='Contracts for this partner'
    )
    contract_count = fields.Integer(
        compute='_compute_contract_count',
        string='# of contracts'
    )
    # contract_job_name = fields.Char(
    #     string='Contract job name',
    #     help='Job position as it would be in contract'
    # ) # res.partner.function
    # contract_name = fields.Char(
    #     string='Contract name',
    #     help='Name, as it would be in contract'
    # ) # res.partner.name
    full_adress = fields.Char(
        compute='_compute_full_adress'
    )  # Check for res.partner.contact_address in base/res
    address_actual = fields.Char(
        string='Actual Address',
    )
    passport_authority = fields.Char(
        string='Passport Authority',
        help='What Department issued the passport',
    )
    passport_date = fields.Date(
        string='Passport Issue Date',
        help='Date when receive a passport',
    )
    passport_number = fields.Char(
        string='Passport Number',
    )
    passport_series = fields.Char(
        string='Passport Series',
    )
    psrn = fields.Char(
        string='PSRN',
        help='Primary State Registration Number',
    )
    representative_id = fields.Many2one(
        'res.partner',
        string='Representative',
        help='Person, who represents company'
    )
    signature = fields.Binary(
        string='Client signature'
    )

    @api.one
    @api.depends('street', 'street2', 'city', 'state_id', 'zip', 'country_id')
    def _compute_full_adress(self):
        address = ""
        full_street = "{} {}".format(
            self.street or "", self.street2 or "").strip()

        if self.zip:
            address += "{}, ".format(self.zip)

        address += ", ".join(map(lambda el: el,
                                 (
                                     self.country_id.name or "",
                                     self.city or "",
                                     full_street or ""
                                 )))
        self.full_adress = address

    @api.one
    @api.depends('self.client_contract_ids')
    def _compute_contract_count(self):
        self.contract_count = len(self.client_contract_ids)
