# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BibliotecaUsuarios(models.Model):
    _name = 'biblioteca.usuarios'
    _description = 'Registro de usuarios'
    _rec_name = 'display_name'
    _order = 'lastname asc, firstname asc'

    firstname = fields.Char(string='Nombres', required=True)
    lastname = fields.Char(string='Apellidos', required=True)

    display_name = fields.Char(
        compute='_compute_display_name',
        store=True
    )

    identificacion = fields.Char(string='Identificación', required=True)
    telefono = fields.Char(string='Teléfono')
    email = fields.Char(string='Correo Electrónico')
    direccion = fields.Text(string='Dirección')
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento')
    activo = fields.Boolean(string='Activo', default=True)

    prestamos = fields.One2many(
        'biblioteca.prestamo',
        'usuario_id',
        string='Préstamos'
    )


    @api.depends('firstname', 'lastname')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.firstname} {rec.lastname}".strip()


    @api.constrains('identificacion')
    def _check_cedula(self):
        for rec in self:
            valido, mensaje = rec.validar_cedula(rec.identificacion)
            if not valido:
                raise ValidationError(mensaje)

    _sql_constraints = [
        ('identificacion_unique',
         'unique(identificacion)',
         'La identificación ya está registrada.'),
    ]

    # ======================================
    # VALIDADOR DE CÉDULA ECUATORIANA
    # ======================================
    def validar_cedula(self, cedula):
        if len(cedula) != 10:
            return (False, "La cédula debe tener exactamente 10 dígitos")
        if not cedula.isdigit():
            return (False, "La cédula solo debe contener números")
        provincia = int(cedula[:2])
        if provincia < 1 or provincia > 24:
            return (False, "Provincia inválida (01–24)")
        tercer_digito = int(cedula[2])
        if tercer_digito > 6:
            return (False, "El tercer dígito debe estar entre 0 y 6")
        coef = [2,1,2,1,2,1,2,1,2]
        digito_v = int(cedula[-1])
        suma = 0
        for i in range(9):
            num = int(cedula[i]) * coef[i]
            suma += num - 9 if num >= 10 else num
        calculado = (10 - (suma % 10)) % 10
        if calculado != digito_v:
            return (False, "Dígito verificador incorrecto.")
        return (True, "Cédula válida")
