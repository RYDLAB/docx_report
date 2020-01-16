import datetime as dt

from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class Extension(object):

    def parse_odoo_date(self, date: str):
        return dt.datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)

    def parse_odoo_datetime(self, datetime: str):
        return dt.datetime.strptime(datetime, DEFAULT_SERVER_DATETIME_FORMAT)
