from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SearchTransfertRevendication(models.Model):
    _name = 'mp.search_transfert_revendication'

    token_transfert = fields.Char(string="Clé de transfert")
    nom_expediteur = fields.Char(string="Nom expéditeur")

    @api.constrains()
    def search_transfert(self,context=None):
        id_user = self.env.uid
        agence = self.env['res.partner'].search([('id', '=', id_user)])
        transfert = self.env['mp.transfert'].search([('token', '=', self.token_transfert ),
                                                    ('id_expediteur.name', '=', self.nom_expediteur),
                                                     ('id_agence_arrive', '=', agence.id_agence.id)])

        if transfert.id:

            return {
                'name': _('Retrait'),
                'view_mode': 'form',
                'res_model': 'mp.transfert',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'views': [[False, 'list'], [True, 'form']],
                'domain': [('id', '=', transfert.id)],
            }
        else:
            raise ValidationError("Identifiant incorrecte ou transaction non existante")

