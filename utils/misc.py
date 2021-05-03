import datetime as dt

# import inspect

from odoo import models  # , fields
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


'''class IDocument(object):
    """Class must be used as an interface for create new document based model"""

    def get_name_by_document_template(self, document_template_id: fields.Many2one):
        raise NotImplementedError(
            "Method {} is not implemented".format(inspect.currentframe().f_code.co_name)
        )

    def get_filename_by_document_template(self, document_template_id: fields.Many2one):
        raise NotImplementedError(
            "Method {} is not implemented".format(inspect.currentframe().f_code.co_name)
        )'''


class Utils(models.AbstractModel):
    _name = "client_contracts.utils"

    '''@staticmethod
    def parse_odoo_date(date: str):
        return dt.datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)

    @staticmethod
    def parse_odoo_datetime(datetime: str):
        return dt.datetime.strptime(datetime, DEFAULT_SERVER_DATETIME_FORMAT)'''

    @staticmethod
    def to_fixed(number, digit=2):
        if isinstance(number, str) and number.isdigit():
            number = float(number)
        return format(number, ".{digit}f".format(digit=digit))
