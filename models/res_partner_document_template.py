from odoo import _, fields, models


class DocumentTemplate(models.Model):
    _name = "res.partner.document.template"
    _description = "Document Template"
    _order = "company_type,document_type,sequence"

    name = fields.Char()
    attachment_id = fields.Many2one(
        "ir.attachment",
        string="Template Attachment",
        ondelete="cascade",
        required=True,
    )
    document_type = fields.Selection(
        string="Type of document",
        selection=[
            ("contract", _("Contract")),
            ("annex", _("Annex")),
            ("addition", _("Addition")),
        ],
    )
    document_type_name = fields.Selection(
        string="Document",
        selection=[
            ("bill", _("Bill")),
            ("specification", _("Specification")),
            ("approval_list", _("Approval List")),
            ("act_at", _("Act of Acceptance and Transfer")),
            ("act_ad", _("Act of Acceptance and Delivery")),
        ],
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
