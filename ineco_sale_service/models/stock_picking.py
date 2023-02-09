# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _description = 'Stock Picking inherited'

    is_required_analytic_account = fields.Boolean(string='Required Analytic Account',
                                                  related='picking_type_id.is_required_analytic_account', store=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', default=False)
    is_post_cost = fields.Boolean(string='Post Cost', default=False)
    post_cost_date = fields.Date(string='Post Cost Date', default=False)
    product_string = fields.Char(string='List of Product', compute='_compute_product_string')

    def _compute_product_string(self):
        for data in self:
            data.product_string = ""
            tmp_string = ""
            for move in data.move_line_ids_without_package:
                tmp_string += "{} x {}".format(move.qty_done, move.product_id.name) + ", "
            if tmp_string:
                data.product_string = tmp_string[:-2]

    def post_costing(self):
        move_ids = []
        line_ids = []
        for rec in self:
            if rec.state != 'done' and not rec.is_post_cost:
                raise UserError(_('State must be Done and not Post Cost'))
            for move in rec.move_ids_without_package:
                move_ids.append(move.id)
            values = self.env['stock.valuation.layer'].search([('stock_move_id', 'in', move_ids)])
            amount = 0.00
            for value in values:
                amount += abs(value.value)
                line_ids.append((0,0,{
                    'name': "{} x {} ({})".format(abs(value.quantity), value.product_id.name, rec.name),
                    'account_id': rec.picking_type_id.debit_account_id.id,
                    'debit': abs(value.value),
                    'date': rec.scheduled_date,
                    'journal_id': rec.picking_type_id.journal_id.id,
                    'analytic_account_id': rec.analytic_account_id.id,
                }))
            if amount:
                line_ids.append((0,0,{
                    'name': rec.name,
                    'account_id': rec.picking_type_id.credit_account_id.id,
                    'credit': amount,
                    'date': rec.scheduled_date,
                    'journal_id': rec.picking_type_id.journal_id.id,
                }))
                new_account_move = {
                    'ref': rec.name,
                    'journal_id': rec.picking_type_id.journal_id.id,
                    'date': rec.scheduled_date,
                    'narration': '',
                    'line_ids': line_ids,
                }
                new_move = self.env['account.move'].create(new_account_move)
                new_move.action_post()
                rec.is_post_cost = True
                rec.post_cost_date = datetime.now().strftime('%Y-%m-%d')
        return True
