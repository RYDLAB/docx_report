# DOCS report
Adds docx reports printing from docx templates like standard Odoo reports
with qweb templates. Standard Odoo reports also available.

For generating pdf from docx external service the "gotenberg" is used.
It should work at the same server as Odoo app. If "gotenberg" absent, there
will be only reports in docx format.

To get and start "gotenberg" container use command:
docker run -h docx_to_pdf -e DEFAULT_LISTEN_PORT=8808 thecodingmachine/gotenberg
