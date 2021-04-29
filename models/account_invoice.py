from odoo import models, _
from odoo.exceptions import UserError
from ..utils import MODULE_NAME


class AccountInvoice(models.Model):
    _inherit = "account.move"

    @staticmethod
    def check_contract_presence(sale_order_ids):
        error_message = ""
        if any(not so.contract_annex_id.contract_id for so in sale_order_ids):
            error_message = _("There is a Sale order without binding contract.")
        if any(not so.contract_annex_id  for so in sale_order_ids):
            error_message = _("There is a Sale order without annex.")
        if error_message:
            raise UserError(error_message)

    def action_invoice_print(self):
        '''
        for so in self.env["sale.order"].search([]):
            if self.id in so.invoice_ids.ids:
                order = so
                break
        else:
            return super().action_invoice_print()

        if not order.contract_annex_id or not order.contract_annex_id.contract_id:
            raise UserError(
                _(
                    "There is no binding contract. It is necessary to link the order with the annex to the contract."
                )
            )
        self.sent = True
        '''

        sale_orders_ids = self.env["sale.order"].search([
            ("invoice_ids", "in", self.ids)
        ])
        if not sale_orders_ids:
            return super().action_invoice_print()

        self.check_contract_presence(sale_orders_ids)
        self.filtered(lambda inv: not inv.is_move_sent).write({'is_move_sent': True})

        view = self.env.ref(
            "{}.res_partner_wizard_print_document_view".format(MODULE_NAME)
        )
        # annex = order.contract_annex_id
        return {
            "name": _("Print Form of Contract Annex"),
            "type": "ir.actions.act_window",
            "res_model": "res.partner.contract.wizard",
            "view_mode": "form",
            "view_id": view.id,
            "target": "new",
            "context": {
                # "self_id": annex.id,
                "active_ids": self.ids,
                "active_model": "res.partner.contract.annex",
                # "company_form": annex.partner_id.company_form
                # if annex.partner_id.is_company
                # else "person",
                "attachment_model": self._name,
                "attachment_res_id": self.id,
            },
        }
