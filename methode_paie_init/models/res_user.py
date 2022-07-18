# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class UserMp(models.Model):
    _inherit = 'res.users'

    #id_agence = fields.Char(related='partner_id.id_agence', inherited=True, readonly=False)