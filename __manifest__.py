# -*- coding: utf-8 -*-
{
    'name': "client_contracts",

    'summary': """
        Module for storing and creating print forms for contracts with clients""",

    'description': """
        Module for storing and creating print forms for contracts with clients
    """,

    'author': "RYDLAB",
    'website': "http://rydlab.ru",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'hr',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
        'views/res_partner.xml',
        'views/contract_wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
