# -*- coding: utf-8 -*-
{
    'name': "odoogoedu",

    'summary': """
        odoo12开发基础练习模块""",

    'description': """
        odoo12开发基础练习模块
        学习模块编程的整个过程
    """,

    'author': "n37r06u3",
    'website': "http://www.odoogo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['board'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/partner.xml',
        'data.xml',
        'views/session_board.xml',
        'reports.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
    'application': True,
    'sequence': 1,
}
