from contextlib import contextmanager

from odoo import api, registry, SUPERUSER_ID
from odoo.tests import common


@contextmanager
def environment():
    """Return an environment with a new cursor for the current database; the
    cursor is committed and closed after the context block.
    """
    reg = registry(common.get_db_name())
    with reg.cursor() as cr:
        yield api.Environment(cr, SUPERUSER_ID, {})
