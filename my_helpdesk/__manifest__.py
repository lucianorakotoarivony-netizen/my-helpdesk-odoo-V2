
{
    'name': 'My Helpdesk',
    'version': '1.0',
    'summary': 'Gestion des tickets de support',
    'description': """
    Système simple de gestion des tickets helpdesk.
    Suivi des demandes d'employé, assignation, priorités.
    """,
    'category': 'Technique',
    'author': 'KheyroW',
    'depends': ['base','web','bus','mail'],
    'assets': {
    'web.assets_backend': [
        'my_helpdesk/static/src/**/*.js',
        'my_helpdesk/static/src/**/*.xml',
    ]
},
    'license':'LGPL-3',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/ticket_views.xml',
        'data/cron.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
