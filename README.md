![logo jpb](https://yt3.ggpht.com/-Pdd2Yc_w1cs/AAAAAAAAAAI/AAAAAAAAAAA/zPOludtwSjU/s88-c-k-no-mo-rj-c0xffffff/photo.jpg,"Logo de juventud Productiva")![logo unefa](https://tecnologiaeducativaunefa.files.wordpress.com/2012/02/unefa-sin-fondo1.png?w=70&h=70,"Logo de unefa")![logo jpv](https://lh3.googleusercontent.com/-DnZXSzvOvRs/V9gxAUjRJIE/AAAAAAAAAAg/ledszMQjm7AJ16qBGs9PFuwBHEBX9iF9gCEw/w163-h110-p/6329863157855626369,"Logo de JPV")
# Sistema tuconsejocomunal.com

## Resumen

tuconsejocomunal.com nace con el fin de suplir la necesidades de las 
Organizaciones de Base del Poder Popular del Estado Venozalano,
para brindar apoyo en la gestión interna de los Consejos Comunales a tráves
de una plataforma web que brinde benificos a toda las comunidades organizadas en OBPP.

## Cádigo de ejemplo

from openerp.osv import fields, osv

class partner(osv.osv):
    _name = 'res.partner'
    _inherit="res.partner"
    _columns = {
        'is_consejo': fields.boolean(
                    'Consejo Comunal'
                    ),
        
      'rif': fields.char(
                    'RIF',
                    size=15,
                    required=True,
                    help='Número del R.I.F. de la Entidad'
                    ),
     'estado_id':fields.many2one('res.estados','Estado',required=True),
     'municipio_id':fields.many2one('res.municipios','Municipio',required=True),
     'parroquia_id':fields.many2one('res.parroquias','Parroquia',required=True)
    }
    
    _defaults={
        'is_consejo':False
        }

class tcc_consejocomunales(osv.osv):
     _name = 'tcc.consejocomunales'
     _inherits = {'res.partner': 'parent_id'}
     _rec_name='parent_id'
     _columns={
		'parent_id':fields.many2one(
                    'res.partner',
                    'Registro de los consejos Comunales',
                    required=True,
                    ondelete='cascade'
                    ),
        'cd_situr':fields.char('Código situr',help='Nombre del Consejo Comunal'),
        'fecha':fields.date('Fecha',size=20,help='Nombre del Consejo Comunal'),
        'active':fields.boolean('Activo',help='Si esta activo el motor lo incluira en la vista...'),
        }
        
## Motivación

Insentivar a los Consejos Comunales a actuar de forma organizada
y sistematizada, donde las familias integrantes puedan contar con
información en tiempo real y oportuna.

## Instalación

Para intalación requiere la versión [odoo-9.0](https://github.com/odoo/odoo/tree/9.0)
y seguir éste orden de intalación de los módulos:
1.- Gestión de los Consejos Comunales (1)

2.- Gestion de Vivienda (2)

3.- Gestion de Familia (3)

4.- Personas (4)

5.- tcc_noticias (5)

6.- Encuestas de Consejos Comunales (5)

7.- Gestion de proyecto (6)

