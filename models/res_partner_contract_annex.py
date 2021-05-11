import math
import logging

from odoo import _, api, fields, models

from ..utils import MODULE_NAME

# from ..utils.misc import Extension, IDocument
_logger = logging.getLogger(__name__)


class ContractOrderAnnex(models.Model):  # , IDocument, Extension):
    _name = "res.partner.contract.annex"
    _inherit = ["client_contracts.utils"]
    _description = "Contract Annex"

    name = fields.Char(
        string="Name",
    )
    display_name = fields.Char(
        compute="_compute_display_name",
    )
    specification_name = fields.Char(
        compute="_compute_specification_name",
    )

    contract_id = fields.Many2one(
        "res.partner.contract",
        string="Contract",
        readonly=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        related="contract_id.company_id",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        related="contract_id.partner_id",
    )
    order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Sale order",
        help="Sale order for this annex.",
        required=True,
    )
    date_conclusion = fields.Date(
        string="Signing Date",
        default=fields.Date.today(),
    )
    counter = fields.Integer(
        string="№",
        help="Contract Annexes counter",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id.id,
    )

    design_period = fields.Integer(
        string="Design Period",
    )
    design_cost = fields.Monetary(
        string="Design Cost",
        currency_field="currency_id",
    )

    design_doc_period = fields.Integer(
        string="Documentation Design Period (days)",
    )
    design_doc_cost = fields.Monetary(
        string="Documentation Design Cost",
        currency_field="currency_id",
    )

    delivery_address = fields.Char(
        string="Delivery Address",
    )
    delivery_period = fields.Integer(string="Delivery Period (days)")

    installation_address = fields.Char(
        string="Installation Address",
    )
    installation_period = fields.Integer(
        string="Installation Period (days)",
    )
    installation_cost = fields.Integer(
        string="Installation Cost",
    )

    total_cost = fields.Monetary(
        string="Total Cost",
        currency_field="currency_id",
    )

    payment_part_one = fields.Float(
        string="Payment 1 Part (%)",
        default=100,
        digits="Account",
    )
    payment_part_two = fields.Float(
        string="Payment 2 Part (%)",
        digits="Account",
    )
    payment_part_three = fields.Float(
        string="Payment 3 Part (%)",
        digits="Account",
    )

    @api.depends("name")
    def _compute_display_name(self):
        for record in self:
            record.display_name = "№{} {}".format(
                record.counter or record.contract_id.contract_annex_number, record.name
            )

    @api.depends("contract_id", "order_id")
    def _compute_specification_name(self):
        self.specification_name = _("{name} from {date}").format(
            name="{}-{}".format(self.contract_id.name, self.order_id.name),
            date=self.contract_id.get_date().strftime("%d.%m.%Y"),
        )

    @api.onchange("order_id")
    def _domain_order_id(self):
        """Using domain function because of
        simple domain does not working properly because of
        contract_id is still False"""
        return {
            "domain": {
                "order_id": [
                    ("partner_id", "=", self.contract_id.partner_id.id),
                    ("contract_annex_id", "=", False),
                ]
            }
        }

    @api.onchange("order_id")
    def _onchange_order_id(self):
        contract_number = self.contract_id.name
        order_number = self.order_id.name or "SO###"

        self.name = "{contract}-{order}".format(
            contract=contract_number,
            order=order_number,
        )

    def create(self, values_list):
        _logger.debug("\n\n Values: %s\n\n", values_list)
        if isinstance(values_list, dict):
            values_list = [values_list]
            _logger.debug("\n\n Values fixed: %s\n\n", values_list)
        records = super(ContractOrderAnnex, self).create(values_list)
        for record in records:
            # Fill annex_id to domain it in future
            # record.order_id.contract_annex_id = record.id
            # Counter
            record.counter = record.contract_id.contract_annex_number
            record.contract_id.contract_annex_number += (
                1  # TODO: should I use a sequence?
            )
        return records

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
            "context": {
                "self_id": self.id,
                "active_model": self._name,
                "company_form": self.partner_id.company_form
                if self.partner_id.is_company
                else "person",
            },
        }

    def get_name_by_document_template(self, document_template_id):
        active_invoices = self.order_id.invoice_ids.filtered(
            lambda r: r.state not in ("draft", "cancel")
        )
        bill_name = active_invoices and active_invoices[-1].number

        return (
            {
                "bill": "{bill_name}",
                "specification": "{counter} {name}",
                "approval_list": "{counter}.1 {name}-1",
                "act_at": "{counter}.2 {name}-2",
                "act_ad": "{counter}.3 {name}-3",
            }
            .get(document_template_id.document_type_name, "Unknown")
            .format(
                counter=self.counter,
                name=self.name,
                bill_name=(bill_name or "Счёт отсутствует"),
            )
        )

    def get_filename_by_document_template(self, document_template_id):
        return "{type} №{name}".format(
            type=_(
                dict(document_template_id._fields["document_type"].selection).get(
                    document_template_id.document_type
                )
            ),
            name={
                "bill": "{counter} {type} {name}",
                "specification": "{counter} {type} {name}",
                "approval_list": "{counter}.1 {type} {name}-1",
                "act_at": "{counter}.2 {type} {name}-2",
                "act_ad": "{counter}.3 {type} {name}-3",
            }
            .get(document_template_id.document_type_name, "Unknown")
            .format(
                counter=self.counter,
                type=_(
                    dict(
                        document_template_id._fields["document_type_name"].selection
                    ).get(document_template_id.document_type_name)
                ),
                name=self.name,
            ),
        )

    def modf(self, arg):
        """Math.modf function for using in XML ir.action.server code
        Uses in data/fields_default.xml
        """
        return math.modf(arg)
