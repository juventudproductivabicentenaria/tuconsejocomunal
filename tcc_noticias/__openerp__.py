# -*- coding: utf-8 -*-
{
    'name': "Noticia TuConsejoComunal",

    'summary': """
        Modulo Diseñado para registrar noticias pertenecientes al consejo comunal""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Raymir Quijada, Ronal Rojas, Edgar Maican",
    

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Noticia',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
   
    'data': [
        # 'security/ir.model.access.csv',
        'views/tcc_noticia_view.xml',
        'views/tcc_categorias_view.xml',
			],
			
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
