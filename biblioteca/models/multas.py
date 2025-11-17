# -*- coding: utf-8 -*-
from odoo import models, fields, api

class BibliotecaMulta(models.Model):
    _name = 'biblioteca.multa'
    _description = 'Registro de multas'
    _rec_name = 'name_multa'

    usuario_id = fields.Many2one(
        'biblioteca.usuarios',
        string='Usuario',
        required=True
    )

    name_multa = fields.Char(
        string='Código de la Multa',
        readonly=True
    )

    multa = fields.Float(string='Multa calculada', default=0.0)
    valor_multa = fields.Float(string='Valor de la Multa', required=True)

    fecha_multa = fields.Date(
        string='Fecha de la Multa',
        default=fields.Date.today
    )

    prestamo_id = fields.Many2one(
        'biblioteca.prestamo',
        string='Préstamo'
    )

    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado')
    ],
    string='Estado',
    default='pendiente',
    required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name_multa'):
            vals['name_multa'] = self.env['ir.sequence'].next_by_code('biblioteca.multa') or '/'
        return super().create(vals)
