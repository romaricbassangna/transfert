# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class OperationSite(models.Model):
    _name = 'mp.operation_site'

    """name = fields.Char(string="Libellé opération")
    montant = fields.Integer(string="Montant")
    id_compte = fields.Many2one('mp.compte', string='Compte')
    id_compte_site = fields.Many2one('mp.compte_site', string='Transfert')
    date = fields.Date(string="Date de transfert", default=datetime.today(), required=True)"""