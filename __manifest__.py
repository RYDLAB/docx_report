# -*- coding: utf-8 -*-
{
    "name": "Client Contracts",
    "summary": """
        Print forms for contracts with clients""",
    "description": """
        Module for storing and creating print forms for contracts with clients
    """,
    "author": "RYDLAB",
    "website": "http://rydlab.ru",
    "category": "Invoicing & Payments",
    "version": "0.2.0",
    "depends": ["base", "contacts", "hr", "russian_requisites", "sale",],
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
