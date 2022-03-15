from json import dumps as json_dumps, loads as json_loads
from logging import getLogger

from werkzeug.urls import url_decode

from odoo.http import (
    content_disposition,
    request,
    route,
    serialize_exception as _serialize_exception,
)
from odoo.tools import html_escape
from odoo.tools.safe_eval import safe_eval, time

from odoo.addons.web.controllers.main import ReportController

_logger = getLogger(__name__)


class DocxReportController(ReportController):
    @route()
    def report_routes(self, reportname, docids=None, converter=None, **data):
        """
        Запускает генерацию файла отчета и возвращает его
        """
        report = request.env["ir.actions.report"]._get_report_from_name(reportname)
        context = dict(request.env.context)
        _data = dict()
        if docids:
            _docids = [int(i) for i in docids.split(",")]
        if data.get("options"):
            _data.update(json_loads(data.pop("options")))
        if data.get("context"):
            # Ignore 'lang' here, because the context in data is the one from the webclient *but* if
            # the user explicitely wants to change the lang, this mechanism overwrites it.
            _data["context"] = json_loads(data["context"])
            if _data["context"].get("lang") and not _data.get("force_context_lang"):
                del _data["context"]["lang"]
            context.update(_data["context"])
        if converter == "docx":
            docx = report.with_context(context)._render_docx_docx(_docids, data=_data)
            docxhttpheaders = [
                (
                    "Content-Type",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                ),
                # ("Content-Length", len(docx)),
            ]
            return request.make_response(docx, headers=docxhttpheaders)
        elif converter == "pdf" and "docx" in report.report_type:
            pdf = report.with_context(context)._render_docx_pdf(_docids, data=_data)
            pdfhttpheaders = [
                (
                    "Content-Type",
                    "application/pdf",
                ),
                ("Content-Length", len(pdf[0])),
            ]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            return super().report_routes(
                reportname, docids=docids, converter=converter, **data
            )

    @route()
    def report_download(self, data, token, context=None):
        """
        Обрабатывает запрос на скачивание файла отчета
        """
        requestcontent = json_loads(data)
        url, type = requestcontent[0], requestcontent[1]
        try:
            if type in ["docx-docx", "docx-pdf"]:
                converter = "docx" if type == "docx-docx" else "pdf"
                extension = "docx" if type == "docx-docx" else "pdf"

                pattern = "/report/%s/" % ("docx" if type == "docx-docx" else "pdf")
                reportname = url.split(pattern)[1].split("?")[0]

                docids = None
                if "/" in reportname:
                    reportname, docids = reportname.split("/")

                if docids:
                    # Generic report:
                    response = self.report_routes(
                        reportname, docids=docids, converter=converter, context=context
                    )
                else:
                    # Particular report:
                    data = dict(
                        url_decode(url.split("?")[1]).items()
                    )  # decoding the args represented in JSON
                    if "context" in data:
                        context, data_context = json_loads(context or "{}"), json_loads(
                            data.pop("context")
                        )
                        context = json_dumps({**context, **data_context})
                    response = self.report_routes(
                        reportname, converter=converter, context=context, **data
                    )

                report = request.env["ir.actions.report"]._get_report_from_name(
                    reportname
                )
                filename = "%s.%s" % (report.name, extension)

                if docids:
                    ids = [int(x) for x in docids.split(",")]
                    obj = request.env[report.model].browse(ids)
                    if report.print_report_name and not len(obj) > 1:
                        report_name = safe_eval(
                            report.print_report_name, {"object": obj, "time": time}
                        )
                        filename = "%s.%s" % (report_name, extension)
                response.headers.add(
                    "Content-Disposition", content_disposition(filename)
                )
                response.set_cookie("fileToken", token)
                return response
            else:
                return super().report_download(data, token, context=context)
        except Exception as e:
            se = _serialize_exception(e)
            error = {"code": 200, "message": "Odoo Server Error", "data": se}
            return request.make_response(html_escape(json_dumps(error)))
