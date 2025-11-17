# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class BibliotecaPrestamo(models.Model):
    _name = 'biblioteca.prestamo'
    _description = 'Registro de préstamos'

    # =========================
    # CAMPOS PRINCIPALES
    # =========================
    name = fields.Char(
        string='Préstamo',
        readonly=True,
        required=True,
        copy=False,
        default='/'
    )

    fecha_prestamo = fields.Datetime(
        string='Fecha de Préstamo',
        default=lambda self: fields.Datetime.now(),
        readonly=True,
    )
    fecha_devolucion = fields.Datetime(
        string='Fecha de Devolución',
    )

    libro_id = fields.Many2one(
        'biblioteca.libro',
        string='Libro',
        required=True,
    )
    usuario_id = fields.Many2one(
        'biblioteca.usuarios',
        string='Usuario',
        required=True,
    )

    registrado_por = fields.Many2one(
        'res.users',
        string='Registrado por',
        default=lambda self: self.env.user,
        readonly=True,
    )

    fecha_maxima = fields.Datetime(
        compute='_compute_fecha_maxima',
        store=True,
        readonly=True,
    )

    # =========================
    # ESTADO
    # =========================
    estado = fields.Selection([
        ('b', 'Borrador'),
        ('p', 'Prestado'),
        ('d', 'Devuelto'),
        ('m', 'Multa'),
    ], default='b', string='Estado')

    # =========================
    # MULTAS
    # =========================
    multa_generada = fields.Boolean(default=False, readonly=True)
    monto_multa = fields.Float(default=0.0, readonly=True)

    multa_id = fields.Many2one(
        'biblioteca.multa',
        string='Multa generada',
        readonly=True,
    )

    motivo_multa = fields.Selection([
        ('dano', 'Daño'),
        ('deterioro', 'Deterioro'),
        ('perdida', 'Pérdida'),
    ])

    # =========================
    # CAMPOS INFORMATIVOS
    # =========================
    libro_disponible = fields.Boolean(
        compute="_compute_info_libro"
    )

    usuario_multas = fields.Integer(
        compute="_compute_info_usuario"
    )

    usuario_multas_pend = fields.Integer(
        compute="_compute_info_usuario"
    )

    # =========================
    # CONSTRAINS
    # =========================

    @api.constrains('estado', 'motivo_multa')
    def _check_motivo_multa(self):
        for rec in self:
            if rec.estado == 'm' and not rec.motivo_multa:
                raise ValidationError("Debe seleccionar un motivo de multa.")

    @api.constrains('libro_id', 'estado')
    def _check_libro_disponible(self):
        for rec in self:
            if rec.estado in ('b', 'p') and rec.libro_id.disponi != 'disponible':
                raise ValidationError("Este libro no está disponible para préstamo.")

    @api.constrains('usuario_id', 'estado')
    def _check_usuario_multas(self):
        for rec in self:
            if rec.estado in ('b', 'p') and rec.usuario_multas_pend > 0:
                raise ValidationError("El usuario tiene multas pendientes.")

    # =========================
    # COMPUTES
    # =========================

    @api.depends('fecha_prestamo')
    def _compute_fecha_maxima(self):
        for record in self:
            record.fecha_maxima = (record.fecha_prestamo or fields.Datetime.now()) + timedelta(days=2)

    @api.depends('libro_id', 'libro_id.disponi')
    def _compute_info_libro(self):
        for rec in self:
            rec.libro_disponible = rec.libro_id.disponi == 'disponible'

    @api.depends('usuario_id')
    def _compute_info_usuario(self):
        """
        PREVIENE EL ERROR:
        AttributeError: 'list' object has no attribute 'filtered'

        Odoo 18 a veces devuelve listas nativas al hacer onchange → arreglado.
        """
        Multa = self.env['biblioteca.multa']

        for rec in self:
            if not rec.usuario_id:
                rec.usuario_multas = 0
                rec.usuario_multas_pend = 0
                continue

            multas = Multa.search([('usuario_id', '=', rec.usuario_id.id)])

            # Asegurar recordset correcto si Odoo devuelve lista
            if not hasattr(multas, 'filtered'):
                multas = Multa.browse([m.id for m in multas])

            rec.usuario_multas = len(multas)

            # Filtrado seguro sin .filtered()
            rec.usuario_multas_pend = len([m for m in multas if m.estado == 'pendiente'])

    # =========================
    # CRON
    # =========================

    def _cron_generar_multas(self):
        prestamos = self.search([
            ('estado', '=', 'p'),
            ('fecha_maxima', '<', fields.Datetime.now()),
        ])
        Multa = self.env['biblioteca.multa']

        for prestamo in prestamos:
            if prestamo.multa_generada:
                continue

            dias_retraso = (fields.Datetime.now() - prestamo.fecha_maxima).days
            if dias_retraso <= 0:
                continue

            monto = dias_retraso * 1.0

            multa = Multa.create({
                'usuario_id': prestamo.usuario_id.id,
                'prestamo_id': prestamo.id,
                'multa': monto,
                'valor_multa': monto,
                'fecha_multa': fields.Date.today(),
                'estado': 'pendiente',
            })

            prestamo.write({
                'estado': 'm',
                'multa_generada': True,
                'monto_multa': monto,
                'multa_id': multa.id,
            })

    # =========================
    # CREATE
    # =========================

    @api.model
    def create(self, vals):
        if vals.get('name') in (None, '/'):
            vals['name'] = self.env['ir.sequence'].next_by_code('biblioteca.prestamo') or '/'
        return super().create(vals)

    # =========================
    # BOTÓN PRESTAR
    # =========================

    def generar_prestamo(self):
        for rec in self:
            rec.write({'estado': 'p'})
            rec.libro_id.disponi = 'prestado'
