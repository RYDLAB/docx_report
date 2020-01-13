import datetime

from odoo import _, api, fields, models
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

from ..utils import MODULE_NAME


class PartnerContract(models.Model):
    _name = "res.partner.contract"
    _description = "Contract"
    _inherit = ["mail.thread", "mail.activity.mixin", "mail.followers"]

    def _get_default_name(self):
        """Returns name format `№YYMM-D-N`,
        where N is a sequence number of contracts which are created this day
        """
        current_day_ts = (
            datetime.datetime.now()
            .replace(minute=0, hour=0, second=0, microsecond=0)
            .timestamp()
        )
        partner = self.env["res.partner"].browse(self.env.context.get("active_id"))

        contracts_today = self.search(
            [("partner_id", "=", partner.id), ("create_date_ts", ">=", current_day_ts),]
        )

        contract_date = "{format_date}-{number}".format(
            format_date=datetime.date.strftime(datetime.date.today(), "%y%m-%d"),
            number=len(contracts_today) + 1,
        )
        return contract_date

    def _get_default_create_date_ts(self):
        """Returns timestamp of now by local datetime"""
        return datetime.datetime.now().timestamp()

    res_model = fields.Char(default=lambda self: self._name)
    name = fields.Char(string="Contract number", default=_get_default_name,)
    create_date = fields.Datetime(string="Created on")
    create_date_ts = fields.Char(default=_get_default_create_date_ts)
    date_conclusion = fields.Date(string="Date of system conclusion",)
    date_conclusion_fix = fields.Date(
        string="Date of manual conclusion",
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
        view = self.env.ref(
            "{}.res_partner_wizard_print_contract_view".format(MODULE_NAME)
        )
        return {
            "name": _("Print Form of Contract"),
            "type": "ir.actions.act_window",
            "res_model": "res.partner.contract.wizard",
            "view_mode": "form",
            "view_id": view.id,
            "target": "new",
            "context": {"self_id": self.id},
        }

    def get_date(self):
        """Uses in xml action (data/fields_default)

        Returns:
            datetime.datetime -- date_conclusion_fix or date_conclusion or create_date
        """
        date = self.date_conclusion_fix or self.date_conclusion
        if date:
            date = datetime.datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)
        else:
            date = self.create_date
            date = datetime.datetime.strptime(date, DEFAULT_SERVER_DATETIME_FORMAT)
        return date

    def _(self, arg):
        """Uses in xml action (data/fields_default)

        Arguments:
            arg {str} -- String to translate
        """
        return _(arg)


class DocumentTemplate(models.Model):
    _name = "res.partner.document.template"
    _description = "Document Template"
    _order = "sequence"

    name = fields.Char()
    attachment_id = fields.Many2one(
        "ir.attachment", string="Template Attachment", required=True,
    )
    company_type = fields.Selection(
        selection=[
            ("person", "Individual"),
            ("sp", "Sole Proprietor"),
            ("plc", "Private Limited Company"),
        ]
    )
    template_type = fields.Selection(
        selection=[("contract", "Contract"), ("annex", "Annex"),]
    )
    sequence = fields.Integer()
