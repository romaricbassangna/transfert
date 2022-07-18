# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Tarif(models.Model):
    _name = 'mp.tarif'

    name = fields.Char(string="Libellé tarif")
    montant_min = fields.Float(string="Montant minimum")
    montant_max = fields.Float(string="Montant maximum")
    commission = fields.Float(string="Commission")
    mode_calcul = fields.Selection([('pourcentage','Pourcentage'),('montant_fixe','Montant fixe')], 'Mode de Calcul')
    id_pays_depart = fields.Many2one('res.country', string='Pays départ')
    id_pays_arrive = fields.Many2one('res.country', string='Pays arrivé')
    active = fields.Boolean( string='Active')