# -*- coding: utf-8 -*-

from odoo import models, fields, api


class productTemplate(models.Model):
    _inherit = 'product.template'


    @api.onchange('list_price')
    def onchange_purchase_price(self):
        self.standard_price = self.list_price / 1.2
