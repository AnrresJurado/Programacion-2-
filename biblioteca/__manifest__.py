# -*- coding: utf-8 -*-
{
    'name': "Biblioteca Universitaria",
    'summary': "Gestión completa de libros, préstamos, usuarios y multas",

    'description': """
Sistema integral de gestión de biblioteca que incluye:

✔ Registro de libros, autores, géneros, editoriales y ubicaciones  
✔ Control de préstamos y devoluciones  
✔ Multas automáticas por retraso, daño, deterioro o pérdida  
✔ Registro de usuarios con historial completo  
✔ Cálculo de disponibilidad y control de sanciones  
✔ Secuencias automáticas para préstamos y multas  
✔ Wizard para cierre de préstamo y evaluación del libro  
    """,

    'author': "Andres Jurado",
    'website': "https://andresjurado.dev",

    'category': 'Education',
    'version': '1.0.0',

    # Módulos requeridos
    'depends': [
        'base',
        'mail',
    ],

    # Archivos del módulo
    'data': [
        # Seguridad
        'security/ir.model.access.csv',

        # Secuencias
        'data/sequence.xml',

        # Vistas separadas por módulo
        'views/libro_views.xml',
        'views/prestamo_views.xml',
        'views/usuarios_views.xml',
        'views/multa_views.xml',
        'views/menu_views.xml',

        # Wizard
        'views/wizard_views.xml',
    ],

    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
