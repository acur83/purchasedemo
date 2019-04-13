# -*- coding: utf-8 -*-
# Part of 
# Created by IT Group.

{
    'name': "SIMPLE Purchase Customization",
    'version': "1.0",
    'summary': "Customization of Purchase",
    'author': "IGE Developer.",
    'category': 'Library',
    'description': """
    Purchase Order Customization.
    """,
    'depends': ['hr', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'security/access.xml',
        'views/purchase_order.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
