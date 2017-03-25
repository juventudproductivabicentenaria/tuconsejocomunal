# -*- coding: utf-8 -*-
{
    'name': "Gestion de Vivienda (2)",

    'summary': """
        En este modulo se relaliza el registro de las viviendas de los consejos comunales""",

    'description': """
       Este modulo es para el registro de las viviendas de los consejos comunales
    """,

    'author': "Isaac Laplante",
    'website': "http://www.yourcompany.com.ve",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','tcc_consejocomunales'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'vistas/vivienda_view.xml',
        'vistas/casas_view.xml',
        'vistas/edificios_view.xml',
        'vistas/callesoavenidas_view.xml',
        'vistas/sectores_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
