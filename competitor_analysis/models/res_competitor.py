# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api, _
from usp.tree import sitemap_tree_for_homepage


class ResCompetitor(models.Model):
    _name = "res.competitor"
    _description = "Competitor Analysis"

    @api.depends("crawled_urls")
    def _compute_crawled_url_count(self):
        """
        Compute total number of crawled urls for each competitor
        :return: Total number of crawled urls
        """
        for rec in self:
            rec.crawled_url_count = len(rec.crawled_urls)

    name = fields.Char(string="Name")
    website_url = fields.Char(
        string="Website URL",
        required=True,
        help="Example: https://www.example.com",
    )
    crawling_active = fields.Boolean(
        string="Crawling Active",
        default=False,
    )
    crawled_urls = fields.One2many(
        string="Crawled URLs",
        comodel_name="res.competitor.webpage",
        inverse_name="competitor_id",
    )
    crawled_url_count = fields.Integer(
        string="Crawled URL Count",
        compute="_compute_crawled_url_count",
        store=True,
    )
    last_crawled = fields.Date(
        string="Last Crawled",
        readonly=True,
    )

    @api.multi
    def unlink(self):
        """
        Delete all related records when competitor is deleted
        :return: super()
        """
        for rec in self:
            rec.crawled_urls.unlink()
        return super(ResCompetitor, self).unlink()

    @api.model
    def _action_crawl_competitors(self, domain=None):
        """
        Multi action for crawl the website and save the urls to the database
        :return: None
        """
        domain = domain or [("crawling_active", "=", True)]
        competitors = self.search(domain)
        for rec in competitors:
            rec.do_crawling()

    def do_crawling(self):
        """
        Start crawling the website
        :return: bool
        """
        self.ensure_one()
        date_now = fields.Date.today()
        WebPageModel = self.env["res.competitor.webpage"]
        create_list = []
        tree = sitemap_tree_for_homepage(self.website_url)
        cleaned_pages = self._clean_duplicate_urls(tree.all_pages())
        for page in cleaned_pages:
            vals = {
                "last_seen": date_now,
                "name": page.url,
            }
            website_record = WebPageModel.search(
                [
                    ("name", "=", page.url),
                    ("competitor_id", "=", self.id),
                ],
            )
            if website_record:
                website_record.write(vals)
            else:
                create_list.append(
                    {
                        **vals,
                        "competitor_id": self.id,
                        "first_seen": date_now,
                    }
                )
        # Create new records
        if create_list:
            WebPageModel.create(create_list)

        # Update last crawled date
        self.last_crawled = date_now
        return True

    def _clean_duplicate_urls(self, pages):
        """
        Clean duplicate urls
        :param pages: List of pages model
        :return: Generator of pages without duplicates
        """
        self.ensure_one()
        unique_urls = {}
        for page in pages:
            if page.url not in unique_urls:
                unique_urls[page.url] = page
        return unique_urls.values()

    def action_open_crawled_urls(self):
        """
        Open the crawled urls
        :return: Action
        """
        self.ensure_one()
        action = self.env.ref(
            "competitor_analysis.action_res_competitor_webpage"
        ).read()[0]
        action["domain"] = [("competitor_id", "=", self.id)]
        return action
