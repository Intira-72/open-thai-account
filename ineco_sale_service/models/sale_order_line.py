# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = 'Service order line'

    manday = fields.Integer(string='Man Days', default=1)
    line_item_ids = fields.One2many('sale.order.line.item', 'order_line_id', string='@ Items', copy=True)
    line_day_ids = fields.One2many('sale.order.line.day', 'order_line_id', string='@ Days', copy=True)
    line_project_ids = fields.One2many('sale.order.line.project', 'order_line_id', string='@ Project', copy=True)
    assigned_id = fields.Many2one('res.users', string='Assign To')
    assigned_ids = fields.Many2many('res.users', 'sale_order_line_users_rel', 'sale_line_id', 'user_id',
                                    string='Assign To')

    @api.onchange('line_item_ids', 'line_day_ids', 'line_project_ids', 'manday')
    def _change_price_unit(self):
        for line in self:
            line.price_unit = sum(line.line_item_ids.mapped('price_subtotal')) + (sum(
                line.line_day_ids.mapped('price_unit')) * line.manday or 1.0) + sum(
                line.line_project_ids.mapped('price_unit'))

    def _timesheet_create_task_prepare_values(self, project):
        self.ensure_one()
        planned_hours = self._convert_qty_company_hours(self.company_id)
        sale_line_name_parts = self.name.split('\n')
        title = sale_line_name_parts[0] or self.product_id.name
        description = '<br/>'.join(sale_line_name_parts[1:])
        return {
            'name': title if project.sale_line_id else '%s: %s' % (self.order_id.name or '', title),
            'planned_hours': planned_hours,
            'partner_id': self.order_id.partner_id.id,
            'email_from': self.order_id.partner_id.email,
            'description': description,
            'project_id': project.id,
            'sale_line_id': self.id,
            'sale_order_id': self.order_id.id,
            'company_id': project.company_id.id,
            'user_ids': self.assigned_ids,
        }

    def _convert_qty_company_hours(self, dest_company):
        company_time_uom_id = dest_company.project_time_mode_id
        planned_hours = 0.00
        for data in self:
            for line in data.line_item_ids:
                if line.uom_id == company_time_uom_id:
                    planned_hours += line.qty
        if planned_hours:
            return planned_hours
        else:
            if self.product_uom.id != company_time_uom_id.id and self.product_uom.category_id.id == company_time_uom_id.category_id.id:
                planned_hours = self.product_uom._compute_quantity(self.product_uom_qty, company_time_uom_id)
            else:
                planned_hours = self.product_uom_qty
        return planned_hours


class SaleOrderLineItem(models.Model):
    _name = 'sale.order.line.item'
    _description = 'Line Item'

    name = fields.Char(string='Description')
    order_line_id = fields.Many2one('sale.order.line', string='Order Line')
    product_id = fields.Many2one('product.product', string='Product')
    qty = fields.Integer(string='Quantity', default=1)
    price_unit = fields.Float(string='Unit Price')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_price_subtotal', store=True, digits=(12, 2))

    @api.depends('qty', 'price_unit')
    def _compute_price_subtotal(self):
        for data in self:
            data.price_subtotal = data.qty * data.price_unit

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.price_unit = self.product_id.lst_price
            self.uom_id = self.product_id.uom_id.id


class SaleOrderLineDay(models.Model):
    _name = 'sale.order.line.day'
    _description = 'Day Item'

    name = fields.Char(string='Description')
    order_line_id = fields.Many2one('sale.order.line', string='Order Line')
    product_id = fields.Many2one('product.product', string='Product')
    price_unit = fields.Float(string='Unit Price')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.price_unit = self.product_id.lst_price
            self.uom_id = self.product_id.uom_id.id


class SaleOrderLineProject(models.Model):
    _name = 'sale.order.line.project'
    _description = 'Project Item'

    name = fields.Char(string='Description')
    order_line_id = fields.Many2one('sale.order.line', string='Order Line')
    product_id = fields.Many2one('product.product', string='Product')
    price_unit = fields.Float(string='Unit Price')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.price_unit = self.product_id.lst_price
            self.uom_id = self.product_id.uom_id.id
