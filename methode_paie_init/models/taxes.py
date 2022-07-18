# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Taxe(models.Model):
    _name = 'mp.taxe'

    name = fields.Char(string="Libellé Taxe")
    valeur_taxe= fields.Float(string="Valeur de la taxe")
    mode_calcul = fields.Selection([('pourcentage','Pourcentage'),('montant_fixe','Montant fixe')], 'Mode de Calcul')
    id_pays = fields.Many2one('res.country', string="Pays d'application de la taxe")
    active = fields.Boolean( string='Active')