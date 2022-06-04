# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp


class DeliveryPackageBarcodeWiz(models.TransientModel):
    _name = 'delivery.package.barcode.wiz'
    _inherit = 'barcodes.barcode_events_mixin'
    _description = 'Wizard to read barcode for delivery package'
    # To prevent remove the record wizard until 2 days old
    _transient_max_hours = 48
    _allowed_product_types = ['product', 'consu']

    @api.model
    def _default_auto_lot(self):
        return self.env.user.company_id.stock_barcodes_auto_lot

    message = fields.Char('Message', default='Scan a barcode', readonly=1)
    message_type = fields.Selection([('success', 'Success'), ('error', 'Error'),
                                     ('info', 'Info')], default='info')
    barcode = fields.Char()
    picking_id = fields.Many2one(
        comodel_name='stock.picking',
    )
    picking_line_ids = fields.Many2many('stock.move', string='Picking Lines')
    package_count = fields.Integer('Package Count')
    package_weight = fields.Float('Package Weight')

    @api.onchange('picking_id')
    def onchange_location_id(self):
        self.package_count = 0
        self.package_weight = 0.0

    def button_save(self):
        # TODO: FIXME
        self.picking_id.write({'carrier_package_count': self.package_count,
                               'picking_total_weight': self.package_weight})

    def process_barcode(self, barcode):
        pick_obj = self.env['stock.picking']

        if barcode and self.env.user.has_group('stock.group_stock_user'):
            domain = self._barcode_domain(barcode)
            picking = pick_obj.search(domain, limit=1)
            if picking:
                self.update({
                    'picking_id': picking.id,
                    'picking_line_ids': [(6, 0, picking.move_lines.ids)],
                    'message': _('Picking found:'),
                    'message_type': 'success',
                })
            else:
                self.update({
                    'message': _('Picking not found'),
                    'message_type': 'error',
                })
        return

    def _barcode_domain(self, barcode):
        return [('name', '=', barcode)]

    def on_barcode_scanned(self, barcode):
        self.barcode = barcode
        self.process_barcode(self.barcode)

