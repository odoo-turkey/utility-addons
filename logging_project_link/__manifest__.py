# Copyright 2023 Samet Altuntaş (https://github.com/samettal)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Logging Project Link",
    "summary": "Provides linking logging with project with a button.",
    "author": "Samet Altuntaş, Odoo Turkey Localization Group",
    "website": "https://github.com/odoo-turkey/utility-addons",
    "license": "AGPL-3",
    "category": "",
    "version": "12.0.0.1.0",
    "depends": ["project"],
    "data": [
        "views/ir_logging_views.xml",
        "wizard/logging_project_link_view.xml",
        "views/project_views.xml",
    ],
    "installable": True,
}
