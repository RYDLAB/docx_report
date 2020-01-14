# -*- coding: utf-8 -*-
import base64
import logging

from odoo import _, api, fields, models

from ..utils import MODULE_NAME
from ..utils.docxtpl import get_document_from_values_stream

_logger = logging.getLogger(__name__)


class ContractWizard(models.TransientModel):
    _name = "res.partner.contract.wizard"

    def _get_default_partner(self):
        current_id = self.env.context.get("active_id")
        return self.env["res.partner.contract"].browse(current_id).partner_id.id

    target = fields.Reference(
        selection=[
            ("res.partner.contract", "Contract"),
            ("res.partner.contract.annex", "Contract Annex"),
        ],
        string="Target",
    )
    company_id = fields.Many2one("res.partner", string="Company")
    partner_id = fields.Many2one("res.partner", string="Partner")
    document_template = fields.Many2one(
        "res.partner.document.template", string="Document Template", required=True,
    )
    transient_field_ids = fields.One2many(
        "res.partner.contract.field.transient",
        "_contract_wizard_id",
        string="Contract Fields",
    )
    transient_field_ids_hidden = fields.One2many(
        "res.partner.contract.field.transient", "_contract_wizard_id",
    )

    @api.onchange("document_template")
    def _onchange_document_template(self):
        """Creates transient fields for generate contract template
        Looks as a tree view of *_contract_field_transient model in xml
        """

        def get_contract_field(technical_name):
            return self.env["res.partner.contract.field"].search(
                [("technical_name", "=", technical_name),]
            )

        # A model is the wizard called from
        active_model = self.env.context.get("active_model")
        # A record is the model called from (manually set with context)
        target_id = self.env.context.get("self_id")

        # Reference to this record
        self.target = "{model},{record_id}".format(
            model=active_model, record_id=int(target_id)
        )

        # Check for model and get this meta fields
        company_id = (
            self.target.company_id
            if hasattr(self.target, "company_id")
            else self.target.contract_id.company_id
        )
        partner_id = (
            self.target.partner_id
            if hasattr(self.target, "partner_id")
            else self.target.contract_id.partner_id
        )

        self.company_id = company_id
        self.partner_id = partner_id

        model_to_action = {
            "res.partner.contract": "{}.action_get_contract_context".format(
                MODULE_NAME
            ),
            "res.partner.contract.annex": "{}.action_get_annex_context".format(
                MODULE_NAME
            ),
        }
        action = model_to_action[active_model]

        # Get dictionary for `transient_fields_ids` with editable fields
        # With data from Odoo database
        contract_context_values = (
            self.env.ref(action).with_context({"onchange_self": self.target}).run()
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
            for field, value in sorted(
                contract_context_values.items(),
                key=lambda tpl: self.env.ref(
                    "{}.contract_field_{}".format(MODULE_NAME, tpl[0])
                ).sequence,
            )
        ]
        self.transient_field_ids_hidden = (
            self.transient_field_ids - self.transient_field_ids.filtered("visible")
        )
        self.transient_field_ids = (
            self.transient_field_ids - self.transient_field_ids_hidden
        )

        # Set up template domain
        template_type = {
            "res.partner.contract": "contract",
            "res.partner.contract.annex": "annex",
        }.get(active_model, False)
        company_type = (
            self.partner_id.company_form if self.partner_id.is_company else "person"
        )

        document_template_domain = [
            ("template_type", "=", template_type),
            ("company_type", "=", company_type),
        ]

        # Set default template
        self.document_template = self.env["res.partner.document.template"].search(document_template_domain, limit=1)

        return {"domain": {"document_template": document_template_domain,}}

    @api.multi
    def get_docx_contract(self):
        template = self.document_template.attachment_id

        path_to_template = template._full_path(template.store_fname)

        fields = {
            transient_field.technical_name: transient_field.value
            for transient_field in (
                self.transient_field_ids + self.transient_field_ids_hidden
            )
            if transient_field.technical_name and transient_field.value
        }

        binary_data = get_document_from_values_stream(path_to_template, fields).read()
        encoded_data = base64.b64encode(binary_data)

        attachment_name = "{name}-{number}.{ext}".format(
            number=self.target.name,
            ext="docx",
            name=(
                _("Contract")
                if self.target._name == "res.partner.contract"
                else (
                    _("Annex")
                    if self.target._name == "res.partner.contract.annex"
                    else ("Unknown")
                )
            ),
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
        res_id = self.target.id
        if hasattr(self.target, "contract_id"):
            res_id = self.target.contract_id.id

        self.env["mail.message"].create(
            {
                "model": "res.partner.contract",
                "res_id": res_id,
                "message_type": "comment",
                "attachment_ids": [(4, document_as_attachment.id, False)],
            }
        )

        return document_as_attachment
