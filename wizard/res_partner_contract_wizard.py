# -*- coding: utf-8 -*-
import base64
import logging
import math
from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError
from pytils import numeral

from ..utils.docxtpl import get_document_from_values_stream

_logger = logging.getLogger(__name__)


class ContractWizard(models.TransientModel):
    _name = "res.partner.contract.wizard"

    def _get_default_template(self):
        _template = self.env["res.partner.contract.template"].search(
            [("is_default", "=", True)]
        )
        if _template:
            return _template[0].id
        return False

    def _get_default_partner(self):
        current_id = self.env.context.get("active_ids")
        return self.env["res.partner.contract"].browse([current_id[0]]).partner_id.id

    company_id = fields.Many2one(
        "res.partner",
        string="Company",
        default=lambda self: self.env.user.company_id.partner_id,
    )
    contract_id = fields.Many2one(
        "res.partner.contract",
        string="Contract",
        default=lambda self: self.env.context.get("active_id"),
    )
    delivery_terms = fields.Integer(string="Delivery terms", default=10)
    order_id = fields.Many2one("sale.order", string="Appex order", help="Appex",)
    partner_id = fields.Many2one(
        "res.partner", string="Partner", default=_get_default_partner
    )
    payment_terms = fields.Integer(string="Payment term", default=45)
    template = fields.Many2one(
        "res.partner.contract.template",
        string="Template",
        help="Template for contract",
        default=_get_default_template,
    )
    type = fields.Selection(
        selection=[("person", "With person"), ("company", "With company")],
        string="Type of contract",
        default="company",
    )

    transient_field_ids = fields.One2many(
        "res.partner.contract.field.transient",
        "_contract_wizard_id",
        string="Contract Fields",
    )

    @api.onchange("partner_id")
    def _set_order_domain(self):
        current_id = self.env.context.get("active_ids")
        domain = [("contract_id", "=", current_id)]
        return {"domain": {"order_id": domain}}

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        """Creates transient fields for generate contract template
        Looks as a tree view of *_contract_field_transient model in xml
        """

        def get_contract_field(technical_name):
            return self.env["res.partner.contract.field"].search(
                [("technical_name", "=", technical_name),]
            )

        self.contract_id = self.env.context.get("active_id")

        contract_context_values = (
            self.env.ref("client_contracts.action_get_context")
            .with_context({"onchange_self": self})
            .run()
        )

        self.transient_field_ids = [  # one2many
            (
                4,
                self.env["res.partner.contract.field.transient"]
                .create(
                    {"contract_field_id": get_contract_field(field).id, "value": value,}
                )
                .id,
                0,
            )
            for field, value in sorted(contract_context_values.items())
        ]

    @api.multi
    def get_docx_contract(self):
        template = self.template.attachment_id
        if not template:
            raise UserError("Template must be set up")

        path_to_template = template._full_path(template.store_fname)

        fields = {
            transient_field.technical_name: transient_field.value
            for transient_field in self.transient_field_ids
            if transient_field.technical_name and transient_field.value
        }

        binary_data = get_document_from_values_stream(path_to_template, fields).read()
        encoded_data = base64.b64encode(binary_data)

        attachment_name = "Contract-{number}.{ext}".format(
            number=self.contract_id.name, ext="docx"
        )
        document_as_attachment = self.env["ir.attachment"].create(
            {
                "name": attachment_name,
                "datas_fname": attachment_name,
                "type": "binary",
                "datas": encoded_data,
            }
        )

        # Send message with attachment to a mail.thread of the company
        self.env["mail.message"].create(
            {
                "model": "res.partner.contract",
                "res_id": self.contract_id.id,
                "message_type": "comment",
                "attachment_ids": [(4, document_as_attachment.id, False)],
            }
        )

        return document_as_attachment

    def modf(self, arg):
        """Math.modf function for using in XML ir.action.server code
        Uses in data/fields_default.xml
        """
        return math.modf(arg)

