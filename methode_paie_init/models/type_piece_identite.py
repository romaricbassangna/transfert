# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class PieceId(models.Model):
    _name = 'mp.piece_id'

    name = fields.Char(string="Type de pièce d'identification")
