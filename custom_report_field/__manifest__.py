{
    "name": "Custom report field",
    "summary": """Creates custom computed fields for reports""",
    "description": """
        Adds custom computed fields for reports.
        Adds new tab with custom fields in report form, where custom fields can be
        created. Here is possible write some python code for computing field's value,
        and this field with computed value will be accessible in report template.

        Also adds wizard where custom fields values can be validated before report
        creation.
    """,
    "author": "RYDLAB",
    "website": "https://rydlab.ru",
    "category": "Technical",
    "version": "16.0.1.0.2",
    "license": "LGPL-3",
    "depends": ["base", "web", "report_monetary_helpers"],
    "data": [
        "security/ir.model.access.csv",
        "views/ir_actions_report_views.xml",
        "wizard/custom_report_field_values_wizard_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "custom_report_field/static/src/js/action_manager_report.js",
        ],
    },
}
