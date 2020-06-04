# -*- coding: utf-8 -*-
{
    'name': "AIO Pharmacy",

    'summary': """
       All In One Pharmacy Solution contaions all pharmacy needs""",

    'description': """
        All In One Pharmacy Solution contaions all pharmacy needs
		Sales :
		Purchase :
		Inventory :
    """,

    'author': "E.Mudathir Ahmed Omer",
    'website': "http://www.msolution.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'module_category_point_of_sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','stock','sale_management','backend_theme_cyan'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/starter_data.xml',
        'views/menu.xml',
        'views/purchase_view.xml',
        'views/sales_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
