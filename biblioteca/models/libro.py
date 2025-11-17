# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
import requests

class BibliotecaLibro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Libros de la biblioteca'
    _rec_name = 'titulo'

    codigo_libro = fields.Char(
        string='Código del Libro',
        readonly=True,
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('biblioteca.libro')
    )

    titulo = fields.Char(string='Título del Libro', required=True)

    author = fields.Many2one(
        'biblioteca.autor',
        string='Autor Libro'
    )

    publicacion = fields.Char(string='Año Publicación')

    ejemplares = fields.Integer(
        string='Número de ejemplares',
        default=1,
    )

    costo = fields.Float(
        string='Costo',
        compute='_compute_costo',
        store=True
    )

    isbn = fields.Char(string='ISBN')

    editorial_id = fields.Many2one(
        'biblioteca.editorial',
        string='Editorial'
    )

    genero_id = fields.Many2one(
        'biblioteca.genero',
        string='Género'
    )

    # *** CORRECCIÓN AQUÍ ***
    ubicacion_id = fields.Many2one(
        'biblioteca.ubicacion',
        string='Ubicación'
    )

    description = fields.Text(string='Descripción del Libro')

    disponi = fields.Selection([
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('reservado', 'Reservado')
    ], string='Estado', default='disponible')


    @api.depends('ejemplares')
    def _compute_costo(self):
        for record in self:
            record.costo = (record.ejemplares or 0) * 1.50


    def importar_desde_openlibrary(self):
        for record in self:
            if not record.isbn:
                raise UserError("Debe ingresar un ISBN para poder buscar.")

            url = f"https://openlibrary.org/isbn/{record.isbn}.json"
            response = requests.get(url)

            if response.status_code != 200:
                raise UserError("No se encontró un libro con ese ISBN en OpenLibrary.")

            data = response.json()

            # TÍTULO
            record.titulo = data.get('title') or record.titulo

            # AÑO
            record.publicacion = data.get('publish_date') or record.publicacion

            # AUTOR
            if data.get('authors'):
                autor_key = data['authors'][0].get('key', '').replace('/authors/', '')

                try:
                    autor_info = requests.get(
                        f"https://openlibrary.org/authors/{autor_key}.json"
                    ).json()
                    nombre_completo = autor_info.get('name', autor_key)
                except Exception:
                    nombre_completo = autor_key

                partes = nombre_completo.split()
                firstname = " ".join(partes[:-1]) if len(partes) > 1 else nombre_completo
                lastname = partes[-1] if len(partes) > 1 else ""

                autor_obj = self.env['biblioteca.autor'].search([
                    ('firstname', '=', firstname),
                    ('lastname', '=', lastname)
                ], limit=1)

                if not autor_obj:
                    autor_obj = self.env['biblioteca.autor'].create({
                        'firstname': firstname,
                        'lastname': lastname
                    })

                record.author = autor_obj.id

            # DESCRIPCIÓN
            desc = data.get('description')
            if isinstance(desc, dict):
                desc = desc.get('value')

            record.description = desc or record.description or "Sin descripción"
