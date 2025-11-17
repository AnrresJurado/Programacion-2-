# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BibliotecaLibro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'biblioteca.libro'
    _rec_name = 'firstname'
    
    codigo_libro= fields.Char(string= 'Código del Libro')
    firstname = fields.Char(sritng='Nombre Libro')
    author = fields.Many2one('biblioteca.autor', string='Autor Libro') 
    publicacion = fields.Char(string='Año Publicacion')
    ejemplares = fields.Integer(string='Numero ejemplares')
    costo = fields.Char(string='Costo')
    description = fields.Text(string='Descripcion libro')
    isbn = fields.Char(string='ISBN')
    categoria = fields. Char(string='Categoria')
    ubicacion = fields. Char(string='Ubicacion Fisica')


class BibliotecaAutor(models.Model):
    _name = 'biblioteca.autor'
    _description = 'Registro de autores'
    _rec_name = 'firstname'
    
    firstname = fields.Char(string='Nombre')
    lastname = fields.Char(string='Apellido')
    nacimiento = fields.Date(string='Fecha de Nacimiento')
    libros = fields.Many2many(
        'biblioteca.libro',
        'libros_autores_rel',
        column1='autor_id',
        column2='libro_id',
        string='Libros Publicados'
    )

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.firstname or ''} {record.lastname or ''}".strip()
            result.append((record.id, name))
        return result


class BibliotecaPrestamo(models.Model):
    _name = 'biblioteca.prestamo'
    _description = 'biblioteca.prestamo'
    
    name = fields.Char()
    fecha_prestamo = fields.Datetime()
    libro_id = fields.Many2one('biblioteca.libro')
    usuario_id = fields.Many2one('biblioteca.usuarios', string='Usuario')
    fecha_devolucion = fields.Datetime(string='Fecha de Devolución')
    multa_booleana = fields.Boolean(default=False)
    multa = fields.Float(string='Multa', default=0.0)
    estado = fields.Selection([
        ('p', 'Prestado'),
        ('d', 'Devuelto'),
        ('r', 'Retrasado'),
        ('m', 'Multa')
    ], string='Estado', default='prestado')

class BibliotecaMulta(models.Model):
    _name = 'biblioteca.multa'
    _description = 'biblioteca.multa'
    _rec_name = 'name_multa'
    
    name_multa = fields.Char(string='Codigo de la Multa')
    multa = fields.Char(string='Informacion de la Multa')
    valor_multa = fields.Float(string='Valor de la Multa')
    fecha_multa = fields.Date(string='Fecha de la Multa')
    prestamo = fields.Many2one('biblioteca.prestamo')

class BibliotecaUsuarios(models.Model):
    _name = 'biblioteca.usuarios'
    _description = 'biblioteca.usuarios'
    _rec_name = 'firstname'
    
    firstname = fields.Char(string='Nombres')
    lastname = fields.Char(string='Apellidos')
    identificacion = fields.Char(string='Identificacion')
    telefono = fields.Char(string='Telefono')
    email = fields.Char(string='Email')
    direccion = fields.Text(string='Direccion')
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento')
    activo = fields.Boolean(string='Activo', default=True)
    prestamos = fields.One2many('biblioteca.prestamo', 'usuario_id', string='Prestamos')

   