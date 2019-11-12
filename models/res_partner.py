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
    contract_job_name = fields.Char(
        string='Contract job name',
        help='Job position as it would be in contract'
    )
    contract_name = fields.Char(
        string='Contract name',
        help='Name, as it would be in contract'
    )
    full_adress = fields.Char(
        compute='_compute_full_adress'
    )
    passport_data = fields.Char(
        string='Passport',
        help='Passport data'
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
        # TODO: lite rewrite
        if self.zip:
            full_adress = '{}, {}, {}, {} {}'.format(
                self.zip, self.country_id.name, self.city,
                self.street, self.street2
            )
        else:
            full_adress = '{}, {}, {} {}'.format(
                self.country_id.name, self.city,
                self.street, self.street2
            )
        self.full_adress = full_adress

    @api.one
    @api.depends('self.client_contract_ids')
    def _compute_contract_count(self):
        self.contract_count = len(self.client_contract_ids)
