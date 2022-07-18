# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CompteSite(models.Model):
    _name = 'mp.compte_site'



    """ name = fields.Char(string="Libellé Compte")
    num_compte = fields.Char(string="N° Compte")
    montant_init = fields.Integer(string="Montant initiale")
    state = fields.Selection([('initialiser','Initialisation'),('confirmer','Confirmer')], 'Statut', compute="_compute_state", required=True, readonly=True, default='initialiser')
    id_site = fields.Many2one('mp.site', string='Site')
    montant_compte = fields.Float(compute="_montant_compte", method=True, store="False", string='Montant du compte')"""