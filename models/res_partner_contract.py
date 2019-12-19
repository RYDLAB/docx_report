import datetime

from odoo import api, fields, models


class PartnerContract(models.Model):
    _name = "res.partner.contract"
    _inherit = ["mail.thread", "mail.activity.mixin", "mail.followers"]

    name = fields.Char(string="Contract number",)
    date_conclusion = fields.Date(string="Date of conclusion",)
    date_conclusion_fix = fields.Date(
        string="Manual Date of conclusion",
        help="Field for manual edit when contract is signed or closed",
        default=lambda self: self.date_conclusion,
    )
    contract_annex_ids = fields.One2many(
        "res.partner.contract.annex",
        "contract_id",
        string="Annexes",
        help="Annexes to this contract",
    )
    contract_annex_number = fields.Integer(
        default=1, help="Counter for generate Annex name"
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        default=lambda self: self.env.context.get("active_id"),
        required=True,
    )
    company_id = fields.Many2one(
        "res.partner",
        string="Company",
        default=lambda self: self.env.user.company_id.partner_id,
    )
    state = fields.Selection(
        [("draft", "New"), ("sign", "Signed"), ("close", "Closed"),],
        string="Status",
        readonly=True,
        copy=False,
        index=True,
        track_visibility="onchange",
        track_sequence=3,
        default="draft",
    )

    @api.multi
    def action_sign(self):
        self.write({"state": "sign", "date_conclusion": fields.Date.today()})

    @api.multi
    def action_close(self):
        self.write({"state": "close"})

    @api.multi
    def action_renew(self):
        self.write({"state": "draft"})

    @api.multi
    def action_print_form(self):
        view = self.env.ref("client_contracts.res_partner_wizard_print_contract_view")
        return {
            "name": "Print Form of Contract",
            "type": "ir.actions.act_window",
            "res_model": "res.partner.contract.wizard",
            "view_mode": "form",
            "view_id": view.id,
            "target": "new",
            "context": {"self_id": self.id},
        }

    @api.model
    def create(self, vals):

        datetime_now = datetime.datetime.now().strftime("%Y-%m-%d")
        vals["name"] = self._calculate_contract_name(datetime_now)

        return super(PartnerContract, self).create(vals)

    def _calculate_contract_name(self, _date):

        contract_date = datetime.datetime.strptime(_date, "%Y-%m-%d")
        date_part = contract_date.strftime("%d%m-%y")

        today_contracts = self.search([("date_conclusion", "=", contract_date.date()),])
        if len(today_contracts) > 0:
            name = today_contracts[-1].name or "0-0-0"
            last_contract_number = int(name.split("-")[2]) + 1
        else:
            last_contract_number = 1

        return "{}-{}".format(date_part, last_contract_number)


class PrintTemplateContract(models.Model):
    _name = "res.partner.template.print.contract"
    _description = "Print Template Contract"

    attachment_id = fields.Many2one(
        "ir.attachment", string="Template Attachment", required=True,
    )
    is_default = fields.Boolean(string="Default Template", default=False,)


class PrintTemplateAnnex(models.Model):
    _name = "res.partner.template.print.annex"
    _description = "Print Template Contract Annex"

    attachment_id = fields.Many2one(
        "ir.attachment", string="Template Attachment", required=True,
    )
    is_default = fields.Boolean(string="Default Template", default=False,)
