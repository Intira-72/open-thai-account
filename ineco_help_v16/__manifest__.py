# -*- coding: utf-8 -*-

{
    'name': 'INECO Youtube Helper',
    'version': '1.00',
    'category': 'INECO',
    'sequence': 145,
    'summary': 'Link yourtube video to help user',
    'description': """
INECO Youtube Helper
    """,
    'website': 'https://www.ineco.co.th',
    'depends': ['base', 'base_setup', 'bus', 'web_tour'],
    'data': [
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': {
            'ineco_help_v16/static/src/js/components/youtube_menu/*'
        },
        'web.assets_qweb': {
        },
    },
    'license': 'LGPL-3',
}
