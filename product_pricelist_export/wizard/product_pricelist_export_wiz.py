# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from io import BytesIO
from base64 import b64encode
import xlsxwriter


class ProductPricelistExportWiz(models.TransientModel):
    _name = 'product.pricelist.export.wiz'
    _description = 'Product Pricelist Export Wizard'

    product_categ_id = fields.Many2one('product.category',
                                       string='Product Category')
    # Todo: many2many yap
    pricelist_id = fields.Many2one('product.pricelist',
                                   string='Pricelist', required=True)

    def action_export(self):
        self.ensure_one()
        categ_name = self.product_categ_id.name
        pricelist_name = self.pricelist_id.name
        currency_name = self.pricelist_id.currency_id.name
        products = self._get_products()
        rules = self._get_price_rules()
        fl = BytesIO()
        workbook = xlsxwriter.Workbook(fl)
        worksheet = workbook.add_worksheet(_(pricelist_name))
        self._write_header(workbook, worksheet)
        rules_header = self._write_rules_header(workbook, worksheet, rules)

        for idx, product in enumerate(products):
            worksheet.write(idx + 1, 0, idx + 1)
            worksheet.write(idx + 1, 1, product.default_code)
            worksheet.write(idx + 1, 2, product.attr_price)
            worksheet.write(idx + 1, 3, currency_name)
            worksheet.write(idx + 1, 4, categ_name)
            for rule in rules_header:
                product_price = product.attr_price * (1 - rule['discount']/100)
                product_price = round(product_price, 2)
                worksheet.write(idx + 1, rule['first_column'], rule['min_qty'])
                worksheet.write(idx + 1, rule['first_column'] + 1, rule['discount'])
                worksheet.write(idx + 1, rule['first_column'] + 2, product_price) # Todo fix price calc

        # get base url
        workbook.close()
        fl.seek(0)
        fl_b64 = b64encode(fl.read())
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        attachment_obj = self.env['ir.attachment']
        # create attachment
        attachment_id = attachment_obj.create(
            {'name': "name", 'datas_fname': 'deneme.xlsx', 'datas': fl_b64})
        # prepare download url
        download_url = '/web/content/' + str(
            attachment_id.id) + '?download=true'
        # download
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }

    def _write_header(self, workbook, worksheet):
        """
        Writes header to the worksheet
        Fields:
        Product Code, Product Name, Price, Price Currency, Product Category
        """
        bold = workbook.add_format({'bold': True})
        worksheet.set_column('A:A', 10)
        worksheet.write('A1', _('Sequence'), bold)
        worksheet.set_column('B:B', 25)
        worksheet.write('B1', _('Product Code'), bold)
        worksheet.set_column('C:C', 15)
        worksheet.write('C1', _('Standard Price'), bold)
        worksheet.set_column('D:D', 10)
        worksheet.write('D1', _('Currency'), bold)
        worksheet.set_column('E:E', 25)
        worksheet.write('E1', _('Category Name'), bold)
        return True

    def _write_rules_header(self, workbook, worksheet, rules):
        """
        Writes price rules to the worksheet
        """
        bold = workbook.add_format({'bold': True})
        column_list = []
        col = 5  # start from column F
        for rule in rules:
            worksheet.set_column(col, col, 15)
            worksheet.write(0, col, _('Quantity'), bold)
            worksheet.set_column(col + 1, col + 1, 15)
            worksheet.write(0, col + 1, _('Discount %'), bold)
            worksheet.set_column(col + 2, col + 2, 15)
            worksheet.write(0, col + 2, _('Unit Price'), bold)
            column_list.append({
                'first_column': col,
                'min_qty': rule.min_quantity,
                'discount': rule.price_discount,
            })
            col += 3
        return column_list

    def _get_price_rules(self):
        """
        Returns price rules according to the selected pricelist. It also sorts
        the rules according to the quantity.
        """
        rules = self.env['product.pricelist.item'].search([
            ('pricelist_id', '=', self.pricelist_id.id),
            ('categ_id', '=', self.product_categ_id.id),
            ('applied_on', '=', '2_product_category'),
            ('price_discount', '!=', 0.0),
        ])

        if not rules:
            raise ValidationError(_('There is no price rule in this category'))

        return rules.sorted(key=lambda r: r.min_quantity)

    def _get_products(self):
        """
        Returns products according to the selected category. If no category
        selected, returns all products. # Todo
        """
        products = self.env['product.product'].search([
            ('categ_id', '=', self.product_categ_id.id),
            ('sale_ok', '=', True),
            ('attr_price', '=', 0.0) # Todo: maybe delete this
        ])
        if not products:
            raise ValidationError(_('There is no product in this category'))
        return products
