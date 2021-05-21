# -*- coding: utf-8 -*-
{
    "name": "DOCX report",
    "summary": """
        Print docx report from docx template""",
    "description": """""",
    "author": "RYDLAB",
    "website": "http://rydlab.ru",
    "category": "Technical",
    "version": "0.0.1",
    "depends": ["base"],
    "external_dependencies": {"python": ["docxtpl", "num2words"]},
    "data": [
        "data/assets_extension.xml",
        "views/ir_actions_report_views.xml",
    ],
}
