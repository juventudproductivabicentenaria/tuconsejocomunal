# Sistema tuconsejocomunal.com

## Resumen

tuconsejocomunal.com es una herramienta web para mejorar la gestión interna de
las Organizaciones de Base del Poder Popular (OBPP) del Estado Venozalano,
y brindar apoyo en la organización y esparcimiento de la información y agilizar
los procesos activos de los consejos comunales. Tales como:

    -Ofrecer registro de familias que conforman el Consejo Comunal y  estructura organizacional del mismo.
    -Publicar información en la plataforma y notificar a todos los miembros de la comunaidad registrados.
    -Descargar formatos de documentos solicitados por los entes del Estado reguladores de los Consejos Comunales.
        

## Código de ejemplo

    class partner(osv.osv):
        _name = 'res.partner'
        _inherit="res.partner"
        _columns = {
            'is_consejo': fields.boolean(
                    'Consejo Comunal'),
            'rif': fields.char(
                    'RIF',
                    size=15,
                    required=True,
                    help='Número del R.I.F. de la Entidad'),
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

## Documentación

    [Documentación](tuconsejocomunal/docs/)

    
    
## Proyecto colaborativo
    
    Este es un proyecto de caracter público cualquier desarrollador puede
    ser colaborador.
