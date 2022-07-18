# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models, Command
from odoo.exceptions import ValidationError


class Compte(models.Model):
    _name = 'mp.compte'



    name = fields.Char(string="Libellé Compte")
    num_compte = fields.Char(string="N° Compte")
    montant_init = fields.Integer(string="Montant initiale")
    state = fields.Selection([('initialiser','Initialisation'),('confirmer','Confirmer')], 'Statut',compute="_compute_state", required=True, readonly=True, default='initialiser')
    id_agence = fields.Many2one('mp.agence', string='Agence')
    montant_compte = fields.Float( string='Montant du compte', compute="_compute_montant_compte",)



    @api.onchange('name', 'id_agence')
    def _compute_montant_compte(self):

        for record in self :
            if record.state != 'initialiser' :
                cr = self._cr
                cr.execute("SELECT SUM(montant) FROM mp_operation where name = 'depot' and id_compte =" +str(record.id)+"")
                result = cr.fetchall()
                depot = result[0][0]

                cr.execute("SELECT SUM(montant) FROM mp_operation_site  where name = 'depot' and id_compte =" +str(record.id)+"")
                result = cr.fetchall()
                virement_depot = result[0][0]
                if depot ==None or virement_depot ==None:
                    if depot == None:
                        depot = 0
                    if virement_depot == None:
                        virement_depot = 0
                init = int(record.montant_init)
                res = init - virement_depot + depot
                record.montant_compte = res
            else:
                record.montant_compte =0

    @api.depends('name')
    def _compute_state(self):
        self.write({'state':'confirmer'})