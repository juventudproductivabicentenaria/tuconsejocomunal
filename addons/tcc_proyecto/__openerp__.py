# -*- coding: utf-8 -*-
{
    'name': "Gestion de proyecto (6)",

    'summary': """
        """,

    'description': """
        
    """,

    'author': "Yorgenis, Wladimir",
    

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'proyecto',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project','tcc_consejocomunales'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
         'vistas/tcc_proyecto.xml'
         
    ],
    # only loaded in demonstration mode
    'demo': [
       # 'demo.xml',
    ],
}
