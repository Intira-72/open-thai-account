# -*- coding: utf-8 -*-

from odoo.exceptions import AccessError
from odoo import api, fields, models, _
from odoo import SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
from odoo.http import request
from odoo.addons.account.models.account_tax import TYPE_TAX_USE

import logging


class AccountAccountTemplate(models.Model):
    _inherit = "account.account.template"

    parent_id = fields.Many2one('account.account.template', string='Parent')
    account_type = fields.Selection(selection_add=[('view', 'View')])


class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    def generate_account(self, tax_template_ref, acc_template_ref, code_digits, company):
        """ This method generates accounts from account templates.

        :param tax_template_ref: Taxes templates reference for write taxes_id in account_account.
        :param acc_template_ref: dictionary containing the mapping between the account templates and generated accounts (will be populated)
        :param code_digits: number of digits to use for account code.
        :param company_id: company to generate accounts for.
        :returns: return acc_template_ref for reference purpose.
        :rtype: dict
        """
        self.ensure_one()
        account_tmpl_obj = self.env['account.account.template']
        acc_template = account_tmpl_obj.search([('nocreate', '!=', True), ('chart_template_id', '=', self.id)],
                                               order='id')
        template_vals = []
        for account_template in acc_template:
            code_main = account_template.code and len(account_template.code) or 0
            code_acc = account_template.code or ''
            if code_main > 0 and code_main <= code_digits:
                code_acc = str(code_acc) + (str('0' * (code_digits - code_main)))
            vals = self._get_account_vals(company, account_template, code_acc, tax_template_ref)
            template_vals.append((account_template, vals))
        accounts = self._create_records_with_xmlid('account.account', template_vals, company)
        for template, account in zip(acc_template, accounts):
            acc_template_ref[template] = account
            if template.parent_id:
                acc = self.env['account.account'].search([('code', '=', template.parent_id.code)], limit=1)
                account.write({'parent_id': acc.id})
        return acc_template_ref
