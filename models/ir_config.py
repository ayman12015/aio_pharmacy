# -*- coding: utf-8 -*-

from odoo import models, fields, api , _
#from odoo.exceptions import UserError




class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_stock_production_lot = fields.Boolean("Lots & Serial Numbers", default=True,
                                                implied_group='stock.group_production_lot')

    module_product_expiry = fields.Boolean("Expiration Dates",default=True,
        help="Track following dates on lots & serial numbers: best before, removal, end of life, alert. \n Such dates are set automatically at lot/serial number creation based on values set on the product (in days).")
