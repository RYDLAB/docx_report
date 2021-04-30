from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    description_sale = fields.Text(
        "Sale Description",
        translate=True,
        help="A product's description you want to inform to your customers.\n"
        "This description will be copied to every Sales Order, Delivery Order and Customer Invoice/Credit Note",
    )
