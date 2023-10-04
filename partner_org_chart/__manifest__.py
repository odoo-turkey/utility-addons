# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Partner Organization Chart",
    "summary": "Organization chart on partner form",
    "license": "LGPL-3",
    "website": "https://github.com/odoo-turkey",
    "author": "Yigit Budak",
    "category": "CRM",
    "version": "1.0",
    "description": """
Org Chart Widget for Partners
=======================
Copied from hr_org_chart
This module extend the partner form with a organizational chart.
        """,
    "depends": ["base"],
    "data": [
        "views/partner_views.xml",
        "views/assets.xml",
    ],
    "qweb": [
        "static/src/xml/partner_org_chart.xml",
    ],
}
