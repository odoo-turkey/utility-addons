# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Competitor Analysis",
    "summary": "Analyze your competitors",
    "version": "12.0.1.0.1",
    "category": "Tools",
    "website": "https://github.com/odoo-turkey",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["base", "queue_job"],
    "external_dependencies": {"python": ["usp.tree"]},
    "data": [
        "security/competitor_security.xml",
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "views/res_competitor_views.xml",
        "views/res_competitor_proxy_views.xml",
        "views/res_competitor_webpage_views.xml",
        "views/menus.xml",
        "views/assets.xml",
    ],
}
