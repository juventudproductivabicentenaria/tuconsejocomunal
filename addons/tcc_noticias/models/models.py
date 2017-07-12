# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class tcc_noticias(osv.osv):
    _name = 'tcc.noticias'
    _rec_name='titulo'
    
    _columns={
		'consejo_id':fields.many2one(
                    'tcc.consejocomunales',
                    'Consejo Comunal',
                    required=True,
                    ondelete='cascade'
                    ),
		'categoria_id':fields.many2one(
                    'tcc.noticias_categoria',
                    'Categoria',
                    required=True,
                    ),
        'titulo':fields.char('Título',help='Título de la noticia'),
        'subtitulo':fields.char('Sub Título',help='Sub Título de la noticia'),
        'fecha_init':fields.datetime('Fecha publicación',help='Fecha de publicación'),
        'fecha_fin':fields.datetime('Fecha fin de la publicación',help='Fecha fin de la publicación'),
        'cotenido':fields.html('Noticia'),
        'active':fields.boolean('Activo',help='Si esta activo el motor lo incluira en la vista...'),
        }
        
    _defaults={
        'active':True
        }
        
        
class tcc_noticias_categoria(osv.osv):
    _name = 'tcc.noticias_categoria'
    _rec_name='name'
    
    _columns={
        'name':fields.char('Nombre',required=True,help='Título de la noticia'),
        'active':fields.boolean('Activo',help='Si esta activo el motor lo incluira en la vista...'),
        }
        
    _defaults={
        'active':True
        }

