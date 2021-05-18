from odoo import models


class Utils(models.AbstractModel):
    _name = "client_contracts.utils"

    @staticmethod
    def to_fixed(number, digit=2):
        if isinstance(number, str) and number.isdigit():
            number = float(number)
        return f"{number:.{digit}f}"
