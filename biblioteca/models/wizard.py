from odoo import models, fields, api

class BibliotecaWizard(models.TransientModel):
    _name = 'biblioteca.wizard'
    _description = 'Wizard de Cierre de Préstamo'

    prestamo_id = fields.Many2one(
        'biblioteca.prestamo',
        string='Préstamo',
        required=True,
        readonly=True
    )

    evaluacion_libro = fields.Selection([
        ('ok', 'En buen estado'),
        ('deterioro', 'Deterioro'),
        ('dano', 'Daño'),
        ('perdida', 'Pérdida'),
    ], string='Estado del Libro', required=True)

    observaciones = fields.Text(string='Comentario del bibliotecario')

    def cerrar_prestamo(self):
        self.ensure_one()
        prestamo = self.prestamo_id

        # 1. Marcar préstamo devuelto
        prestamo.write({
            'fecha_devolucion': fields.Datetime.now(),
            'estado': 'd',  # luego se cambia si hay multa
        })

        # 2. Marcar libro disponible
        if prestamo.libro_id:
            prestamo.libro_id.write({'disponi': 'disponible'})

        # 3. Generar multa si corresponde
        if self.evaluacion_libro in ('deterioro', 'dano', 'perdida'):

            monto = 10.0  # Ajustable

            multa = self.env['biblioteca.multa'].create({
                'usuario_id': prestamo.usuario_id.id,
                'prestamo_id': prestamo.id,     # <-- CORRECTO
                'multa': monto,
                'valor_multa': monto,
                'fecha_multa': fields.Date.today(),
                'estado': 'pendiente',
            })

            prestamo.write({
                'estado': 'm',
                'multa_generada': True,
                'multa_id': multa.id,
                'monto_multa': monto,
                'motivo_multa': self.evaluacion_libro,
            })

        return {'type': 'ir.actions.act_window_close'}
