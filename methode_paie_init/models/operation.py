# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class Operation(models.Model):
    _name = 'mp.operation'

    name = fields.Char(string="Libellé opération")
    montant = fields.Float(string="Montant")
    id_compte_client = fields.Many2one('mp.compte_client', string='Compte client')
    id_compte_agence = fields.Many2one('mp.compte', string='Compte Agence')
    id_transfert = fields.Many2one('mp.transfert', string='Transfert')
    taxe = fields.Float(string="taxe")
    date = fields.Date(string="Date de transfert", default=datetime.today(), required=True)
