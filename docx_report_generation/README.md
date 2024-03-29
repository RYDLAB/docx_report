# DOCX report
Functionality

Allows you to add docx files to the report model as a source template.
You can get reports based on such a template in docx or pdf format.
Currently, the simultaneous creation of multiple reports is not supported.

To convert docx -> pdf, an available gutenberg service is required on localhost:8808.
An example of launching a service in docker-compose next to Odoo:

```yaml
gotenberg:
    image: thecodingmachine/gotenberg:6
    restart: unless-stopped
    environment:
        LOG_LEVEL: INFO
        DEFAULT_LISTEN_PORT: 8808
        DISABLE_GOOGLE_CHROME: 1
        DEFAULT_WAIT_TIMEOUT: 30
        MAXIMUM_WAIT_TIMEOUT: 60
```

Creating a report

The report creates in the same way as the standard Odoo procedure:
1. In Settings -> Technical -> Reports, you need to create a new record. In the record of the report 
   choose one of the new types: "DOCX" or "DOCX(PDF)". 
   You do not need to fill in the "Template name" field, but instead download the docx file of the report. 
   All other fields are filled in the same as in standard Odoo reports.
2. If custom fields are applied in the report template, then you need to create them on the tab
   "Custom fields".
3. In the entry of the specified model, an additional item with the name of the created report will appear in the print menu. 
   Clicking on it will display a wizard in which you can check the values of custom fields before generating the report file.
4. When generating a report from the portal, the file is generated without displaying the wizard.


Templates creating

1. Templates can be created in any text editor that supports the docx format.
2. All formatting of the template is saved in the generated report.
3. Double curly braces are used to insert variables.
4. Access to the Odoo record for which the report generation is called is performed through the "docs" variable, 
   accessing attributes and methods as in Odoo: {{docs.attribute_name }}
5. It is possible to call the methods available for the entry in "docs", or passed to the context of the report.
6. By default, the report context contains methods of the "report_monetary_helper" module, which can be called directly by name.
7. Custom fields may also be present in the context of the report. 
   Such fields must be created in the report record. 
   In the template, custom fields are available by the name specified in the "tech_name" field of the custom field entry.
