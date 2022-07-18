# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models, Command
from odoo.exceptions import ValidationError
from datetime import datetime


class Compte(models.Model):
    _name = 'mp.compte'



    name = fields.Char(string="Libellé Compte")
    num_compte = fields.Char(string="N° Compte")
    montant_init = fields.Integer(string="Montant initiale")
    state = fields.Selection([('initialiser','Initialisation'),('confirmer','Confirmer')], 'Statut',required=True, readonly=True, default='initialiser')
    id_agence = fields.Many2one('mp.agence', string='Agence')
    montant_compte = fields.Float( string='Montant du compte', compute="_compute_montant_compte",)
    date = fields.Date(string="Date de création", default=datetime.today(), required=True)
    debit = fields.Float( string='Debit', compute="_compute_debit",)
    credit = fields.Float( string='Credit', compute="_compute_credit",)
    taxe = fields.Float( string='Taxes', compute="_compute_taxes",)

    _sql_constraints = [
        ('id_agence_uniq', 'unique (id_agence)', 'Une agence un peu pas avoir plusieur compte !')
    ]



    @api.onchange('name', 'id_agence')
    def _compute_taxes(self):

        for record in self :
            somme_taxe = 0
            operation_compte = self.env['mp.operation_client_agence'].search([('id_compte_agence', '=', record.id)])

            for taxe in operation_compte:
                somme_taxe = somme_taxe + taxe.taxe

            record.taxe = somme_taxe


    @api.onchange('name', 'id_agence')
    def _compute_debit(self):

        for record in self :
            somme_debit = 0
            operation_compte = self.env['mp.operation_compte'].search([('name', '=', 'debit'),
                                                                       ('id_compte_depart', '=', record.id)])
            for debit in operation_compte:
                somme_debit = somme_debit + debit.montant

            operation_client_agence = self.env['mp.operation_client_agence'].search([('name', '=', 'debit'),
                                                                       ('id_compte_agence', '=', record.id)])

            for debit in operation_client_agence:
                somme_debit = somme_debit + debit.montant

            record.debit = somme_debit


    @api.onchange('name', 'id_agence')
    def _compute_credit(self):

        for record in self :
            somme_credit = 0
            operation_compte = self.env['mp.operation_compte'].search([('name', '=', 'credit'),
                                                                       ('id_compte_arrive', '=', record.id)])

            for debit in operation_compte:
                somme_credit = somme_credit + debit.montant

            operation_client_agence = self.env['mp.operation_client_agence'].search([('name', '=', 'credit'),
                                                                       ('id_compte_agence', '=', record.id)])

            for debit in operation_client_agence:
                y = debit.montant
                somme_credit = somme_credit + debit.montant

            record.credit = somme_credit

    @api.depends('debit', 'credit')
    def _compute_montant_compte(self):

        for record in self :
            somme_credit = 0
            operation_compte = self.env['mp.operation_compte'].search([('name', '=', 'credit'),
                                                                       ('id_compte_arrive', '=', record.id)])
            y = operation_compte

            for debit in operation_compte:
                somme_credit = somme_credit + debit.montant

            operation_client_agence = self.env['mp.operation_client_agence'].search([('name', '=', 'credit'),
                                                                       ('id_compte_agence', '=', record.id)])

            for debit in operation_client_agence:
                y = debit.montant
                somme_credit = somme_credit + debit.montant


            somme_debit = 0
            operation_compte = self.env['mp.operation_compte'].search([('name', '=', 'debit'),
                                                                       ('id_compte_depart', '=', record.id)])

            for debit in operation_compte:
                somme_debit = somme_debit + debit.montant

            operation_client_agence = self.env['mp.operation_client_agence'].search([('name', '=', 'debit'),
                                                                       ('id_compte_agence', '=', record.id)])

            for debit in operation_client_agence:
                somme_debit = somme_debit + debit.montant


            record.montant_compte = somme_credit - record.montant_init - somme_debit

    @api.depends('name')
    def initialiser(self):
        self.write({'state':'confirmer'})