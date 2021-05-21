import io
from collections import OrderedDict
from jinja2 import Environment as Jinja2Environment
from logging import getLogger

from docxcompose.composer import Composer
from docx import Document
from docxtpl import DocxTemplate

from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import AccessError, UserError
from odoo.sql_db import TestCursor
from odoo.tools.safe_eval import safe_eval, time

from ..utils.num2words import num2words_, num2words_currency

_logger = getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = "ir.actions.actions"

    report_name = fields.Char(required=False)
    report_type = fields.Selection(
        selection_add=[("docx-docx", "DOCX")], ondelete="cascade"
    )
    report_docx_template = fields.Binary(
        string="Report docx template",
    )

    def _render_docx_docx(self, res_ids=None, data=None):
        if not data:
            data = {}
        data.setdefault("report_type", "docx")

        # access the report details with sudo() but evaluation context as current user
        self_sudo = self.sudo()

        save_in_attachment = OrderedDict()
        # Maps the streams in `save_in_attachment` back to the records they came from
        stream_record = dict()
        if res_ids:
            Model = self.env[self_sudo.model]
            record_ids = Model.browse(res_ids)
            docx_record_ids = Model
            if self_sudo.attachment:
                for record_id in record_ids:
                    attachment = self_sudo.retrieve_attachment(record_id)
                    if attachment:
                        stream = self_sudo._retrieve_stream_from_attachment(attachment)
                        save_in_attachment[record_id.id] = stream
                        stream_record[stream] = record_id
                    if not self_sudo.attachment_use or not attachment:
                        docx_record_ids += record_id
            else:
                docx_record_ids = record_ids
            res_ids = docx_record_ids.ids

        if save_in_attachment and not res_ids:
            _logger.info("The DOCS report has been generated from attachments.")
            return self_sudo._post_docx(save_in_attachment), "docx"

        template = self.report_docx_template
        template_path = template._full_path(template.store_fname)

        doc = DocxTemplate(template_path)

        jinja_env = Jinja2Environment()

        functions = {
            "number2words": num2words_,
            "currency2words": num2words_currency,
        }
        jinja_env.globals.update(**functions)

        doc.render(data, jinja_env)

        docx_content = io.BytesIO()
        doc.save(docx_content)
        docx_content.seek(0)

        if res_ids:
            _logger.info(
                "The DOCS report has been generated for model: %s, records %s."
                % (self_sudo.model, str(res_ids))
            )
            return (
                self_sudo._post_docx(
                    save_in_attachment, docx_content=docx_content, res_ids=res_ids
                ),
                "docx",
            )
        return docx_content, "docx"

    def _post_docx(self, save_in_attachment, docx_content=None, res_ids=None):
        def close_streams(streams):
            for stream in streams:
                try:
                    stream.close()
                except Exception:
                    pass

        if len(save_in_attachment) == 1 and not docx_content:
            return list(save_in_attachment.values())[0].getvalue()

        streams = []

        if docx_content:
            # Build a record_map mapping id -> record
            record_map = {
                r.id: r
                for r in self.env[self.model].browse(
                    [res_id for res_id in res_ids if res_id]
                )
            }

            # If no value in attachment or no record specified, only append the whole docx.
            if not record_map or not self.attachment:
                streams.append(docx_content)
            else:
                if len(res_ids) == 1:
                    # Only one record, so postprocess directly and append the whole docx.
                    if (
                        res_ids[0] in record_map
                        and not res_ids[0] in save_in_attachment
                    ):
                        new_stream = self._postprocess_docx_report(
                            record_map[res_ids[0]], docx_content
                        )
                        # If the buffer has been modified, mark the old buffer to be closed as well.
                        if new_stream and new_stream != docx_content:
                            close_streams([docx_content])
                            docx_content = new_stream
                    streams.append(docx_content)
                else:
                    streams.append(docx_content)

        if self.attachment_use:
            for stream in save_in_attachment.values():
                streams.append(stream)

        if len(streams) == 1:
            result = streams[0].getvalue()
        else:
            try:
                result = self._merge_docx(streams)
            except Exception:
                raise UserError(_("One of the documents, you try to merge is fallback"))

        close_streams(streams)
        return result

    def _postprocess_docx_report(self, record, buffer):
        attachment_name = safe_eval(self.attachment, {"object": record, "time": time})
        if not attachment_name:
            return None
        attachment_vals = {
            "name": attachment_name,
            "raw": buffer.getvalue(),
            "res_model": self.model,
            "res_id": record.id,
            "type": "binary",
        }
        try:
            self.env["ir.attachment"].create(attachment_vals)
        except AccessError:
            _logger.info(
                "Cannot save DOCX report %r as attachment", attachment_vals["name"]
            )
        else:
            _logger.info(
                "The DOCX document %s is now saved in the database",
                attachment_vals["name"],
            )
        return buffer

    def _merge_docx(self, streams):
        writer = Document()
        composer = Composer(writer)
        for stream in streams:
            reader = Document(stream)
            composer.append(reader)
        return composer.getvalue()
