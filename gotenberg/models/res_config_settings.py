# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_gotenberg = fields.Boolean(string="Gotenberg")
    server = fields.Char(
        string="Server",
        config_parameter="service.gotenberg_server",
    )
    method_authentication = fields.Selection(
        [
            ("none", "None"),
            ("basic", "Basic Authentication"),
        ],
        default="none",
        config_parameter="service.gotenberg_method_authentication",
    )
    username = fields.Char(
        string="Username", config_parameter="service.gotenberg_username"
    )
    password = fields.Char(
        string="Password", config_parameter="service.gotenberg__password"
    )
