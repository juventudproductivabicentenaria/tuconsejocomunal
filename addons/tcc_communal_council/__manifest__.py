# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Consejo Comunal',
    'author' : 'A.C. JUVENTUD PRODUCTIVA VENEZOLANA R.S.',
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
    'depends' : ['base_setup','survey',],
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
        'views/product_distribution_view.xml',      # Vistas Distribución
        
        'security/tcc_group_consejo/ir.model.access.csv',
        'security/tcc_group_residente/ir.model.access.csv',
        'security/tcc_group_vocero/ir.model.access.csv',
        #~ 'data/data_account_type.xml',
        #~ 'data/account_data.xml',
        
    ],
    'demo': [
        #~ 'demo/account_demo.xml',
    ],
    'qweb': [
        #~ "static/src/xml/account_reconciliation.xml",
        #~ "static/src/xml/account_payment.xml",
        #~ "static/src/xml/account_report_backend.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
