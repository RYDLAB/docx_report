import base64

from odoo import api, fields, models
from odoo.exceptions import ValidationError

from ..utils import MODULE_NAME
from ..utils.docxtpl import get_document_from_values_stream


class ContractWizard(models.TransientModel):
    _name = "res.partner.contract.wizard"

    def _default_target(self):
        return "{model},{target_id}".format(
            model=self.active_model, target_id=int(self.env.context.get("self_id"))
        )

    def _default_document_template(self):
        return self.env["res.partner.document.template"].search(self._get_template_domain(), limit=1)

    def _get_template_domain(self):
        template_type = {
            "res.partner.contract": "contract",
            "res.partner.contract.annex": "annex",
        }.get(self.active_model, False)
        company_type = (
            self.partner_id.company_form if self.partner_id.is_company else "person"
        )

        document_template_domain = [
            ("template_type", "=", template_type),
            ("company_type", "=", company_type),
        ]
        return document_template_domain

    target = fields.Reference(
        selection=[
            ("res.partner.contract", "Contract"),
            ("res.partner.contract.annex", "Contract Annex"),
        ],
        string="Target",
        default=_default_target,
    )
    company_id = fields.Many2one(
        "res.partner", string="Company", compute="_compute_company_id",
    )
    partner_id = fields.Many2one(
        "res.partner", string="Partner", compute="_compute_partner_id",
    )
    document_name = fields.Char(
        string="Document Name", compute="_compute_document_name"
    )
    document_template = fields.Many2one(
        "res.partner.document.template",
        string="Document Template",
        default=_default_document_template,
        readonly=False,
    )
    transient_field_ids = fields.One2many(
        "res.partner.contract.field.transient",
        "_contract_wizard_id",
        string="Contract Fields",
    )
    transient_field_ids_hidden = fields.One2many(
        "res.partner.contract.field.transient", "_contract_wizard_id",
    )

    @api.depends("company_id", "target")
    def _compute_company_id(self):
        if self.target:
            self.company_id = self.target.company_id

    @api.depends("partner_id", "target")
    def _compute_partner_id(self):
        if self.target:
            self.partner_id = self.target.partner_id

    @api.depends("document_name", "document_template", "target")
    def _compute_document_name(self):
        self.document_name = self.target.get_name_by_document_template(
            self.document_template
        )

    @api.constrains("document_template")
    def _check_document_template(self):
        if not self.document_template:
            raise ValidationError("You did not set up the template...")

    @api.onchange('document_template')
    def _domain_document_template(self):
        return {
            "domain": {
                "document_template": self._get_template_domain(),
            }
        }

    @api.onchange("document_template")
    def _onchange_document_template(self):
        """Creates transient fields for generate contract template
        Looks as a tree view of *_contract_field_transient model in xml
        """

        def get_contract_field(technical_name):
            return self.env["res.partner.contract.field"].search(
                [("technical_name", "=", technical_name),]
            )

        model_to_action = {
            "res.partner.contract": "action_get_contract_context",
            "res.partner.contract.annex": "action_get_annex_context",
        }
        action = "{}.{}".format(MODULE_NAME, model_to_action[self.active_model])

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

    # Other

    @api.multi
    def get_docx_contract(self):
        template = self.document_template.attachment_id
        template_path = template._full_path(template.store_fname)

        payload = self.payload()
        binary_data = get_document_from_values_stream(template_path, payload).read()
        encoded_data = base64.b64encode(binary_data)

        get_fn = self.target.get_filename_by_document_template
        attachment_name = "{}.docx".format(get_fn(self.document_template or "Unknown"))

        document_as_attachment = self.env["ir.attachment"].create(
            {
                "name": attachment_name,
                "datas_fname": attachment_name,
                "type": "binary",
                "datas": encoded_data,
            }
        )

        return self.afterload(document_as_attachment)

    def payload(self):
        # Collect fields into a key-value structure
        fields = {
            transient_field.technical_name: transient_field.value
            for transient_field in (
                self.transient_field_ids + self.transient_field_ids_hidden
            )
            if transient_field.technical_name and transient_field.value
        }
        # Extend with special case
        if self.target._name == "res.partner.contract.annex":
            fields.update(
                {
                    "annex_name": self.document_name,
                    "specification_name": self.target.specification_name,
                }
            )
        # Extend with order product lines
        if hasattr(self.target, "order_id") and self.target.order_id.order_line:
            def number_generator(n=1):
                while (True):
                    yield n
                    n += 1

            counter = number_generator()

            fields.update(
                {
                    "order_products": [
                        {
                            "number": next(counter),
                            "label": item.product_id.name,
                            "count": item.product_uom_qty,
                            "unit": item.product_uom.name,
                            "cost": item.price_unit,
                            "amount": item.price_subtotal,
                        } for item in self.target.order_id.order_line or []
                    ]
                }
            )
        return fields

    def afterload(self, result):
        res_id = self.target.id
        if hasattr(self.target, "contract_id"):
            res_id = self.target.contract_id.id

        self.env["mail.message"].create(
            {
                "model": "res.partner.contract",
                "res_id": res_id,
                "message_type": "comment",
                "attachment_ids": [(4, result.id, False)],
            }
        )

        return result

    @property
    def active_model(self):
        return self.env.context.get("active_model")
