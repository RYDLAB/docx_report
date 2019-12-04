# -*- coding: utf-8 -*-

from werkzeug import datastructures

from odoo import http


class ResPartnerContractBinary(http.Controller):

    @http.route('/web/binary/get_compiled_contract')
    def download_compiled_contract(self, doc_id, doc_name):
        contract_wizard = http.request.env['res.partner.contract.wizard'].sudo().browse(int(doc_id))
        file_content = contract_wizard.get_docx_contract_1().read()
        headers = datastructures.Headers()
        headers.add('Content-Disposition', 'attachment', filename=doc_name)
        return http.request.make_response(file_content, headers)
