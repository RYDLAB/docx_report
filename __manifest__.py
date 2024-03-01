{
    "name": "DOCX report",
    "summary": """Printing reports in docx format from docx templates.""",
    "description": """
        Adds generation reports from .docx templates like standard Odoo reports
        with qweb templates. Standard Odoo reports also available.
        For generating .pdf from .docx external service the "Gotenberg" is used,
        and it required module for integration with this service: "gotenberg".
        If integration module "gotenberg" is absent, or service itself unreachable
        there will be only reports in docx format.

        This is the beta version, bugs may be present.
    """,
    "author": "RYDLAB",
    "website": "https://rydlab.ru",
    "category": "Technical",
    "version": "15.0.1.8.1",
    "license": "LGPL-3",
    "depends": ["base", "web", "custom_report_field", "report_monetary_helpers"],
    "external_dependencies": {"python": ["docxcompose", "docxtpl", "bs4"]},
    "data": [
        "views/ir_actions_report_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "docx_report/static/src/css/mimetypes.css",
            "docx_report/static/src/js/action_manager_report.js",
        ],
    },
}
