from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SearchTransfert(models.Model):
    _name = 'mp.search_transfert'

    token_transfert = fields.Char(string="Clé de transfert")
    nom_beneficiaire = fields.Char(string="Nom bénéficiaire")

    @api.constrains()
    def search_transfert(self,context=None):
        id_user = self.env.uid
        agence = self.env['res.partner'].search([('id', '=', id_user)])
        transfert = self.env['mp.transfert'].search([('token', '=', self.token_transfert ),
                                                    ('id_beneficiaire.name', '=', self.nom_beneficiaire),
                                                     ('state1', '=', 'envoye'),
                                                     ('id_agence_arrive', '=', agence.id_agence.id)])

        if transfert.id:

            return {
                'name': _('Retrait'),
                'view_mode': 'form',
                'res_model': 'mp.transfert',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'views': [[False, 'list'], [False, 'form']],
                'domain': [('id', '=', transfert.id)],
            }
        else:
            raise ValidationError("Identifiant incorrecte ou transaction inexistante")

