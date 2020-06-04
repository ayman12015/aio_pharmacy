# -*- coding: utf-8 -*-
{
    'name': " Pharmacy Managment Tracking performance",

    'summary': """
       APharmacy management tracking performance""",

    'description': """
        to make this happen we need three modules:
		1 - Sales : to control sales orders
		2- Purchase : to control purchase order
		3- Inventory : to locate the medcine or the product in locations 
    """,

    'author': "Ayman Osman",
    'website': "http://www.ayman.com",

    #
    'category': 'module_category_point_of_sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','stock','sale_management'],

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
