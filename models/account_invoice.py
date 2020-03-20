from odoo import models, _
from odoo.exceptions import UserError
from ..utils import MODULE_NAME


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def invoice_print(self):
        self.ensure_one()
        for so in self.env["sale.order"].search([]):
            if self.id in so.invoice_ids.ids:
                order = so
                break
        else:
            return super().invoice_print()

        if not order.contract_annex_id or not order.contract_annex_id.contract_id:
            raise UserError(
                _(
                    "There is no binding contract. It is necessary to link the order with the annex to the contract."
                )
            )

        self.sent = True

        view = self.env.ref(
            "{}.res_partner_wizard_print_document_view".format(MODULE_NAME)
        )
        return {
            "name": _("Print Form of Contract Annex"),
            "type": "ir.actions.act_window",
            "res_model": "res.partner.contract.wizard",
            "view_mode": "form",
            "view_id": view.id,
            "target": "new",
            "context": {
                "self_id": order.contract_annex_id.id,
                "active_model": "res.partner.contract.annex",
                "attachment_model": self._name,
                "attachment_res_id": self.id
            },
        }
