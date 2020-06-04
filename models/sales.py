# -*- coding: utf-8 -*-

from odoo import models, fields, api , _
from odoo.exceptions import UserError


class saleLine(models.Model):
    _inherit="sale.order.line"

    batch = fields.Many2one('purchase.order.line.batch')
    tracking = fields.Selection([('lot','Lot'),('serial','Serial'),('none','None')],related="product_id.tracking")

    @api.onchange('product_id')
    def get_product_batch(self):
        #if product have serial then get first batch near expiraion date
        if self.tracking in ('lot','serial'):

            batch = self.env['purchase.order.line.batch'].search([('product_id','=',self.product_id.id)],order="expiration_date")

            self.batch = batch[0]
            # for line in batch:
            #     self.batch = line
            #     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", line,line.id,line.expiration_date)
            #     break

class saleOrder(models.Model):
    _inherit = "sale.order"

    partner_id = fields.Many2one('res.partner', default=48)
    journal_id = fields.Many2one('account.journal', required=1, domain=[('type', 'in', ('cash', 'bank'))])
    #user_id = fields.Many2one('res.users', readonly=1, default=lambda self: self._uid)


    def action_confirm(self):

        super(saleOrder,self).action_confirm()

        # get created picking and use wizard to submit all Qty
        picking = self.env['stock.picking'].search([('origin', '=', self.name)])

        # get all bathces here
        batches = []
        # expir_date = []
        qun = []
        for line in self.order_line:
            batches.append(line.batch)
            # expir_date.append(line.expiration_date)
            qun.append(line.product_uom_qty)

        # to for loop batches one by one
        count = -1
        for line in picking.move_line_ids:

            count += 1

            # set it because it change to zero so we must reflect purchase qty to pickiing
            line.initial_demand = qun[count]

            if batches[count].name != False:
                lot = self.env['stock.production.lot']
                # serch if product have lot
                lot_search = lot.search([('product_id', '=', line.product_id.id), ('name', '=', batches[count].name)])
                # if have lot created and selected from user then add qty to same lot else create new lot for product
                line.lot_id = lot_search.id

                # # serch if product have lot
                # lot_search = lot.search([('product_id', '=', line.product_id.id), ('name', '=', batches[count].name)])
                #
                # # if have lot created and selected from user then add qty to same lot else create new lot for product
                # if lot_search:
                #     lot_search.product_qty += qun[count]
                #     print("/.>>>>>>>>>>>>>>>>>>>>>>>>>.",line.product_id,line.lot_id)
                #     line.lot_id = lot_search.id
                # else:
                #     line.lot_id = lot.with_context(active_picking_id=picking.id).create(
                #         {
                #              'product_id': line.product_id.id,
                #              'name': batches[count].name
                #          })
                #     line.lot_id.removal_date = batches[count].expiration_date

        immediate_transfere = self.env['stock.immediate.transfer'].create({

        })
        immediate_transfere.pick_ids = picking

        # picking validated and effect stock
        immediate_transfere.process()

        invoice_wizard = self.env['sale.advance.payment.inv'].with_context(active_ids=[self.id]).create({
            'advance_payment_method':'delivered'
        })

        invoice_wizard.create_invoices()

        invoice = self.env['account.invoice'].search([('origin','=',self.name)])
        invoice.action_invoice_open()

        #{'default_invoice_ids': [(4, active_id, None)]}

        payment = self.env['account.payment'].with_context({'default_invoice_ids': [(4, invoice.id, None)]}).create({
            'invoice_ids': [(4, invoice.id, None)],
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'payment_date': invoice.date_invoice,
            'journal_id': self.journal_id.id,
            'partner_id': self.partner_id.id,
            'currency_id': 3,
            #'writeoff_account_id': False,
            'communication': invoice.name,
            'amount': invoice.amount_total,
            'payment_method_id': 2,
            #'payment_difference_handling': 'open',
            #'writeoff_label': 'Write-Off',


        })

        payment.post()

        #if invoice.residual == 0:
        invoice.state = 'paid'
        self.state = 'done'

