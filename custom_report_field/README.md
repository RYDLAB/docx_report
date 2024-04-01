# Custom report values
Adds custom computed fields for reports.
Adds new tab with custom fields in report form, where custom fields can be
created. Here is possible to write python code block for computing
field's values, and this fields with computed values vill be accessible in report
template.

Also adds wizard where custom fields values can be validated before report creation.
If it is required to change some value, it shoud be changed in record where it stored.

Fields in Custom Field creation form:
"name": Name for showing in interface.
"tech_name": by this literal field's value can be accessed in templates.
"required": If value can't be empty, in fact it must be equivalent to True.
"visible": Will this field be showed in validation wizard or not.
"Description": Text field storing info for users.
"Computing field's value" tab: Place for input python code computing field's value.
        Help about code writing can be found in neighbour "Help" tab.
