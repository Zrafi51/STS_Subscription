{
    'name': 'STS Abonnement',
    'version': '1.0',
    'category': 'Extra Tools',
    'author': 'Mehdi Zrafi',
    'summary': 'Module pour la gestion des abonnements de la STS with Payment Integration',
    'depends': ['base', 'resroutier', 'web', 'auth'],
    'data': [
        'security/ir.model.access.csv',
        'views/abonne_views.xml',
        'views/abonnement_views.xml',
        'views/menu.xml',
        'views/payment_views.xml',
    ],
    'installable': True,
    'application': True,
    'sequence': 1
}
