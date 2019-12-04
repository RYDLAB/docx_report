import datetime

from odoo import api, fields, models


class PartnerContract(models.Model):
    _name = 'res.partner.contract'
    _inherit = 'mail.thread'

    name = fields.Char(
        string='Contract number',
        help='Number of contract, letters and digits',
    )
    date = fields.Date(
        string='Date of conclusion',
        help='Date, when contract was concluded',
        default=datetime.date.today(),
        required=True
    )
    order_ids = fields.One2many(
        'sale.order',
        'contract_id',
        string='Annexes',
        help='Annexes to this contract'
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Contract Partner',
        help='Contract partner',
        default=lambda self: self.env.context['active_id'],
        required=True
    )

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

    def _calculate_contract_name(self, _date):

        contract_date = datetime.strptime(_date, '%Y-%m-%d')
        date_part = contract_date.strftime('%d%m-%y')

        today_contracts = self.search([
            ('date', '=', contract_date.date()),
        ])
        if len(today_contracts) > 0:
            last_contract_number = int(
                today_contracts[-1].name.split('-')[2]) + 1
        else:
            last_contract_number = 1

        return '{}-{}'.format(date_part, last_contract_number)


class AnnexType(models.Model):
    _name = 'res.partner.contract.annex.type'

    name = fields.Char(
        string='Annex template name'
    )
    description = fields.Text(
        string='Annex template description'
    )


class ContractTemplate(models.Model):
    _name = 'res.partner.contract.template'

    attachment_id = fields.Many2one(
        'ir.attachment',
        string="Template Attachment",
        required=True,
    )
    is_default = fields.Boolean(
        string='Default Template',
        default=False,
    )
