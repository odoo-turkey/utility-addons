odoo.define('web.PartnerOrgChart', function (require) {
"use strict";

var AbstractField = require('web.AbstractField');
var concurrency = require('web.concurrency');
var core = require('web.core');
var field_registry = require('web.field_registry');

var QWeb = core.qweb;
var _t = core._t;

var FieldOrgChart = AbstractField.extend({

    events: {
        // "click .o_partner_redirect": "_onpartnerRedirect",
        // "click .o_partner_sub_redirect": "_onpartnerSubRedirect",
    },
    /**
     * @constructor
     * @override
     */
    init: function () {
        this._super.apply(this, arguments);
        this.dm = new concurrency.DropMisordered();
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Get the chart data through a rpc call.
     *
     * @private
     * @param {integer} partner_id
     * @returns {Deferred}
     */
    _getOrgData: function (partner_id) {
        var self = this;
        return this.dm.add(this._rpc({
            route: '/partner/get_org_chart',
            params: {
                partner_id: partner_id,
            },
        })).then(function (data) {
            self.orgData = data;
        });
    },
    /**
     * @override
     * @private
     */
    _render: function () {
        if (!this.recordData.id) {
            return this.$el.html(QWeb.render("partner_org_chart", {
                managers: [],
                children: [],
            }));
        }

        var self = this;
        return this._getOrgData(this.recordData.id).then(function () {
            self.$el.html(QWeb.render("partner_org_chart", self.orgData));
            self.$('[data-toggle="popover"]').each(function () {
                $(this).popover({
                    html: true,
                    title: function () {
                        var $title = $(QWeb.render('hr_orgchart_emp_popover_title', {
                            partner: {
                                name: $(this).data('emp-name'),
                                id: $(this).data('emp-id'),
                            },
                        }));
                        $title.on('click',
                            '.o_partner_redirect', _.bind(self._onpartnerRedirect, self));
                        return $title;
                    },
                    container: 'body',
                    placement: 'left',
                    trigger: 'focus',
                    content: function () {
                        var $content = $(QWeb.render('hr_orgchart_emp_popover_content', {
                            partner: {
                                id: $(this).data('emp-id'),
                                name: $(this).data('emp-name'),
                                direct_sub_count: parseInt($(this).data('emp-dir-subs')),
                                indirect_sub_count: parseInt($(this).data('emp-ind-subs')),
                            },
                        }));
                        $content.on('click',
                            '.o_partner_sub_redirect', _.bind(self._onpartnerSubRedirect, self));
                        return $content;
                    },
                    template: QWeb.render('hr_orgchart_emp_popover', {}),
                });
            });
        });
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------
    //
    // /**
    //  * Redirect to the partner form view.
    //  *
    //  * @private
    //  * @param {MouseEvent} event
    //  * @returns {Deferred} action loaded
    //  */
    // _onpartnerRedirect: function (event) {
    //     event.preventDefault();
    //     var partner_id = parseInt($(event.currentTarget).data('partner-id'));
    //     return this.do_action({
    //         type: 'ir.actions.act_window',
    //         view_type: 'form',
    //         view_mode: 'form',
    //         views: [[false, 'form']],
    //         target: 'current',
    //         res_model: 'hr.partner',
    //         res_id: partner_id,
    //     });
    // },
    // /**
    //  * Redirect to the sub partner form view.
    //  *
    //  * @private
    //  * @param {MouseEvent} event
    //  * @returns {Deferred} action loaded
    //  */
    // _onpartnerSubRedirect: function (event) {
    //     event.preventDefault();
    //     var partner_id = parseInt($(event.currentTarget).data('partner-id'));
    //     var partner_name = $(event.currentTarget).data('partner-name');
    //     var type = $(event.currentTarget).data('type') || 'direct';
    //     var domain = [['parent_id', '=', partner_id]];
    //     var name = _.str.sprintf(_t("Direct Subordinates of %s"), partner_name);
    //     if (type === 'total') {
    //         domain = ['&', ['parent_id', 'child_of', partner_id], ['id', '!=', partner_id]];
    //         name = _.str.sprintf(_t("Subordinates of %s"), partner_name);
    //     } else if (type === 'indirect') {
    //         domain = ['&', '&',
    //             ['parent_id', 'child_of', partner_id],
    //             ['parent_id', '!=', partner_id],
    //             ['id', '!=', partner_id]
    //         ];
    //         name = _.str.sprintf(_t("Indirect Subordinates of %s"), partner_name);
    //     }
    //     if (partner_id) {
    //         return this.do_action({
    //             name: name,
    //             type: 'ir.actions.act_window',
    //             view_mode: 'kanban,list,form',
    //             views: [[false, 'kanban'], [false, 'list'], [false, 'form']],
    //             target: 'current',
    //             res_model: 'hr.partner',
    //             domain: domain,
    //         });
    //     }
    // },
});

field_registry.add('partner_org_chart', FieldOrgChart);

return FieldOrgChart;

});
