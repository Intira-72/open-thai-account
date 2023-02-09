# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from collections import defaultdict


class ProjectProject(models.Model):
    _inherit = 'project.project'
    _description = 'Inherited Project'

    picking_ids = fields.Many2many('stock.picking', compute='_get_picking', string="Pickings")

    @api.depends()
    def _get_picking(self):
        self.picking_ids = False
        for data in self:
            pickings = self.env['stock.picking'].search([('analytic_account_id', '=', data.analytic_account_id.id)])
            if pickings:
                data.picking_ids = pickings
            else:
                data.picking_ids = False

    @api.depends('sale_line_id.product_uom_qty', 'sale_line_id.product_uom')
    def _compute_allocated_hours(self):
        sol_ids = self._fetch_sale_order_item_ids()
        for project in self:
            # project_id = project.id or project._origin.id
            order_line_item = self.env['sale.order.line.item'].search([('order_line_id', 'in', sol_ids)])
            qty = 0.00
            for line in order_line_item:
                qty += line.qty
            project.allocated_hours = qty
