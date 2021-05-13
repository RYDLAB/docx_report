import base64
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

from ..utils import MODULE_NAME
from ..utils.docxtpl import get_document_from_values_stream

_logger = logging.getLogger(__name__)


class ContractWizard(models.TransientModel):
    _name = "res.partner.contract.wizard"
    _inherit = ["client_contracts.utils"]

    def _default_target(self):
        return "{model},{target_id}".format(
            model=self.env.context.get("active_model"),
            target_id=int(self.env.context.get("self_id")),
        )

    def _default_document_template(self):
        return self.env["res.partner.document.template"].search(
            self._get_template_domain(), limit=1
        )

    def _get_template_domain(self):
        template_type = {
            "res.partner.contract": "contract",
            "res.partner.contract.annex": "annex",
            "sale.order": "offer",
        }.get(self.active_model, False)
        company_type = self.env.context.get("company_form", False)
        document_template_domain = [
            ("template_type", "=", template_type),
            ("company_type", "=", company_type),
        ]
        return document_template_domain

    target = fields.Reference(
        selection=[
            ("res.partner.contract", "Contract"),
            ("res.partner.contract.annex", "Contract Annex"),
            ("sale.order", "Offer"),
        ],
        string="Target",
        default=_default_target,
        help="Record of contract or annex entity, from where wizard has been called",
    )
    company_id = fields.Many2one(
        comodel_name="res.partner",
        string="Company",
        compute="_compute_company_id",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        compute="_compute_partner_id",
    )
    document_name = fields.Char(
        string="Document Name", compute="_compute_document_name"
    )
    document_template = fields.Many2one(
        comodel_name="res.partner.document.template",
        string="Document Template",
        default=_default_document_template,
        domain=lambda self: self._get_template_domain(),
        readonly=False,
    )
    transient_field_ids = fields.One2many(
        "res.partner.contract.field.transient",
        "_contract_wizard_id",
        string="Contract Fields",
    )
    transient_field_ids_hidden = fields.One2many(
        "res.partner.contract.field.transient",
        "_contract_wizard_id",
    )

    @api.depends("target")
    def _compute_company_id(self):
        if self.target and self.target.company_id:
            self.company_id = self.target.company_id.id
        else:
            self.company_id = self.env.company.id

    @api.depends("target")
    def _compute_partner_id(self):
        if self.target:
            self.partner_id = self.target.partner_id

    @api.depends("document_template", "target")
    def _compute_document_name(self):
        self.document_name = self.target.get_name_by_document_template(
            self.document_template
        )

    @api.constrains("document_template")
    def _check_document_template(self):
        if not self.document_template:
            raise ValidationError("You did not set up the template...")

    @api.onchange("document_template")
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

        def get_contract_field_data(field_name, field_value):
            rec = self.env["res.partner.contract.field"].search(
                [("technical_name", "=", field_name)]
            )
            if not rec:
                raise UserError(
                    _(
                        'Field "%s" specified in template, not found in model "res.partner.contract.field"'
                    )
                    % field_name
                )
            return {
                "contract_field_id": rec.id,
                "visible": rec.visible,
                "value": field_value,
            }

        model_to_action = {
            "res.partner.contract": "action_get_contract_context",
            "res.partner.contract.annex": "action_get_annex_context",
            "sale.order": "action_get_so_context",
        }
        action_external_id = "{}.{}".format(
            MODULE_NAME, model_to_action[self.active_model]
        )
        action_rec = self.env.ref(action_external_id)
        action_rec.model_id = (
            self.env["ir.model"].search([("model", "=", self.active_model)]).id
        )

        # Get dictionary for `transient_fields_ids` with editable fields
        # With data from Odoo database
        contract_context_values = action_rec.with_context(
            {"onchange_self": self.target}
        ).run()

        transient_fields_data = [
            get_contract_field_data(field_name, field_value)
            for field_name, field_value in contract_context_values.items()
        ]
        transient_fields_hidden_data = list(
            filter(lambda item: not item["visible"], transient_fields_data)
        )
        transient_fields_data = list(
            filter(lambda item: item["visible"], transient_fields_data)
        )

        self.transient_field_ids = [
            (
                6,
                False,
                self.env["res.partner.contract.field.transient"]
                .create(transient_fields_data)
                .ids,
            )
        ]
        self.transient_field_ids_hidden = [
            (
                6,
                False,
                self.env["res.partner.contract.field.transient"]
                .create(transient_fields_hidden_data)
                .ids,
            )
        ]

    # Other
    def get_docx_contract(self):
        template = self.document_template.attachment_id
        template_path = template._full_path(template.store_fname)

        payload = self.payload()
        binary_data = get_document_from_values_stream(template_path, payload).read()
        encoded_data = base64.b64encode(binary_data)

        get_fn = self.target.get_filename_by_document_template
        attachment_name = "{}.docx".format(get_fn(self.document_template or "Unknown"))

        document_as_attachment = (
            self.env["ir.attachment"]
            .sudo()
            .create(
                {
                    "name": attachment_name,
                    "store_fname": attachment_name,
                    "type": "binary",
                    "datas": encoded_data,
                }
            )
        )
        return self.afterload(document_as_attachment)

    def payload(self):
        # Collect fields into a key-value structure
        fields = {
            transient_field.technical_name: transient_field.value
            for transient_field in (
                self.transient_field_ids + self.transient_field_ids_hidden
            )
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
        if (
            self.target._name == "sale.order"
            or hasattr(self.target, "order_id")
            and self.target.order_id.order_line
        ):

            def number_generator(n=1):
                while True:
                    yield n
                    n += 1

            sale_order_rec = (
                self.target
                if self.target._name == "sale.order"
                else self.target.order_id
            )
            counter = number_generator()
            fields.update(
                {
                    "products": [
                        {
                            "number": next(counter),
                            "vendor_code": item.product_id.default_code,
                            "label": item.product_id.display_name,
                            "description": item.name,
                            # "uom": item.product_id.uom_po_id.name,
                            "count": item.product_uom_qty,
                            "unit": item.product_uom.name,
                            "cost": self.to_fixed(item.price_unit),
                            "cost_wo_vat": self.to_fixed(item.price_reduce_taxexcl),
                            "discount": self.to_fixed(item.discount),
                            "subtotal": self.to_fixed(item.price_subtotal),
                            "currency_symbol": item.currency_id.symbol,
                            "display_type": item.display_type,
                        }
                        for item in sale_order_rec.order_line or []
                    ],
                    "total_amount": self.to_fixed(
                        sum(sale_order_rec.order_line.mapped("price_subtotal"))
                    ),
                }
            )
        return self.middleware_fields(fields)

    def afterload(self, result):
        res_id = self.target.id
        if hasattr(self.target, "contract_id"):
            res_id = self.target.contract_id.id
        target_model = (
            self.target._name
            if self.target._name
            not in ("res.partner.contract", "res.partner.contract.annex")
            else "res.partner.contract"
        )
        self.env["mail.message"].create(
            {
                "model": self.env.context.get("attachment_model") or target_model,
                "res_id": self.env.context.get("attachment_res_id", res_id),
                "message_type": "comment",
                "attachment_ids": [(4, result.id, False)],
            }
        )
        return result

    @staticmethod
    def middleware_fields(kv):
        """
        Removes items without values from dictionary.
        :kv: dict.
        """
        # Debug False values
        empty = []
        for k, v in list(kv.items()):
            if not v:
                empty.append(k)
                kv.pop(k)
        _logger.debug("Empty fields: {}".format(empty))
        return kv

    @property
    def active_model(self):
        return self.env.context.get("active_model")
