# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
{
    'name': 'Biblioteca',
    'version': '1.0',
    'summary': 'Gestión de biblioteca: libros, autores, préstamos, multas y usuarios',
    'description': """
Módulo para administrar una biblioteca completa:
- Registro de libros con detalles como ISBN, autor, categoría y ubicación.
- Gestión de autores y sus libros publicados.
- Control de usuarios registrados.
- Registro de préstamos y devoluciones de libros.
- Control de multas por retrasos o daños.
""",
    'author': 'Tu Nombre',
    'website': 'https://www.tusitio.com',
    'category': 'Tools',  # Categoría visible en Odoo
    'license': 'AGPL-3',
    'depends': ['base'],  # Dependencias de Odoo
    'data': [
        'security/ir.model.access.csv',  # Permisos de acceso
        'views/views.xml',               # Vistas y menús
        'data/sequence.xml'
    ],
    'installable': True,  # Necesario para que se pueda instalar
    'application': True,  # Marca el módulo como aplicación visible
    'auto_install': False, # No se instala automáticamente
}


