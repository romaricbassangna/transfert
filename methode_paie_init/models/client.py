# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Client(models.Model):
    _name = 'mp.client'

    name = fields.Char(string="Nom")
    prenom = fields.Char(string="Prenom")
    nationatile =fields.Many2one('res.country', string='Nationalité')
    tel = fields.Char(string="N° Téléphone")
    id_piece_iden = fields.Many2one('mp.piece_id', string="Type de pièce")
    id_transfert_id_beneficiaire = fields.One2many('mp.transfert', 'id_beneficiaire', string="Transfert beneficiare")
    id_transfert_id_expediteur = fields.One2many('mp.transfert', 'id_expediteur', string="Transfert expediteur")
    num_piece = fields.Char(string="N° de la pièce")
    sexe = fields.Selection([('m','Masculin'),('f','Féminin')], 'Sexe')
    date_delivrance_piece_id = fields.Date(string="Date de délivrance")
    date_expiration_piece_id = fields.Date(string="Date d'expiration")


    _sql_constraints = [
        ('client_tel_uniq', 'unique (name,prenom,nationatile,sexe,tel)', 'Le client que vous chercher à creer existe déjà veillez rechercher dans la liste des client !')
    ]

    _sql_constraints = [
        ('client_num_piece_uniq', 'unique (name,prenom,nationatile,sexe,id_piece_iden,num_piece)', 'Le client que vous chercher à creer existe déjà veillez rechercher dans la liste des client !')
    ]