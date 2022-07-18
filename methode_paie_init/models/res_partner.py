# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class PartnerMp(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    id_agence = fields.Many2one('mp.agence', string="Agence")

