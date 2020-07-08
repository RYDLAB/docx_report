from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    description_sale = fields.Text(
        "Sale Description",
        translate=True,
        help="A description of the Product that you want to communicate to your customers. "
        "This description will be copied to every Sales Order, Delivery Order and Customer Invoice/Credit Note",
    )
