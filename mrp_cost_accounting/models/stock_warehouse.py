# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    waiting_cost_factor = fields.Float(string='Waiting Cost Factor',
                                       help='This field is used to calculate'
                                            ' MRP cost accounting. It is used'
                                            ' to calculate the cost of waiting'
                                            ' products in the warehouse.',
                                       default=10.0)
