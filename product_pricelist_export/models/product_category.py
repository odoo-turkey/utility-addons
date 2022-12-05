# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, fields, api, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    show_in_pricelist = fields.Boolean(string='Show in Pricelist')
    pricelist_discount_scales = fields.Char(string='Pricelist Discount Scales',
                                            help='Pricelist Discount Scales'
                                                 ' for this category. Example:'
                                                 ' 50,100,150,200,250')
