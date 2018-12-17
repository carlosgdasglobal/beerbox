{
    'name': "Babel Bundle",
    'author': 'ERP Ukraine',
    'website': 'https://erp.co.ua',
    'support': 'support@erp.co.ua',
    'category': 'Tools',
    'version': '11.0.2.0',
    'license': 'AGPL-3',
    'depends': [
        'website',
    ],
    'data': [
        'views/assets.xml',
    ],
    'external_dependencies': {
        'bin': [
            'babel',
        ],
    },
    'images': ['static/description/babel-cover.png'],
    'post_load': 'babel_patch',
    'uninstall_hook': 'uninstall_hook',
    'installable': True,
    'application': False,
    'auto_install': False,
}
