# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class AccountAccount(models.Model):
    _inherit = 'account.account'
    _order = 'code'

    parent_id = fields.Many2one('account.account', string='Parent')
    # name2 = fields.Char(string=u'Secondary Name', copy=False, tracking=True)
    # tax_sale_ok = fields.Boolean(string=u'ภาษีขาย', copy=False, tracking=True)
    # tax_purchase_ok = fields.Boolean(string=u'ภาษีซื้อ', copy=False, tracking=True)
    # cheque_in_ok = fields.Boolean(string=u'เช็ครับ', copy=False, tracking=True)
    # cheque_out_ok = fields.Boolean(string=u'เช็คจ่าย', copy=False, tracking=True)
    # deposit_ok = fields.Boolean(string=u'มัดจำ', copy=False, tracking=True)
    # wht_purchase_ok = fields.Boolean(string=u'ภาษีหัก ณ ที่จ่าย', copy=False, tracking=True)
    # wht_sale_ok = fields.Boolean(string=u'ภาษีถูกหัก ณ ที่จ่าย', copy=False, tracking=True)
    # wait = fields.Boolean(string=u'ภาษีซื้อรอนำส่ง', copy=False, tracking=True)
    # tax_sale_wait = fields.Boolean(string=u'ภาษีขายรอนำส่ง', copy=False, tracking=True)

    account_type = fields.Selection(selection_add=[('view', 'View')], ondelete={'view': 'cascade'})
    internal_group = fields.Selection(selection_add=[('view', 'View')], ondelete={'view': 'cascade'})

    def name_get(self):
        result = []
        for account in self:
            show_code = self._context.get('show_code', False)
            if show_code:
                name = account.code
            else:
                name = account.code + ' ' + account.name
            result.append((account.id, name))
        return result
