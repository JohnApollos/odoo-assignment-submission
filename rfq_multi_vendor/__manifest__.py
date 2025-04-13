{
    'name': 'RFQ Multiple Vendors',
    'version': '1.0',
    'depends': ['purchase'],
    'author': 'John Apollos Olal Onyango',
    'category': 'Purchases',
    'description': 'Allows assigning multiple vendors to an RFQ and managing bids.',
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_bid_views.xml',
        'views/purchase_bid_inline_views.xml',
        'views/purchase_views.xml',
        'wizard/bid_selection_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
