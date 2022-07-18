# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Pays(models.Model):
    _name = 'mp.pays'
    _description='Pays'

    name = fields.Char(string="Nom pays")