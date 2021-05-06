# -*- coding: utf-8 -*-
{
    "name": "Client Contracts",
    "summary": """
        Print forms for contracts with clients""",
    "description": """
        Module for storing and creating print forms for contracts.
    """,
    "author": "RYDLAB",
    "website": "http://rydlab.ru",
    "category": "Invoicing & Payments",
    "version": "14.0.1.0.0",
    "depends": ["base", "contacts", "hr", "l10n_ru", "sale", "sale_margin"],
    "external_dependencies": {"python": ["docxtpl", "num2words"]},
    "data": [
        "data/assets_extension.xml",
        "data/fields_default.xml",
        "data/payment_terms.xml",
        "security/ir.model.access.csv",
        "views/res_partner_contract.xml",
        "views/res_partner_contract_annex.xml",
        "views/res_partner_contract_field.xml",
        "views/res_partner_document_template.xml",
        "views/res_partner.xml",
        "views/sale_order.xml",
        "wizard/res_partner_contract_wizard.xml",
    ],
}
