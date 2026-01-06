# -*- coding: utf-8 -*-
# from odoo import http


# class AuthOauthProvider(http.Controller):
#     @http.route('/auth_oauth_provider/auth_oauth_provider', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/auth_oauth_provider/auth_oauth_provider/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('auth_oauth_provider.listing', {
#             'root': '/auth_oauth_provider/auth_oauth_provider',
#             'objects': http.request.env['auth_oauth_provider.auth_oauth_provider'].search([]),
#         })

#     @http.route('/auth_oauth_provider/auth_oauth_provider/objects/<model("auth_oauth_provider.auth_oauth_provider"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('auth_oauth_provider.object', {
#             'object': obj
#         })

