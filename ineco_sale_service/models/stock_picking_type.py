# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'
    _description = 'Operation Type inherited'

    is_required_analytic_account = fields.Boolean(string='Required Analytic Account', default=False)
    debit_account_id = fields.Many2one('account.account', string='Debit')
    credit_account_id = fields.Many2one('account.account', string='Credit')
    journal_id = fields.Many2one('account.journal', string='Journal')
