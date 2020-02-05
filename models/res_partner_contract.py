import datetime

from odoo import _, api, fields, models

from ..utils import MODULE_NAME
from ..utils.misc import Extension, IDocument


class PartnerContract(models.Model, IDocument, Extension):
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
    create_date_ts = fields.Char(default=_get_default_create_date_ts)
    res_model = fields.Char(default=lambda self: self._name)
    name = fields.Char(string="Contract number", default=_get_default_name,)
    create_date = fields.Datetime(string="Created on")
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
            "{}.res_partner_wizard_print_document_view".format(MODULE_NAME)
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

    def get_name_by_document_template(self, document_template_id):
        return self.name

    def get_filename_by_document_template(self, document_template_id):
        return _("{type} {number} from {date}").format(
            type=_(
                dict(document_template_id._fields["document_type"].selection).get(
                    document_template_id.document_type
                )
            ),
            number=self.name,
            date=self.get_date().strftime("%d.%m.%Y"),
        )

    def get_date(self):
        """Uses in xml action (data/fields_default)

        Returns:
            datetime.datetime -- date_conclusion_fix or date_conclusion or create_date
        """
        date = self.date_conclusion_fix or self.date_conclusion
        if date:
            date = self.parse_odoo_date(date)
        else:
            date = self.parse_odoo_datetime(self.create_date)
        return date

    def _(self, arg):
        """Uses in xml action (data/fields_default)

        Arguments:
            arg {str} -- String to translate
        """
        return _(arg)
