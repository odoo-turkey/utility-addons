# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product Pricelist Export",
    "summary": "Export pricelist as an excel file",
    "version": "12.0.1.0.1",
    "development_status": "Mature",
    "category": "Tools",
    "website": "https://github.com/yibudak",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product", "sale"
    ],
    "external_dependencies": {
        "python": ["xlsxwriter"]
    },
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "wizard/product_pricelist_export_wiz_view.xml",
        "views/product_category_views.xml",
    ],
}
