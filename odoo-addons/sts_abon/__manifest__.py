{
    'name': 'STS Abonnement',
    'version': '1.0',
    'category': 'Productivity',
    'author': 'Mehdi Zrafi',
    'summary': 'Module pour la gestion des abonnements de la STS with Payment Integration',
    'depends': ['base', 'resroutier', 'web', 'auth_signup', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/abonne_views.xml',
        'views/abonnement_views.xml',
        'views/payment_views.xml',
        'views/auth_views.xml',
        'views/templates/signup_template.xml',
        'views/templates/homepage_template.xml',
        'views/templates/verification_template.xml',
        'views/templates/login_template.xml',
        'views/templates/data_template.xml',
        'views/templates/subscription_template.xml',
        'views/reset_password_template.xml',
        'views/forgot_password_template.xml',
        'views/auth_signup_template.xml',
        'views/auth_login_template.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'sts_abon/static/src/css/style.css',
            'sts_abon/views/js/subscription.js',
        ],
    },
    'installable': True,
    'application': True,
    'sequence': 1,
}