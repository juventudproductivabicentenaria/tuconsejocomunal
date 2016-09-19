# -*- coding: utf-8 -*-
{
    'name': "Gestión de los Consejos comunales",

    'summary': """
		Este módulo lleva todo el CRUD del los consejos comunales 
        """,

    'description': """
        Este módulo es para el registro de los consejos comunales
    """,

    'author': "Felipe Villamizar",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'UNEFA',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'vistas/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'datas/demo.xml',
    ],
}
