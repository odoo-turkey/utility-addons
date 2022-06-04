# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Delivery Package Barcode',
    'summary': 'Provides fields to be able to use integration modules.',
    'author': 'Yiğit Budak, Odoo Turkey Localization Group',
    'website': 'https://github.com/odoo-turkey/utility-addons',
    'license': 'AGPL-3',
    'category': 'Delivery',
    'version': '12.0.1.1.0',
    'depends': ["barcodes", "stock", "delivery_integration_base"],
    'data': [
        'wizard/delivery_package_barcode_wiz_views.xml',
    ],
    'installable': True,
}
