import io
from docxtpl import DocxTemplate


def get_document_from_values_stream(path_to_template: str, vals: dict):
    doc = DocxTemplate(path_to_template)
    doc.render(vals)
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream
