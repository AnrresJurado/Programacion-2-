# -*- coding: utf-8 -*-

from odoo import models, fields, api


class biblioteca(models.Model):
    _name = 'biblioteca.libro'
    _description = 'biblioteca.biblioteca'
    _rec_name = 'lastname'
    
    firstname = fields.Char(sritng='Nombre Libro')
    author = fields.Many2one('biblioteca.autor', string='Autor Libro') 
    value = fields.Integer(string='Numero ejemplares')
    value2 = fields.Float(compute="_value_pc", store=True, string="Costo")
    description = fields.Text(string='Descripcion libro')

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
    

class BibliotecaAutor(models.Model):
    _name = 'biblioteca.autor'
    _description = 'biblioteca.autor'
    
    firstname = fields.Char()
    lastname =  fields.Char()
    
    @api.depends('firstname','lastname')
    def_compute_display_name(self):
        for record in self:
            record.display_name = f"{record.firstname} {record.lastname}"
            