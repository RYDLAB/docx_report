import math

from odoo import _, api, fields, models

from ..utils import MODULE_NAME
from ..utils.misc import Extension, IDocument


class ContractOrderAnnex(models.Model, IDocument, Extension):
    _name = "res.partner.contract.annex"
    _description = "Contract Annex"

    name = fields.Char(string="Name",)
    display_name = fields.Char(compute="_compute_display_name",)
    order_id = fields.Many2one(
        "sale.order",
        string="Order",
        required=True,
        help="Orders with this partner which are not uses in annexes yet",
    )
    contract_id = fields.Many2one(
        "res.partner.contract", string="Contract", readonly=True,
    )
    number = fields.Integer(string="№",)
    date_conclusion = fields.Date(
        string="Conclusion Date", default=fields.Date.today(),
    )
    prepaid_expense = fields.Float(string="Prepaid Expense", default=0)
    delivery_time = fields.Integer(related="order_id.delivery_time", readonly=True,)
    payment_term = fields.Many2one(
        "account.payment.term", related="order_id.payment_term_id", readonly=True,
    )

    @api.onchange("order_id")
    def _onchange_order_id(self):
        contract_number = self.contract_id.name
        order_number = self.order_id.name or "SO###"

        self.name = "{contract}-{order}".format(
            contract=contract_number, order=order_number,
        )

        # Compute domain for order_id because of bug with
        # not working correctly domain in model
        return {
            "domain": {
                "order_id": [
                    ("partner_id", "=", self.contract_id.partner_id.id),
                    ("contract_annex_id", "=", False),
                ]
            }
        }

    @api.multi
    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = "№{} {}".format(record.number or record.contract_id.contract_annex_number, record.name)

    @api.model
    def create(self, values):
        record = super().create(values)

        # Fill annex_id to domain it in future
        record.order_id.contract_annex_id = record.id

        # Counter
        record.number = record.contract_id.contract_annex_number
        record.contract_id.contract_annex_number += 1

        return record

    @api.multi
    def action_print_form(self):
        view = self.env.ref(
            "{}.res_partner_wizard_print_document_view".format(MODULE_NAME)
        )
        return {
            "name": _("Print Form of Contract Annex"),
            "type": "ir.actions.act_window",
            "res_model": "res.partner.contract.wizard",
            "view_mode": "form",
            "view_id": view.id,
            "target": "new",
            "context": {"self_id": self.id},
        }

    def get_name_by_document_template(self, document_template_id):
        return {
            "specification": "{number} {name}",
            "approval_list": "{number}.1 {name}-1",
            "act_at": "{number}.2 {name}-2",
            "act_ad": "{number}.3 {name}-3",
        }.get(document_template_id.document_type_name, "Unknown").format(
            number=self.number,
            name=self.name,
        )

    def get_filename_by_document_template(self, document_template_id):
        return "{type} №{name}".format(
            type=_(dict(document_template_id._fields['document_type'].selection).get(document_template_id.document_type)),
            name={
                "bill": "{number} {type} {name}",
                "specification": "{number} {type} {name}",
                "approval_list": "{number}.1 {type} {name}-1",
                "act_at": "{number}.2 {type} {name}-2",
                "act_ad": "{number}.3 {type} {name}-3",
            }.get(document_template_id.document_type_name).format(
                number=self.number,
                type=_(dict(document_template_id._fields['document_type_name'].selection).get(document_template_id.document_type_name)),
                name=self.name,
            )
        )

    def modf(self, arg):
        """Math.modf function for using in XML ir.action.server code
        Uses in data/fields_default.xml
        """
        return math.modf(arg)
