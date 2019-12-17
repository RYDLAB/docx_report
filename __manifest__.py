# -*- coding: utf-8 -*-
{
    "name": "client_contracts",
    "summary": """
        Print forms for contracts with clients""",
    "description": """
        Module for storing and creating print forms for contracts with clients
    """,
    "author": "RYDLAB",
    "website": "http://rydlab.ru",
    "category": "Invoicing & Payments",
    "version": "0.1.1",
    "depends": ["base", "contacts", "l10n_ru_doc", "sale",],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_contract.xml",
        "views/res_partner_contract_annex.xml",
        "views/res_partner.xml",
        "wizard/res_partner_contract_wizard.xml",
        "data/fields_default.xml",
    ],
}
