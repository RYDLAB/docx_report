import io

from docxtpl import DocxTemplate
from jinja2 import Environment as Jinja2Environment

from .num2words import num2words_, num2words_currency


def get_document_from_values_stream(path_to_template: str, vals: dict):
    doc = DocxTemplate(path_to_template)

    jinja_env = Jinja2Environment()

    functions = {
        "number2words": num2words_,
        "currency2words": num2words_currency,
    }
    jinja_env.globals.update(**functions)

    doc.render(vals, jinja_env)

    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)

    return file_stream
