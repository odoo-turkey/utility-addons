# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # Avoid using child_ids, as it is used by form view.
    org_chart_child_ids = fields.One2many(
        related="child_ids",
        string="Direct Subordinates",
    )
