# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class tcc_noticias(osv.osv):
     _name = 'tcc_noticias.tcc_noticias'
     _rec_name = 'titulo_noticia'

     stados=[
     ('borrador','Borrador'),
     ('publicado','Publicado'),
     ('cancel','Cancelado'),
     ('vencido','Vencido'),
     ]
     _columns={
     
        'titulo_noticia':fields.char('Titulo',size=50,required=True,help='Titulo'),
        'subtitulo':fields.char('Subtitulo',size=50,required=True,help='Subtitulos'),
        'categorias_id':fields.many2one('tcc_categorias.tcc_categorias','Categoria',required=True,help='Categorias'),
        'consejocomunal_id':fields.many2one('tcc.consejocomunales','Consejo comunal',required=True,help='Nombre del consejo comunal'),
        'state':fields.selection(stados, help='Seleccion del estado actual de la publicacion',default='borrador'),
        'fecha_p':fields.datetime('Fecha de Publicacion',size=20,required=True,help='Ingrese Fecha de publicacion'),
        'contenido':fields.html('Contenido',size=20,required=True,help='Ingrese Contenido'),
        'fecha_f':fields.datetime('Fecha de Finalizacion',size=20,help='Fecha final'),
        'active':fields.boolean('Activar',help='Si esta activo el motor lo incluira en la vista...')
        }
        
     _defaults={
        'active':True,
        }
