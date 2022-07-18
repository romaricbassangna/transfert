# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Ville(models.Model):
    _name = 'mp.ville'

    name = fields.Char(string="Nom ville")
    id_pays = fields.Many2one('res.country', string='Pays')