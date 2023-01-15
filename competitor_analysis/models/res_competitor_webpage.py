# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, _


class ResCompetitorWebPage(models.Model):
    _name = "res.competitor.webpage"
    _description = "Competitor Analysis Webpages"

    _sql_constraints = [
        (
            "url_competitor_unique",
            "UNIQUE(name, competitor_id)",
            _("The URL must be unique for each competitor. "),
        )
    ]

    name = fields.Char(
        string="Name",
        help="Crawled web page URL",
    )
    competitor_id = fields.Many2one(
        string="Competitor",
        comodel_name="res.competitor",
        required=True,
        readonly=True,
    )
    first_seen = fields.Date(
        string="First Seen",
        readonly=True,
    )
    last_seen = fields.Date(
        string="Last Seen",
        readonly=True,
    )
