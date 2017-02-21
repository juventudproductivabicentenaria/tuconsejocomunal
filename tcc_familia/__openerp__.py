# -*- coding: utf-8 -*-
{
    'name': "Gestion de Familia (3)",

    'summary': """
        Reguistro de grupos familiares en los consejos comunales""",

    'description': """
        En este modúlo se realizan los registros de los grupos familiares que conviven
         dentro de tu consejo comunal para asi optimizar la información 
         según las casas o edificios de la comunidad. 
    """,

    'author': "Alberto Salmeron ,Jenny Forero y Yirleidy Lovera ",
    

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Gestion publica',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','tcc_consejocomunales','tcc_vivienda'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
         'views/familias.xml',
         
         
    ],
    # only loaded in demonstration mode
    'demo': [
       # 'demo.xml',
    ],
}
