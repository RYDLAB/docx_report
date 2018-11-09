# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api


class PartnerContract(models.Model):

    _name = 'res.partner.contract'

    name = fields.Char(
        string='Contract number',
        help='Number of contract, letters and digits',)
    date = fields.Date(
        string='Date of conclusion',
        help='Date, when contract was concluded',
        default=datetime.now().date(),
        required=True)
    partner_id = fields.Many2one(
        'res.partner',
        string='Contract Partner',
        help='Contract partner',
        default=lambda self: self.env.context['active_id'],
        required=True)
    order_ids = fields.One2many(
        'sale.order',
        'contract_id',
        string='Annexes',
        help='Annexes to this contract')

    def _calculate_contract_name(self, _date):
        contract_date = datetime.strptime(_date, '%Y-%m-%d')
        date_part = contract_date.strftime('%d%m-%y')
        today_contracts = self.search([('date', '=', contract_date.date())])
        if len(today_contracts) > 0:
            last_contract_number = int(today_contracts[-1].name.split('-')[2]) + 1
        else:
            last_contract_number = 1
        return '{}-{}'.format(date_part, last_contract_number)

    @api.onchange('date')
    def _change_contract_name(self):
        """
        Procedure for forming contract name
        :return: contract name in format "DDMM-YY-№"
        """

        self.name = self._calculate_contract_name(self.date)

    @api.model
    def create(self, vals):
        datetime_now = datetime.now().strftime("%Y-%m-%d")
        vals['name'] = self._calculate_contract_name(datetime_now)
        return super(PartnerContract, self).create(vals)


class AnnexType(models.Model):

    _name = 'res.partner.contract.annex.type'

    name = fields.Char(string='Annex template name')
    description = fields.Text(string='Annex template description')


class ResPartner(models.Model):

    _inherit = 'res.partner'

    client_contract_ids = fields.One2many(
        'res.partner.contract',
        'partner_id',
        string='Contracts',
        help='Contracts for this partner')
    contract_count = fields.Integer(
        compute='_compute_contract_count',
        string='# of contracts')
    contract_name = fields.Char(string='Contract name', help='Name, as it would be in contract')
    contract_job_name = fields.Char(string='Contract job name', help='Job position as it would be in contract')
    representative_id = fields.Many2one('res.partner', string='Representative', help='Person, who represents company')
    passport_data = fields.Char(string='Passport', help='Passport data')
    full_adress = fields.Char(compute='_compute_full_adress')
    bank_account = fields.Many2one('res.partner.bank', string='Bank account')
    signature = fields.Binary(string='Client signature')

    @api.one
    @api.depends('street', 'street2', 'city', 'state_id', 'zip', 'country_id')
    def _compute_full_adress(self):
        if self.zip:
            full_adress = '{}, {}, {}, {} {}'.format(self.zip, self.country_id.name, self.city, self.street,
                                                     self.street2)
        else:
            full_adress = '{}, {}, {} {}'.format(self.country_id.name, self.city, self.street,
                                                     self.street2)
        self.full_adress = full_adress

    @api.one
    @api.depends('self.client_contract_ids')
    def _compute_contract_count(self):
        self.contract_count = len(self.client_contract_ids)


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    contract_id = fields.Many2one(
        'res.partner.contract',
        string='Contract',
        help='Contract, assigned to this order')


class ContractTemplate(models.Model):

    _name = 'res.partner.contract.template'
    _inherit = 'ir.attachment'

    is_contract_template = fields.Boolean(srting='Is this document contract template?', default=True)
