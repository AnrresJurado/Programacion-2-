# -*- coding: utf-8 -*-
from odoo import models, fields, api

class BibliotecaAutor(models.Model):
    _name = 'biblioteca.autor'
    _description = 'Registro de autores'
    _rec_name = 'display_name'

    firstname = fields.Char(string='Nombre')
    lastname = fields.Char(string='Apellido')
    nacionalidad = fields.Char(string='Nacionalidad')
    nacimiento = fields.Date(string='Fecha de Nacimiento')
    biografia = fields.Text(string='Biografía')
    display_name = fields.Char(compute='_compute_display_name', store=True)
    libros = fields.Many2many(
        'biblioteca.libro',
        'libros_autores_rel',
        column1='autor_id',
        column2='libro_id',
        string='Libros publicados'
    )

    @api.depends('firstname', 'lastname')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.firstname or ''} {record.lastname or ''}".strip()
