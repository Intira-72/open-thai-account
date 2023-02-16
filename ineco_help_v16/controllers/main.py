# -*- coding: utf-8 -*-
# Copyright (c) 2010 INECO PARTNERSHIP LIMITED (http://www.ineco.co.th)
# All Right Reserved

from odoo import http
from odoo.http import request


class HelpController(http.Controller):
    @http.route('/help/version', type='json', auth="none")
    def version_info(self):
        params = request.env['ir.config_parameter'].sudo().search([('key', '=', 'database.uuid')])
        return {'version': params.value}
