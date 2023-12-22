{
    'name': 'Real estate',
    'version': '13.0.0',
    'category': 'Hidden',
    'description': "Real estate",
    'data': [
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
    ],
    'test': True,
    'installable': True,
    'auto_install': True,
    'post_init_hook': 'post_init',
}