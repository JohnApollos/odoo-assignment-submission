{
    'name': 'Purchase Request',
    'version': '1.0',
    'depends': ['purchase', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/purchase_request_views.xml',
        'views/purchase_request_line_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}
