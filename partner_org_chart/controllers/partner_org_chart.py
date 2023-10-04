# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.exceptions import AccessError
from odoo.http import request


class PartnerOrgChartController(http.Controller):
    def _prepare_partner_data(self, active, partner):
        p_types = dict(partner._fields["type"].selection)
        partner_type = p_types.get(partner.type, partner.type)
        return dict(
            is_self=active.id == partner.id,
            id=partner.id,
            name=partner.display_name,
            link="/mail/view?model=res.partner&res_id=%s" % partner.id,
            partner_type=_(partner_type),
        )

    @http.route("/partner/get_org_chart", type="json", auth="user")
    def get_org_chart(self, partner_id):
        if not partner_id:  # to check
            return {}
        partner_id = int(partner_id)

        Partner = request.env["res.partner"]
        # check and raise
        if not Partner.check_access_rights("read", raise_exception=False):
            return {}
        try:
            Partner.browse(partner_id).check_access_rule("read")
        except AccessError:
            return {}
        else:
            active_partner = Partner.browse(partner_id)

        commercial_partner = active_partner.commercial_partner_id

        # Compute children
        def _compute_partner_tree(partner):
            partner_data = self._prepare_partner_data(active_partner, partner)
            child_data = [_compute_partner_tree(child) for child in partner.child_ids]
            return {
                "data": partner_data,
                "child_ids": child_data,
            }

        return _compute_partner_tree(commercial_partner)
