# -*- coding: utf-8 -*-
import base64
import math
from datetime import datetime

from odoo import api, fields, models
from pytils import numeral

from ..utils.docxtpl import get_document_from_values_stream

class ContractWizard(models.TransientModel):
    _name = 'res.partner.contract.wizard'

    def _get_default_template(self):
        _template = self.env['res.partner.contract.template'].search([
            ('is_default', '=', True)
        ])
        if _template:
            return _template[0].id
        return False

    def _get_default_partner(self):
        current_id = self.env.context.get('active_ids')
        return self.env['res.partner.contract'].browse([current_id[0]]).partner_id.id

    def _get_default_contract(self):
        current_id = self.env.context.get('active_ids')
        return self.env['res.partner.contract'].browse(current_id[0])

    def _get_partner_representer(self):
        return self.partner_id.representative_id

    _context_name = fields.Char(
        string='Contract number',
        compute='_compute_context_name',
        readonly=True
    )
    _context_date = fields.Char(
        string='Contract date',
        compute='_compute_context_date',
        readonly=True
    )
    _context_partner_contract_name = fields.Char(
        string='Partner contract name',
        compute='_compute_context_partner_contract_name',
        readonly=True
    )
    _context_partner_adress = fields.Char(
        compute='_compute_context_partner_adress',
        readonly=True
    )
    _context_partner_representer_contract_name = fields.Char(
        string='partner representer contract name',
        compute='_compute_context_partner_representer_contract_name',
        readonly=True
    )
    _context_partner_inn = fields.Char(
        string='Partner inn',
        compute='_compute_context_partner_inn',
        readonly=True
    )
    _context_partner_kpp = fields.Char(
        string='Partner kpp',
        compute='_compute_context_partner_kpp',
        readonly=True
    )
    _context_partner_rs = fields.Char(
        string='Partner corresponding account',
        compute='_compute_context_partner_rs',
        readonly=True
    )
    _context_partner_bik = fields.Char(
        string='Partner bank bik',
        compute='_compute_context_partner_bik',
        readonly=True
    )
    _context_partner_bank = fields.Char(
        string='Partner bank name',
        compute='_compute_context_partner_bank',
        readonly=True
    )
    _context_partner_phone = fields.Char(
        string='Partner phone',
        compute='_compute_context_partner_phone',
        readonly=True
    )
    _context_partner_representer_name = fields.Char(
        string='Partner representer name',
        compute='_compute_context_partner_representer_name',
        readonly=True
    )
    _context_seller_contract_name = fields.Char(
        string='Seller contract name',
        compute='_compute_context_seller_contract_name',
        readonly=True
    )
    _context_seller_adress = fields.Char(
        string='Seller full adress',
        compute='_compute_context_seller_adress',
        readonly=True
    )
    _context_seller_representer_contract_job_name = fields.Char(
        string='Seller representer contract job name',
        compute='_compute_context_seller_representer_contract_job_name',
        readonly=True
    )
    _context_seller_representer_contract_name = fields.Char(
        string='Seller representer contract name',
        compute='_compute_context_seller_representer_contract_name',
        readonly=True
    )
    _context_seller_inn = fields.Char(
        string='Seller inn',
        compute='_compute_context_seller_inn',
        readonly=True
    )
    _context_seller_kpp = fields.Char(
        string='Seller kpp',
        compute='_compute_context_seller_kpp',
        readonly=True
    )
    _context_seller_rs = fields.Char(
        string='Seller corresponding account',
        compute='_compute_context_seller_rs',
        readonly=True
    )
    _context_seller_bik = fields.Char(
        string='Seller bank bik',
        compute='_compute_context_seller_bik',
        readonly=True
    )
    _context_seller_bank = fields.Char(
        string='Seller bank name',
        compute='_compute_context_seller_bank',
        readonly=True
    )
    _context_seller_phone = fields.Char(
        string='Seller phone',
        compute='_compute_context_seller_phone',
        readonly=True
    )
    _context_seller_representer_job_name = fields.Char(
        string='Seller representer job name',
        compute='_compute_context_seller_representer_job_name',
        readonly=True
    )
    _context_seller_representer_name = fields.Char(
        string='Seller representer name',
        compute='_compute_context_seller_representer_name',
        readonly=True
    )
    _context_summ_rub = fields.Char(
        string='Contract summ(rub)',
        compute='_compute_context_summ_rub',
        readonly=True
    )
    _context_summ_rub_word = fields.Char(
        string='Contract summ(rub), word',
        compute='_compute_context_summ_rub_word',
        readonly=True
    )
    _context_summ_kop = fields.Char(
        string='Contract summ(kop)',
        compute='_compute_context_summ_kop',
        readonly=True
    )
    _context_summ_word = fields.Char(
        string='Contract summ word',
        compute='_compute_context_summ_word',
        readonly=True
    )
    _context_delivery_term = fields.Char(
        string='Contract delivery term',
        compute='_compute_context_delivery_term',
        readonly=True
    )
    _context_delivery_term_word = fields.Char(
        string='Contract delivery term word',
        compute='_compute_context_delivery_term_word',
        readonly=True
    )
    _context_payment_term = fields.Char(
        string='Contract payment term',
        compute='_compute_context_payment_term', readonly=True
    )
    _context_payment_term_word = fields.Char(
        string='Contract payment term word',
        compute='_compute_context_payment_term_word', readonly=True
    )
    _context_partner_passport_data = fields.Char(
        string='Partner passport data',
        compute='_compute_partner_passport_data',
        readonly=True
    )

    annex_lines = fields.One2many(
        'res.partner.contract.annex.line',
        'id',
        auto_join=True,
        copy=True
    )
    company_id = fields.Many2one(
        'res.partner',
        string='Company',
        help='Seller company',
        default=lambda self: self.env.user.company_id.partner_id
    )
    contract_id = fields.Many2one(
        'res.partner.contract',
        string='Contract',
        default=_get_default_contract
    )
    delivery_terms = fields.Integer(
        string='Delivery terms',
        help='When product must be delivered',
        default=10
    )
    order_id = fields.Many2one(
        'sale.order',
        string='Appex order',
        help='Appex',
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        help='Partner to render contract',
        default=_get_default_partner
    )
    payment_terms = fields.Integer(
        string='Payment term',
        help='When customer must pay',
        default=45
    )
    template = fields.Many2one(
        'res.partner.contract.template',
        string='Template',
        help='Template for contract',
        default=_get_default_template
    )
    type = fields.Selection(
        selection=[
            ('person', 'With person'),
            ('company', 'With company')
        ],
        string='Type of contract',
        default='company'
    )

    @api.depends('contract_id')
    def _compute_context_name(self):
        self._context_name = self.contract_id.name

    @api.depends('contract_id')
    def _compute_context_date(self):
        contract_date = datetime.strptime(self.contract_id.date, '%Y-%m-%d')
        self._context_date = contract_date.strftime('%d %B %Y')

    @api.depends('partner_id')
    def _compute_context_partner_contract_name(self):
        self._context_partner_contract_name = self.partner_id.contract_name

    @api.depends('partner_id')
    def _compute_context_partner_adress(self):
        self._compute_context_partner_adress = self.partner_id.full_adress

    @api.depends('partner_id')
    def _compute_context_partner_representer_contract_name(self):
        # TODO: lite refactor
        if self.partner_id.representative_id:
            partner_representer_contract_name = self.partner_id.representative_id.contract_name
        else:
            partner_representer_contract_name = ''
        self._context_partner_representer_contract_name = partner_representer_contract_name

    @api.depends('partner_id')
    def _compute_context_partner_inn(self):
        self._context_partner_inn = self.partner_id.inn

    @api.depends('partner_id')
    def _compute_context_partner_kpp(self):
        self._context_partner_kpp = self.partner_id.kpp

    @api.depends('partner_id')
    def _compute_context_partner_rs(self):
        self._context_partner_rs = self.partner_id.bank_account.acc_number

    @api.depends('partner_id')
    def _compute_context_partner_bik(self):
        self._context_partner_bik = self.partner_id.bank_account.bank_id.bic

    @api.depends('partner_id')
    def _compute_context_partner_bank(self):
        self._context_partner_bank = self.partner_id.bank_account.bank_id.name

    @api.depends('partner_id')
    def _compute_context_partner_phone(self):
        self._context_partner_phone = self.partner_id.phone

    @api.depends('partner_id')
    def _compute_context_partner_representer_name(self):
        self._context_partner_representer_name = self.partner_id.representative_id.name

    @api.depends('company_id')
    def _compute_context_seller_contract_name(self):
        self._context_seller_contract_name = self.company_id.contract_name

    @api.depends('company_id')
    def _compute_context_seller_adress(self):
        self._context_seller_adress = self.company_id.full_adress

    @api.depends('company_id')
    def _compute_context_seller_representer_contract_job_name(self):
        # TODO: lite refactor
        if self.company_id.representative_id:
            seller_represent_contract_job_name = self.company_id.representative_id.contract_job_name
        else:
            seller_represent_contract_job_name = ''
        self._context_seller_representer_contract_job_name = seller_represent_contract_job_name

    @api.depends('company_id')
    def _compute_context_seller_representer_contract_name(self):
        # TODO: lite refactor
        if self.company_id.representative_id:
            seller_represent_contract_name = self.company_id.representative_id.contract_name
        else:
            seller_represent_contract_name = ''
        self._context_seller_representer_contract_name = seller_represent_contract_name

    @api.depends('company_id')
    def _compute_context_seller_inn(self):
        self._context_seller_inn = self.company_id.inn

    @api.depends('company_id')
    def _compute_context_seller_kpp(self):
        self._context_seller_kpp = self.company_id.kpp

    @api.depends('company_id')
    def _compute_context_seller_rs(self):
        self._context_seller_rs = self.company_id.bank_account.acc_number

    @api.depends('company_id')
    def _compute_context_seller_bik(self):
        self._context_seller_bik = self.company_id.bank_account.bank_id.bic

    @api.depends('company_id')
    def _compute_context_seller_bank(self):
        self._context_seller_bank = self.company_id.bank_account.bank_id.name

    @api.depends('company_id')
    def _compute_context_seller_phone(self):
        self._context_seller_phone = self.company_id.phone

    @api.depends('company_id')
    def _compute_context_seller_representer_job_name(self):
        # TODO: lite refactor
        if self.company_id.representative_id:
            seller_represent_job_name = self.company_id.representative_id.function
        else:
            seller_represent_job_name = ''
        self._context_seller_representer_job_name = seller_represent_job_name

    @api.depends('company_id')
    def _compute_context_seller_representer_name(self):
        # TODO: lite refactor
        if self.company_id.representative_id:
            seller_represent_name = self.company_id.representative_id.name
        else:
            seller_represent_name = ''
        self._context_seller_representer_name = seller_represent_name

    @api.depends('order_id')
    def _compute_context_summ_rub(self):
        # TODO: lite refactor
        if self.order_id:
            amount = math.modf(self.order_id.amount_total)
        else:
            amount = math.modf(0.0)
        self._context_summ_rub = str(int(amount[1]))

    @api.depends('order_id')
    def _compute_context_summ_rub_word(self):
        # TODO: lite refactor
        if self.order_id:
            amount = math.modf(self.order_id.amount_total)
        else:
            amount = math.modf(0.0)
        self._context_summ_rub_word = numeral.in_words(int(amount[1]))

    @api.depends('order_id')
    def _compute_context_summ_kop(self):
        # TODO: lite refactor
        if self.order_id:
            amount = math.modf(self.order_id.amount_total)
            self._context_summ_kop = str(int(amount[0]))
        else:
            self._context_summ_kop = '0'

    @api.depends('order_id')
    def _compute_context_summ_word(self):
        self._context_summ_word = numeral.rubles(self.order_id.amount_total)

    @api.depends('delivery_terms')
    def _compute_context_delivery_term(self):
        self._context_delivery_term = self.delivery_terms

    @api.depends('delivery_terms')
    def _compute_context_delivery_term_word(self):
        self._context_delivery_term_word = numeral.in_words(
            self.delivery_terms)

    @api.depends('payment_terms')
    def _compute_context_payment_term(self):
        self._context_payment_term = self.payment_terms

    @api.depends('payment_terms')
    def _compute_context_payment_term_word(self):
        self._context_payment_term_word = numeral.in_words(self.payment_terms)

    @api.onchange('partner_id')
    def _compute_partner_passport_data(self):
        return self.partner_id.passport_data

    @api.onchange('partner_id')
    def _set_order_domain(self):
        current_id = self.env.context.get('active_ids')
        domain = [('contract_id', '=', current_id)]
        return {'domain': {'order_id': domain}}

    def _generate_context(self):
        contract_date = datetime.strptime(self.contract_id.date, '%Y-%m-%d')

        partner_representer_contract_name = ''

        seller_represent_contract_name = ''
        seller_represent_contract_job_name = ''
        seller_represent_name = ''
        seller_represent_job_name = ''

        if self.partner_id.representative_id:
            partner_representer_contract_name = self.partner_id.representative_id.contract_name

        if self.company_id.representative_id:
            seller_represent_contract_name = self.company_id.representative_id.contract_name
            seller_represent_contract_job_name = self.company_id.representative_id.contract_job_name
            seller_represent_name = self.company_id.representative_id.name
            seller_represent_job_name = self.company_id.representative_id.function

        amount = math.modf(self.order_id.amount_total)

        order_goods = []
        counter = 1
        for line in self.order_id.order_line:
            order_line_values = {
                'label': counter,
                'description': line.name,
                'count': line.product_qty,
                'mesure': line.product_uom.name,
                'price': line.price_unit,
                'amount': line.price_total
            }
            order_goods.append(order_line_values)
            counter += 1

        annex_terms = ''
        counter = 1
        for line in self.annex_lines:
            annex_terms = annex_terms + \
                '{}) {}\n'.format(counter, line.description)
            counter += 1

        context = {
            'name': self.contract_id.name,
            'current_date': contract_date.strftime('%d %b %Y'),

            'partner_contract_name': self.partner_id.contract_name,
            'partner_adress': self.partner_id.full_adress,
            'partner_representer_contract_name': partner_representer_contract_name,
            'partner_inn': self.partner_id.inn,
            'partner_kpp': self.partner_id.kpp,
            'partner_rs': self.partner_id.bank_account.acc_number,
            'partner_bik': self.partner_id.bank_account.bank_id.bic,
            'partner_bank': self.partner_id.bank_account.bank_id.name,
            'partner_passport_data': self.partner_id.passport_data,
            'partner_phone': self.partner_id.phone,
            'partner_representer_name': self.partner_id.representative_id.name,

            'seller_contract_name': self.company_id.contract_name,
            'seller_adress': self.company_id.full_adress,
            'seller_representer_contract_job_name': seller_represent_contract_job_name,
            'seller_representer_contract_name': seller_represent_contract_name,
            'seller_inn': self.company_id.inn,
            'seller_kpp': self.company_id.kpp,
            'seller_rs': self.company_id.bank_account.acc_number,
            'seller_bik': self.company_id.bank_account.bank_id.bic,
            'seller_bank': self.company_id.bank_account.bank_id.name,
            'seller_phone': self.company_id.phone,
            'seller_representer_job_name': seller_represent_job_name,
            'seller_representer_name': seller_represent_name,

            'summ_rub': int(amount[1]),
            'summ_rub_word': numeral.in_words(int(amount[1])),
            'summ_kop': int(amount[0]),
            'delivery_term': self.delivery_terms,
            'delivery_term_word': numeral.in_words(self.delivery_terms),
            'payment_term': self.payment_terms,
            'payment_term_word': numeral.in_words(self.payment_terms),
            'annex_terms': annex_terms,
            'order_goods': order_goods,
        }
        return context

    def get_docx_contract(self):
        template = self.template.attachment_id
        path_to_template = template._full_path(template.store_fname)

        fields = self._generate_context()

        binary_data = get_document_from_values_stream(
            path_to_template, fields).read()
        encoded_data = base64.b64encode(binary_data)

        attachment = self.env['ir.attachment'].create({
            "name": "Contract-{}.doc".format(self.contract_id.name),
            "type": "binary",
            "datas": encoded_data,
        })
        return attachment


class AnnexLine(models.TransientModel):
    _name = 'res.partner.contract.annex.line'

    @api.onchange('annex_type')
    def _get_default_description(self):
        self.description = self.annex_type.description

    annex_type = fields.Many2one(
        'res.partner.contract.annex.type'
    )
    description = fields.Text()
