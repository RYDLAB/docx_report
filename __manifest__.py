{
    "name": "DOCX report",
    "summary": """
        Print docx report from docx template""",
    "description": """""",
    "author": "RYDLAB",
    "website": "http://rydlab.ru",
    "category": "Technical",
    "version": "0.0.1",
    "depends": ["base", "web"],
    "external_dependencies": {"python": ["docxcompose", "docxtpl"]},
    "data": [
        "views/assets.xml",
        "views/ir_actions_report_views.xml",
    ],
}
