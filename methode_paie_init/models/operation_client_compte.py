# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class OperationClientCompte(models.Model):
    _name = 'mp.operation_client_compte'

    name = fields.Char(string="Libellé opération")
    montant = fields.Integer(string="Montant")
    id_compte = fields.Many2one('mp.compte_client', string='Compte Client')
    date = fields.Date(string="Date de transfert", default=datetime.today(), required=True)