import re
import os
from .environment import environment


GOTENBERG_DEFAULT_SERVER = "localhost:3000"
CONVERT_PDF_FROM_OFFICE_PATH = "convert/office"
HOST_PATTERN = re.compile(r"https?://(www\.)?")


def get_hostname(server):
    return HOST_PATTERN.sub("", server).strip().strip("/")


def _gotenberg_server() -> str:
    env_value = os.environ.get("GOTENBERG_SERVER")

    with environment() as env:
        param_value = (
            env["ir.config_parameter"].sudo().get_param("service.gotenberg_server")
        )
        server = env_value if env_value else param_value

        return server if server else GOTENBERG_DEFAULT_SERVER


def convert_pdf_from_office_url() -> str:
    return _gotenberg_server() + CONVERT_PDF_FROM_OFFICE_PATH


def get_auth():
    with environment() as env:
        conf = env["ir.config_parameter"].sudo()
        auth = conf.get_param("service.gotenberg_method_authentication")

        if auth == "basic":
            username = conf.get_param("service.gotenberg_username")
            password = conf.get_param("service.gotenberg__password")
            return username, password

        return


def check_gotenberg_installed():
    with environment() as env:
        gotenberg_rec = (
            env["ir.module.module"].sudo().search([("name", "=", "gotenberg")])
        )
        return (
            True
            if gotenberg_rec and gotenberg_rec.sudo().state == "installed"
            else False
        )
