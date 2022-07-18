# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Agence(models.Model):
    _name = 'mp.agence'

    name = fields.Char(string="Libellé agence")
    adresse = fields.Char(string="Adresse")
    courriel = fields.Char(string="Courriel")
    tel = fields.Char(string="N° Téléphone")
    id_ville = fields.Many2one('mp.ville', string='Ville')
