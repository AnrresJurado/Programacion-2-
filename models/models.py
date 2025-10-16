# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

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
    _description = 'Registro de préstamos'
    
    name = fields.Char(string='Préstamo', required=True)
    fecha_prestamo = fields.Datetime(default=datetime.now())
    libro_id = fields.Many2one('biblioteca.libro', string='Libro')
    usuario_id = fields.Many2one('biblioteca.usuarios', string='Usuario')
    fecha_devolucion = fields.Datetime(string='Fecha de Devolución')
    multa_boleana = fields.Boolean(string='Tiene Multa', default=False)
    multa = fields.Float(string='Multa', default=0.0)
    fecha_maxima = fields.Datetime(compute='_compute_fecha_maxima')
    usuario = fields.Many2one('res.users', string='Usuario presta',default = lambda self: self.env.uid)
    estado = fields.Selection([
        ('p', 'Prestado'),
        ('d', 'Devuelto'),
        ('r', 'Retrasado'),
        ('m', 'Multa')
    ], string='Estado', default='p')
    
    @api.depend('fecha_maxima' , 'fecha_prestamo')
    def _compute_fecha_maxima(self):
        for record in self:
            record.fecha_maxima = record.fecha_prestamo + timedelta(days=2)
            
    def write(self,vals):
        seq = self.env.ref('biblioteca.sequence_codigo_prestamos').next_by_code('biblioteca.prestamo')
        vals['name'] = seq 
        

    def generar_prestamo(self):
        print("Generando Préstamo")
        self.write({'estado': 'p'})


class BibliotecaMulta(models.Model):
    _name = 'biblioteca.multa'
    _description = 'Registro de multas'
    _rec_name = 'name_multa'
    
    name_multa = fields.Char(string='Código de la Multa')
    multa = fields.Char(string='Información de la Multa')
    valor_multa = fields.Float(string='Valor de la Multa')
    fecha_multa = fields.Date(string='Fecha de la Multa')
    prestamo = fields.Many2one('biblioteca.prestamo', string='Préstamo')


class BibliotecaUsuarios(models.Model):
    _name = 'biblioteca.usuarios'
    _description = 'Registro de usuarios'
    _rec_name = 'firstname'
    
    firstname = fields.Char(string='Nombres')
    lastname = fields.Char(string='Apellidos')
    identificacion = fields.Char(string='Identificación')
    telefono = fields.Char(string='Teléfono')
    email = fields.Char(string='Correo Electrónico')
    direccion = fields.Text(string='Dirección')
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento')
    activo = fields.Boolean(string='Activo', default=True)
    prestamos = fields.One2many('biblioteca.prestamo', 'usuario_id', string='Préstamos')

    @api.constrains('identificacion')
    def _check_identificacion(self):
        for record in self:
            cedula = record.identificacion
            if not cedula:
                raise ValidationError("Debe ingresar una cédula antes de guardar el registro.")
            if not cedula.isdigit():
                raise ValidationError("La cédula solo debe contener números.")
            if len(cedula) != 10:
                raise ValidationError("La cédula debe tener exactamente 10 dígitos.")


   