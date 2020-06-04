# -*- coding: utf-8 -*-
from odoo import http

# class AioPharmacy(http.Controller):
#     @http.route('/aio_pharmacy/aio_pharmacy/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aio_pharmacy/aio_pharmacy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('aio_pharmacy.listing', {
#             'root': '/aio_pharmacy/aio_pharmacy',
#             'objects': http.request.env['aio_pharmacy.aio_pharmacy'].search([]),
#         })

#     @http.route('/aio_pharmacy/aio_pharmacy/objects/<model("aio_pharmacy.aio_pharmacy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aio_pharmacy.object', {
#             'object': obj
#         })