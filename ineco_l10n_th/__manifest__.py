# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'INECO Thailand - Accounting',
    'version': '2.0',
    'category': 'Accounting/Localizations/Account Charts',
    'description': """
Chart of Accounts for Thailand.
===============================

Thai accounting chart and localization.
    """,
    'author': 'INECO',
    'website': '',
    'depends': ['account'],
    'data': [
        'data/l10n_th_chart_data.xml',
        'data/account.account.template.csv',
        'data/l10n_th_chart_post_data.xml',
        'data/account_chart_template_data.xml',
        'views/account_account_view.xml',
    ],
    'demo': [

    ],
    'license': 'LGPL-3',
    # 'post_init_hook': '_preserve_tag_on_taxes',
'application': True,
}
