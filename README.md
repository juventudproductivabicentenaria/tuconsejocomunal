# Sistema tuconsejocomunal.com.ve

## Índice ##

*   [Resumen](#resumen)

*   [Código de ejemplo](#código-de-ejemplo)

*   [Motivación](#motivación)

*   [Instalación](#instalación)

*   [Documentación](#documentación)

*   [Sé un colaborador](#formas-de-colaborar)

*   [Para los desarrolladores](#guía-para-los-commits)

## Resumen ##

tuconsejocomunal.com.ve es una herramienta web para mejorar la gestión interna de
las Organizaciones de Base del Poder Popular (OBPP) del Estado Venozalano,
y brindar apoyo en la organización y esparcimiento de la información y agilizar
los procesos activos de los consejos comunales. Tales como:

* Ofrecer registro de familias que conforman el Consejo Comunal y estructura organizacional del mismo.
* Publicar información en la plataforma y notificar a todos los miembros de la comunidad registrados.
* Ayuda a la gestión de la Distribución de los benefición tanto del Consejo Comunal como los del Estado.
* Descargar formatos de documentos con información que ayude la relación rapida y oportuna con del Estado y otros Organismos.

## Código de ejemplo ##

`
class Partner(models.Model):
    _inherit = 'res.partner'
    
    is_council = fields.Boolean(
                    string='Es consejo', 
                    help="Indica sí el partner es un consejo comunal.",
                    )

class CommunalCouncil(models.Model):
    _name = "tcc.communal.council"
    _description = "Consejo Comunal"
    _inherits = {'res.users': 'user_id'}
    _rec_name = 'name'
    
    
    user_id = fields.Many2one(
                    'res.users', 
                    string='Usuario Consejo Comunal',
                    ondelete="cascade"
                    )
    situr_code = fields.Char(
                    string='Código SITUR',
                    )
    creation_date = fields.Date(
                    string='Fecha creación',
                    )
    rif = fields.Char(
                    string='RIF',
                    )
    state_id = fields.Many2one(
                    'res.country.state', 
                    string='Estado',
                    )

    sector_id = fields.Many2one(
                'tcc.address.sector',
                string='Sector', 
                )
    active = fields.Boolean(default=True)
    
    `
    
## Motivación ##

Insentivar a los Consejos Comunales a actuar de forma organizada
y sistematizada, donde las familias integrantes puedan contar con
información en tiempo real y oportuna.

## Instalación ##

Para intalación requiere la versión [odoo-10.0](https://github.com/odoo/odoo/tree/10.0)

Una vez Instalado Odoo 10, se ubica en el archivo de configuración y en el parametro addons_path del archivo odoo.conf adicionalerle: /tu_ruta/tuconsejocomunal/addons
reinicias el serviccio odoo, actualizas la lista de los modulos como admin y finalmente lo buscas e instalas.   

## Documentación ##

[![Docs](/docs/img/doc.png)](/docs)

## Formas de colaborar ##
    
Este es un proyecto de carácter público y colaborativo cualquiera puede hacer aportes como:

* Desarrollo de código
* Resolviendo las [__Issues__](https://github.com/juventudproductivabicentenaria/tuconsejocomunal/issues)
* Realizando pruebas y detectando fallos del sistema
* Utilizando la plataforma
* Aportar ideas para mejorar la plataforma

## Guía para los commits ##

Para que todos entendamos los cambios realizados y así entender más rápido
el código es conveniente seguir estos sencillos pasos, Así al navegar por
los mensajes de los commits no parezca un desastre.

1. Separar el título del cuerpo del mensaje

2. Limitar el título del mensaje a 50 carácteres

3. Iniciar el título del mensaje en mayúscula

4. No terminar el título del mensaje en punto

5. Usar el modo imperativo en la línea del título

6. Envolver el cuerpo del mensaje en 72 carácteres

7. Usar el cuerpo del mensaje para explicar qué y por qué vs. el cómo

### Por ejemplo ###

    Resumir los cambios en alrededor de 50 caracteres

    Texto explicativo lo más detallado, si es necesario. Envuélvalo a unos 72
    carácteres mas o menos. En algunos contextos, la primera línea se trata como
    el título commit y el resto del texto como el cuerpo. La línea en blanco que
    separa el resumen del cuerpo del mensaje es obligatoria (a menos que omita
    el cuerpo por completo); Varias herramientas como `log`, `shortlog`
    Y `rebase` puede confundirse si se ejecutan los dos juntos.

    Explique el problema que el commit está resolviendo. Concéntrese en por qué
    está haciendo este cambio en lugar de cómo (el código explica eso).
    ¿Hay efectos secundarios u otras consecuencias no intuitivas de este
    ¿cambio? Aquí es el lugar para explicarlo.

    Otros párrafos vienen después de líneas en blanco.

     - Las viñetas también están bien.

     - Normalmente se utiliza un guión o un asterisco para la viñeta, precedido
       Por un solo espacio, con líneas en blanco entre cada viñeta, pero las 
       convenciones pueden variar aquí.

    Si utiliza un rastreador de Issues, ponga referencias a ellos en la parte inferior,
    como esto:


    Resolves: #123
    See also: #456, #789
    Fix: #31
