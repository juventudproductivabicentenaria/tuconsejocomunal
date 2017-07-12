###
#
#   This file is part of odoo-addons.
#
#   odoo-addons is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   odoo-addons is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##

{
    'name': 'Fields masks',
    'version': '0.2',
    'description': """
Fields masks
================================================================================

Based on jquery.inputmask 3.x (https://github.com/RobinHerbots/jquery.inputmask)

An inputmask helps the user with the input by ensuring a predefined format.
This can be useful for dates, numerics, phone numbers, ...

Instructions:

- Just add data-inputmask="mask" to <field />

     Some examples:

     <field name="email" data-inputmask="'alias': 'email'" />
     <field name="ip_address" data-inputmask="'alias': 'ip'" />
     <field name="masked_field" data-inputmask="'mask': '99-9999999'" />

Masking definition:

    - 9: numeric value
    - a: alphabetical value
    - *: alphanumeric value

Aliases available:

    - email
    - ip: IPv4 addresses
    - url

    """,
    'author': 'Aristobulo Meneses',
    'website': 'https://menecio.github.io',
    'category': 'web',
    'depends': ['web'],
    'data': ['views/assets.xml', ]
}
