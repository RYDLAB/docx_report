# -*- coding: utf-8 -*-
# noinspection PyStatementEffect
{
    "name": "Gotenberg™ integration",
    "summary": """Gotenberg integration with Odoo for file conversion.""",
    "description": """
        This module complements the functionality of docx_report_generation, 
        namely it allows you to generate printed forms in PDF from docx templates.
    """,
    "license": "LGPL-3",
    "author": "RYDLAB",
    "website": "http://rydlab.ru",
    "category": "Productivity",
    "version": "0.1",
    # |-------------------------------------------------------------------------
    # | Dependencies
    # |-------------------------------------------------------------------------
    # |
    # | References of all modules that this module depends on. If this module
    # | is ever installed or upgrade, it will automatically install any
    # | dependencies as well.
    # |
    "depends": ["base_setup"],
    # |-------------------------------------------------------------------------
    # | Data References
    # |-------------------------------------------------------------------------
    # |
    # | References to all XML data that this module relies on. These XML files
    # | are automatically pulled into the system and processed.
    # |
    "data": [
        "views/res_config_settings_views.xml",
    ],
    # |-------------------------------------------------------------------------
    # | Demo Data
    # |-------------------------------------------------------------------------
    # |
    # | A reference to demo data
    # |
    "demo": [],
    # |-------------------------------------------------------------------------
    # | Is Installable
    # |-------------------------------------------------------------------------
    # |
    # | Gives the user the option to look at Local Modules and install, upgrade
    # | or uninstall. This seems to be used by most developers as a switch for
    # | modules that are either active / inactive.
    # |
    "installable": True,
    # |-------------------------------------------------------------------------
    # | Auto Install
    # |-------------------------------------------------------------------------
    # |
    # | Lets Odoo know if this module should be automatically installed when
    # | the server is started.
    # |
    "auto_install": False,
}
