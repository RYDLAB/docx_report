{
    "name": "Custom report field",
    "summary": """Creates custom computed fields for reports""",
    "description": """
        Adds custom computed fields for reports.
        Adds new tab with custom fields in report form, where custom fields can be
        created. Here is possible write some python code for computing field's value,
        and this field with computed value vill be accessible in report template.

        Also adds wizard where custom fields values can be validated before report
        creation.
    """,
    "author": "RYDLAB",
    "website": "http://rydlab.ru",
    "category": "Technical",
    "version": "14.0.0.0.1",
    "depends": ["base", "web", "report_monetary_helpers"],
    "data": [
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/ir_actions_report_views.xml",
        "wizard/custom_report_field_values_wizard_views.xml",
    ],
}
