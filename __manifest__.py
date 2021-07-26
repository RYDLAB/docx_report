{
    "name": "DOCX report",
    "summary": """Printing reports in docx format from docx templates.""",
    "description": """
        Adds docx reports printing from docx templates like standard Odoo reports
        with qweb templates. Standard Odoo reports also available.
        For generating pdf from docx external service the "gotenberg" is used.
        It should work at the same server as Odoo app. If "gotenberg" absent, there
        will be only reports in docx format.
    """,
    "author": "RYDLAB",
    "website": "http://rydlab.ru",
    "category": "Technical",
    "version": "0.0.1",
    "depends": ["base", "web", "custom_report_field", "report_monetary_helpers"],
    "external_dependencies": {"python": ["docxcompose", "docxtpl"]},
    "data": [
        "views/assets.xml",
        "views/ir_actions_report_views.xml",
    ],
}
