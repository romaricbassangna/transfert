# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models, Command
from odoo.exceptions import ValidationError
from datetime import datetime


class CompteClient(models.Model):
    _name = 'mp.compte_client'



    name = fields.Char(string="Libellé Compte", default="Compte cleint")
    num_compte = fields.Char(string="N° Compte", default="411")
    id_client = fields.Many2one('mp.client', string='Client')
    montant_compte = fields.Float( string='Montant du compte', compute="_compute_montant_compte",)
    date = fields.Date(string="Date de création", default=datetime.today(), required=True)
    debit = fields.Float( string='Retrait', compute="_compute_debit",)
    credit = fields.Float( string='Dépôt', compute="_compute_credit",)

    _sql_constraints = [
        ('id_agence_uniq', 'unique (id_agence)', 'Une agence un peu pas avoir plusieur compte !')
    ]



    @api.onchange('name', 'id_agence')
    def _compute_debit(self):

        for record in self :
            somme_debit = 0

            operation_client_agence = self.env['mp.operation_client_agence'].search([('name', '=', 'debit'),
                                                                       ('id_compte_client', '=', record.id)])

            for debit in operation_client_agence:
                somme_debit = somme_debit + debit.montant

            record.debit = somme_debit


    @api.onchange('name', 'id_agence')
    def _compute_credit(self):

        for record in self :
            somme_credit = 0

            operation_client_agence = self.env['mp.operation_client_agence'].search([('name', '=', 'credit'),
                                                                       ('id_compte_client', '=', record.id)])

            for debit in operation_client_agence:
                y = debit.montant
                somme_credit = somme_credit + debit.montant

            record.credit = somme_credit

    @api.depends('debit', 'credit')
    def _compute_montant_compte(self):

        for record in self :
            somme_credit = 0
            operation_client_agence = self.env['mp.operation_client_agence'].search([('name', '=', 'credit'),
                                                                       ('id_compte_client', '=', record.id)])

            for debit in operation_client_agence:
                y = debit.montant
                somme_credit = somme_credit + debit.montant

            somme_debit = 0
            operation_client_agence = self.env['mp.operation_client_agence'].search([('name', '=', 'debit'),
                                                                       ('id_compte_client', '=', record.id)])

            for debit in operation_client_agence:
                somme_debit = somme_debit + debit.montant


            record.montant_compte = somme_credit - somme_debit
