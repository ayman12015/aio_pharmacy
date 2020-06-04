# -*- coding: utf-8 -*-

from odoo import models, fields, api , _
from odoo.exceptions import UserError


class purchaseLineBatch(models.Model):
    _name = "purchase.order.line.batch"
    _order = "create_date desc"

    name = fields.Char(string="Batch",required=1)
    product_id = fields.Many2one('product.product',required=0)
    expiration_date = fields.Date(required=1)

    @api.constrains('name','product_id')
    def check_product_id(self):
        if not self.product_id:
            raise UserError(_("You Must Select Product First , Return To Previous Screen by click on Discard Button!!"))


class purchaseLine(models.Model):
    _inherit="purchase.order.line"

    batch = fields.Many2one('purchase.order.line.batch')
    #expiration_date =fields.Date()

    def _onchange_quantity(self):
        """
        To set cost price in product.product
        :return:
        """
        super(purchaseLine,self)._onchange_quantity()
        self.price_unit = self.product_id.standard_price

class purchase(models.Model):
    _inherit="purchase.order"

    partner_id =fields.Many2one('res.partner',default=47)
    journal_id = fields.Many2one('account.journal',required=1,domain=[('type','in',('cash','bank'))])
    user_id = fields.Many2one('res.users',readonly=1,default=lambda self:self._uid)
    # barcode_text = fields.Char(string="Barcode",size=15)
    #
    # @api.onchange('barcode_text')
    # def get_product_by_barcode(self):
    #     print(">>>>>>>>>>>>>>>>>",self.barcode_text)
    #     product = self.env['product.template'].search([('barcode','=',self.barcode_text)])
    #     if product:
    #         print(">>>>")
    #         self.barcode_text = ''

    @api.constrains('order_line')
    def check_order_have_line(self):
        if len(self.order_line) == 0:
            raise UserError(_("You Must at least select one product to purchase it"))


    def button_confirm(self):
        """"
        when click on confirm order must validate order and create picking and invoice automaticly
        """
        #I think function need more optimaization to make order done as fast as possible


        #trigger constraint
        self.check_order_have_line()

        super(purchase,self).button_confirm()

        #get created picking and use wizard to submit all Qty
        picking = self.env['stock.picking'].search([('origin','=',self.name)])

        #get all bathces here
        batches = []
        #expir_date = []
        qun = []
        for line in self.order_line:
            batches.append(line.batch)
            #expir_date.append(line.expiration_date)
            qun.append(line.product_qty)

        #to for loop batches one by one
        count = -1
        for line in picking.move_line_ids:

            count += 1

            # set it because it change to zero so we must reflect purchase qty to pickiing
            line.initial_demand = qun[count]

            if batches[count].name != False:
                lot = self.env['stock.production.lot']

                # serch if product have lot
                lot_search = lot.search([('product_id','=',line.product_id.id),('name','=',batches[count].name)])

                #if have lot created and selected from user then add qty to same lot else create new lot for product
                if lot_search:
                    lot_search.product_qty += qun[count]
                    line.lot_id = lot_search.id
                else:
                    line.lot_id = lot.with_context(active_picking_id=picking.id).create(
                    {
                        'product_id': line.product_id.id,
                        'name': batches[count].name
                    })
                    line.lot_id.removal_date = batches[count].expiration_date



        immediate_transfere =  self.env['stock.immediate.transfer'].create({

        })
        immediate_transfere.pick_ids = picking


        #picking validated and effect stock
        immediate_transfere.process()

        #create invoice to effect accounting
        invoice  = self.env['account.invoice'].create({
            'purchase_id':self.id,
            'origin':self.name,
            'partner_id':self.partner_id.id
        })
        #to active onchange to set products in invoice line automaticlly
        invoice.purchase_order_change()
        invoice.action_invoice_open()
        payment = self.env['account.payment'].with_context(invoice_ids=[(4, invoice.id, None)]).create({
            'invoice_ids': [(4, invoice.id, None)],
            'partner_type': 'supplier',
            'payment_date': self.date_order,
            'payment_token_id': False,
            'journal_id': self.journal_id.id,
            'partner_id': self.partner_id.id,
            'currency_id': 3,
            'writeoff_account_id': False,
            'communication': invoice.name,
            'amount': self.amount_total,
            'payment_method_id': 2,
            'payment_difference_handling': 'open',
            'writeoff_label': 'Write-Off',
            'payment_type': 'outbound'

        })

        {'invoice_ids':[(4, invoice.id, None)],
            'payment_type': 'outbound',
            'payment_method_id': 1,
            'amount': self.amount_total,
            'journal_id': self.journal_id.id,
            'partner_type': 'supplier',
            'partner_id': self.partner_id.id,
            'has_invoices': True,}

        """"""
        #TODO:Invoice not change to done(paid) after validate payment
        payment.action_validate_invoice_payment()
        invoice.state = 'paid'
        #invoice.residaul = 0
        self.invoice_ids = invoice
        self.invoice_count = 1
        self.state = 'done'
        #must set order to state done
        #self.state = 'done'


