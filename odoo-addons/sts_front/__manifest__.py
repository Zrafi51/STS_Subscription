{
    'name': 'STS Frontend',
    'version': '1.0',
    'summary': 'Frontend module for STS subscriptions',
    'author': 'Mehdi Zrafi',
    'category': 'Extra Tools',
    'depends': ['website', 'web', 'sts_abon', 'auth', 'resroutier'],
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'sts_front/static/src/css/style.css',
        ],
    },
    'installable': True,
    'application': True,
    'sequence': 4
}