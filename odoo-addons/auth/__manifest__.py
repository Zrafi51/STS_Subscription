{
    'name': 'Authentication',
    'version': '1.0',
    'summary': 'User Authentication with SMS Verification',
    'category': 'Extra Tools',
    'author': 'Mehdi Zrafi',
    'depends': ['base', 'web'],#, 'web'
    'data': [
        'security/ir.model.access.csv',
        'views/auth_views.xml',
        'views/auth_menus.xml',
    ],
    'installable': True,
    'application': True,
    'sequence': 2
}
