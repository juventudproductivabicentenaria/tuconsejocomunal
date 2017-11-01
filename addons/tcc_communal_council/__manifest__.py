# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Consejo Comunal',
    'author' : 'A.C. JUVENTUD PRODUCTIVA VENEZOLANA R.S., UNEFA y Fundación ATTA',
    'version' : '1.1',
    'summary': 'Registro de la estructura de los consejo comunal',
    'sequence': 10,
    'description': """
Registro de los Consejos comunales
====================
Un consejo Comunal es un registro único, que estará compuesto por voceros e integrantes de la comunidad.

Cada Consejo comunal podrá realizar registros de noticias, tareas y encuentas y será notificados todos los miembros del consejo comunal
    """,
    'category': 'Consejo Comunal',
    'website': 'http://juventudproductivabicentenaria.blogspot.com/',
    #~ 'images' : ['images/accounts.jpeg','images/bank_statement.jpeg','images/cash_register.jpeg','images/chart_of_accounts.jpeg','images/customer_invoice.jpeg','images/journal_entries.jpeg'],
    'depends' : ['base_setup','survey','project','l10n_ve_dpt','inputmask_widget','backend_theme_v10'],
    'data': [
        'security/communal_council_security.xml',   # Grupos y roles
        'security/filter_users_rule.xml',           # Filtros 
        'views/communal_council_view.xml',          # Vistas Consejos comunales
        'views/dwelling_view.xml',                  # Vistas Vivienda
        'views/family_view.xml',                    # Vistas Familia
        'views/home_address_view.xml',              # Vistas Dirección
        'views/persons_view.xml',                   # Vistas Residente
        'views/notice_view.xml',                    # Vistas Noticias
        'views/committee_view.xml',                 # Vistas Comités
        'views/survey_view.xml',                    # Vistas Encuestas
        'views/project_view.xml',                   # Vistas Proyectos
        'views/product_distribution_view.xml',      # Vistas Distribución
        'data/ir_sequence_data.xml',                # Sequencia codigo de familia
        'data/family_data.xml',                     # Data de familia
        'data/persons_data.xml',                    # Data de Personas
        
        'security/tcc_group_consejo/ir.model.access.csv',
        'security/tcc_group_residente/ir.model.access.csv',
        'security/tcc_group_vocero/ir.model.access.csv',
        
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
