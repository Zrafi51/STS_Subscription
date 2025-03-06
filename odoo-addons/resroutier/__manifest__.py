{
    'name': 'STS Resroutier',
    'version': '1.0',
    'summary': 'Route and Transportation Management',
    'description': """
        Comprehensive route management system for STS:
        - Route definition and management
        - Stop management
        - Schedule management
        - Tariff calculation
    """,
    'author': 'Mehdi Zrafi',
    'category': 'Transportation',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/resroutier_views.xml',
        'views/resroutier_menus.xml',
    ],
    'installable': True,
    'application': True,
    'sequence': -3,
    'license': 'LGPL-3',
}