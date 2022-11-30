# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'MRP Cost Accounting',
    'summary': 'Cost accounting for MRP, Sales, Purchases, Invoices',
    'version': '12.0.1.0.0',
    'development_status': 'Beta',
    'category': 'mrp',
    'website': 'https://github.com/odoo-turkey',
    'author': 'Yiğit Budak, Odoo Turkey',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'purchase', 'mrp', 'sale', 'stock', 'account', 'mrp_bom_cost'
    ],
    'data': [
        'view/stock_warehouse_view.xml',
        'view/product_view.xml',
    ],
    'post_init_hook': 'compute_total_quant_cost',
}
