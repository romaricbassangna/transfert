# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import uuid
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
import requests
import time
import logging

logging.basicConfig(filename="E:/moceansms.log")
_logger = logging.getLogger(__name__)

class Transfert(models.Model):
    _name = 'mp.transfert'

    name = fields.Char(string="Libellé transfert",default="", compute="_compute_name")
    token = fields.Char(string="Clé de transfert")
    montant = fields.Integer(string="Montant du transfert",)
    commission = fields.Float(string="Commission", compute="_compute_commission")
    id_expediteur = fields.Many2one('mp.client', string="Nom Expéditeur")
    id_beneficiaire = fields.Many2one('mp.client', string="Nom Bénéficiaire")
    id_tarif = fields.Many2one('mp.tarif', string="Tarif", compute="_compute_id_tarif")
    id_agence_depart = fields.Many2one('mp.agence', string="Agence depart", compute="_compute_id_agence_depart")
    id_agence_arrive = fields.Many2one('mp.agence', string="Agence arrivée")
    state1 = fields.Selection([('draft','Brouillon'),('envoye','Envoyé'),('retirer','Retirer')], 'Statut', required=True, readonly=True, default='draft')
    date_transfert = fields.Date(string="Date d'envoi", default=datetime.today(), required=True)
    montant_total = fields.Float(string="Montant Total", compute="_compute_montant_total")
    date_retrait = fields.Date(string='Date de retrait')

    name_beneficiaire = fields.Char(related='id_beneficiaire.name', store=True, string="name beneficiaire")
    prenom_beneficiaire = fields.Char(related='id_beneficiaire.prenom', store=True, string="prenom ")
    nationatile_beneficiaire = fields.Many2one(related='id_beneficiaire.nationatile', store=True, string="nationatile")
    tel_beneficiaire = fields.Char(related='id_beneficiaire.tel', store=True, string="N° téléphone")
    id_piece_iden_beneficiaire = fields.Many2one(related='id_beneficiaire.id_piece_iden', store=True, string="pièce d'identité")
    num_piece_beneficiaire = fields.Char(related='id_beneficiaire.num_piece',store=True,  string="N° Pièce d'identité ")
    Sexe_beneficiaire = fields.Selection(related='id_beneficiaire.sexe',store=True, string="Sexe beneficiaire")
    date_delivrance_piece_id_beneficiaire = fields.Date(related='id_beneficiaire.date_delivrance_piece_id',store=True,  string="Date delivrance ID")
    date_expiration_piece_id_beneficiaire = fields.Date(related='id_beneficiaire.date_expiration_piece_id',store=True,  string="Date expiration ID")

    name_expediteur = fields.Char(related='id_expediteur.name',store=True,  string="name expediteur")
    prenom_expediteur = fields.Char(related='id_expediteur.prenom',store=True, string="prenom ")
    nationatile_expediteur= fields.Many2one(related='id_expediteur.nationatile',store=True, string="nationatile")
    tel_expediteur= fields.Char(related='id_expediteur.tel', store=True, string="N° téléphone ")
    id_piece_iden_expediteur = fields.Many2one(related='id_expediteur.id_piece_iden', store=True, string="pièce d'identité")
    num_piece_expediteur = fields.Char(related='id_expediteur.num_piece',store=True, string="N° Pièce d'identité")
    Sexe_expediteur = fields.Selection(related='id_expediteur.sexe',store=True,  string="Sexe")
    date_delivrance_piece_id_expediteur = fields.Date(related='id_expediteur.date_delivrance_piece_id',store=True,  string="Date delivrance ID")
    date_expiration_piece_id_expediteur = fields.Date(related='id_expediteur.date_expiration_piece_id',store=True,  string="Date expiration ID")

    id_ville_depart = fields.Many2one('mp.ville', string='Ville départ', compute="_compute_id_ville_depart")
    id_ville_arrive = fields.Many2one('mp.ville', string="Ville d'arrivée", required=True)


    action_time = fields.Datetime(
        'Action Time', readonly=True,  default=fields.Datetime.now())
    message = fields.Text(string="Message", compute="_message_envoie")
    recipient = fields.Text(string="Recipient", compute="_numtelephone_envoie" ,help="Allow send to multiple recipient. Put (,) in between phone number.")
    connection_id = fields.Many2one("moceansms.smsconnection",  String="Connection", compute='_compute_id_connection')
    id_pays_arrive2= fields.Char(string="Pays d'arrivé", related="id_ville_arrive.name")



    state = fields.Selection([
        ('draft', 'Queued'),
        ('sending', 'Waiting'),
        ('send', 'Sent'),
        ('error', 'Error'),
    ],
        'Message Status',
        readonly=True,
        default='draft'
    )

    user_id = fields.Many2one(
        'res.users', string='Username', default=lambda self: self.env.user)
    reserve_key = fields.Char(size=30)
    send_to_all = fields.Boolean(default=False)

    @api.onchange('montant', 'id_ville_arrive')
    def _compute_id_connection(self):
        cr =self._cr
        id_user = self.env.uid
        cr.execute('select moceansms_smsconnection.id from moceansms_smsconnection '
                    'where moceansms_smsconnection.id = ' +str(id_user)+'')
        result = cr.fetchall()
        id_connection = result[0][0]
        for record in self:
            record.connection_id = id_connection

    @api.onchange('montant', 'nom_beneficiaire')
    def _message_envoie(self):
        #self.message = 'Bonjour vour reçcu un tranfert de la Bange Bank'
        if self.state1=="envoye":
            tk =self.token
            nom =self.nom_beneficiaire
            temps=self.action_time

            self.message= "M "+nom+" vous a envoyé un transfert Bange Bank M .. à ..... au \n Num "+tk+"\n"+str(fields.Datetime.now())+"."+"\n Bange Bank Votre banque de confiance."
        elif self.state1 == "retirer":
            nom2 = self.nom_expediteur
            self.message= "M "+nom2+" a un retrait de votre part à la Bange Bank à "+str(fields.Datetime.now())+"."+"\n Bange Bank Votre banque de confiance."
        else:
            self.message= ''

    @api.onchange('montant', 'nom_beneficiaire')
    def _numtelephone_envoie(self):
        #tel = self.env['mp.client'].search([(self.id_beneficiaire,  "=", self.id_beneficiaire.tel)])
        tel = self.tel_beneficiaire
        pays = self.id_pays_arrive2

        if pays == "Cameroun":
            self.recipient="237"+str(tel)
        elif pays == "Guinnée Equatoriale":
            self.recipient = "237"+str(tel)
        else:
            self.recipient = "237" + str(tel)

    def cron_sms(self):

        unique_key = time.time()
        self.env["mp.transfert"].search([("state", "=", "draft")]).write(
            {"reserve_key": unique_key, "state": "sending"})

        pending_sms = self.env["mp.transfert"].search(
            [("reserve_key", "=", unique_key)])


        for sms in pending_sms:

            params = {
                "mocean-api-key": sms.connection_id.api_key,
                "mocean-api-secret": sms.connection_id.api_secret,
                "mocean-from": sms.connection_id.sender_name,
                "mocean-to": sms.recipient,
                "mocean-text": sms.message,
                "mocean-resp-format": "JSON",
                "mocean-medium": "odoo"
            }

            if self.send(params) == True:
                params["state"] = "sent"
            else:
                params["state"] = "error"

            params["connection_id"] = sms.connection_id.id
            params["user_id"] = sms.user_id.id

            self.history(params, sms.connection_id)
            self.env["mp.transfert"].search(
                [("id", "=", sms.id)]).unlink()

    def send(self, data):
        url = 'https://rest.moceanapi.com/rest/2/sms'

        try:
            res = requests.post(url, data=data)
            res_data = res.json()
            if str(res.status_code) != "202":
                _logger.error("Fail to send sms due to %s" %
                              (res_data.err_msg))
                return False
        except Exception as e:
            _logger.error("Fail to send sms due to %s" % (e))
            return False
        return True

    def history(self, data, connection_id):
        self.env["moceansms.smshistory"].create({
            "recipient": data["mocean-to"],
            "message": data["mocean-text"],
            "state": data["state"],
            "connection_id": data["connection_id"],
            "user_id": data["user_id"]
        })
        return True

    def cron_mark_sms_expire(self):

        queue_sms = self.env["mp.transfert"].search(
            [("reserve_key", "!=", "")])
        current_time = time.time()

        for sms in queue_sms:

            expire_time = float(sms.reserve_key) + float("86400")

            if current_time > expire_time:
                self.env["mp.transfert"].search(
                    ["id", "=", sms.id]).unlink()

                self.history(
                    {
                        "mocean-to": sms.recipient,
                        "mocean-text": sms.message,
                        "user_id": sms.user_id,
                        "connection_id": sms.connction_id,
                        "state": "error"
                    }
                )

    @api.onchange('montant')
    def onchange_montant(self):

        cr =self._cr
        id_user = self.env.uid
        cr.execute( 'select res_country.id, mp_a.id, mp_v.id  from res_country '
                    'inner join mp_ville mp_v on mp_v.id_pays = res_country.id '
                    'inner join mp_agence mp_a on mp_a.id_ville = mp_v.id '
                    'inner join res_partner rp on rp.id_agence = mp_a.id '
                    'where rp.id =  ' +str(id_user)+'')
        result = cr.fetchall()
        id_depart = result[0][0]
        id_agence = result[0][1]
        id_ville_depart = result[0][2]


        if self.montant != 0:
                cr.execute( 'select res_country.id from res_country '
                        'inner join mp_ville mp_v on mp_v.id_pays = res_country.id '
                        'inner join mp_agence mp_a on mp_a.id_ville = mp_v.id '
                        'where mp_v.id =  ' +str(self.id_ville_arrive.id)+'')

                id_arrive = result[0][0]
                cr.execute( 'select id,commission,mode_calcul from mp_tarif where montant_min <= '+"'"+str(self.montant)+"'"+' AND montant_max >= '+"'"+str(self.montant)+"'"+' AND id_pays_depart =  ' +str(id_depart)+' AND id_pays_arrive =  ' +str(id_arrive)+' AND active = True')
                result = cr.fetchall()
                if result !=[]:
                    id_tarif = result[0][0]
                    new_commission = result[0][1]
                    mode_calcul = result[0][2]
                    if mode_calcul == 'montant_fixe':
                        new_montant = self.montant - new_commission
                    else:
                        new_montant = self.montant * new_commission * 0.01
                        new_montant = self.montant - new_montant
                    self.write({'id_tarif': id_tarif,'montant':new_montant,})
                    self.write({'commission': new_commission})
        else:
                self.write({'id_agence_depart': id_agence, 'id_ville_arrive': id_ville_depart,'id_ville_depart': id_ville_depart})


    @api.depends('id_expediteur.name','id_beneficiaire.name')
    def _compute_name(self):
        for record in self:
            rr = record.id_expediteur.name
            if record.id_expediteur.name == False or record.id_beneficiaire.name == False  :
                if record.id_expediteur.name == False :
                    record.name =str(record.id_beneficiaire.name)
                if record.id_beneficiaire.name == False :
                    record.name = str(record.id_expediteur.name)
            else:
                record.name = str(record.id_expediteur.name)+ "-" +str(record.id_beneficiaire.name)


    @api.depends('montant', 'id_ville_arrive')
    def _compute_commission(self):
        cr =self._cr
        id_user = self.env.uid
        cr.execute( 'select res_country.id from res_country '
                    'inner join mp_ville mp_v on mp_v.id_pays = res_country.id '
                    'inner join mp_agence mp_a on mp_a.id_ville = mp_v.id '
                    'inner join res_partner rp on rp.id_agence = mp_a.id '
                    'where rp.id =  ' +str(id_user)+'')
        result = cr.fetchall()
        id_depart = result[0][0]
        for record in self:
                if record.id_ville_arrive.id != False :

                    cr.execute( 'select res_country.id from res_country '
                                'inner join mp_ville mp_v on mp_v.id_pays = res_country.id '
                                'inner join mp_agence mp_a on mp_a.id_ville = mp_v.id '
                                'where mp_v.id =  ' +str(record.id_ville_arrive.id)+'')
                    result = cr.fetchall()
                    id_arrive = result[0][0]
                    cr.execute( 'select commission from mp_tarif where montant_min <= '+"'"+str(record.montant)+"'"+' AND montant_max >= '+"'"+str(record.montant)+"'"+' AND id_pays_depart =  ' +str(id_depart)+' AND id_pays_arrive =  ' +str(id_arrive)+' AND active = True')
                    result = cr.fetchall()
                    if result !=[]:
                        commission = result[0][0]
                        record.commission = commission
                    else:
                        record.commission = 0
                else:
                    record.commission = 0


    @api.depends('id_ville_depart')
    def _compute_id_ville_depart(self):
        cr =self._cr
        id_user = self.env.uid
        cr.execute( 'select mp_v.id from mp_ville mp_v '
                    'inner join mp_agence mp_a on mp_a.id_ville = mp_v.id '
                    'inner join res_partner rp on rp.id_agence = mp_a.id '
                    'where rp.id =  ' +str(id_user)+'')
        result = cr.fetchall()
        id_depart = result[0][0]

        for record in self:
            record.id_ville_depart = id_depart



    @api.depends('montant', 'id_ville_arrive')
    def _compute_id_tarif(self):
        cr =self._cr
        id_user = self.env.uid
        cr.execute( 'select res_country.id from res_country '
                    'inner join mp_ville mp_v on mp_v.id_pays = res_country.id '
                    'inner join mp_agence mp_a on mp_a.id_ville = mp_v.id '
                    'inner join res_partner rp on rp.id_agence = mp_a.id '
                    'where rp.id =  ' +str(id_user)+'')
        result = cr.fetchall()
        id_depart = result[0][0]

        for record in self:
            if record.id_ville_arrive.id != False:
                cr.execute( 'select res_country.id from res_country '
                            'inner join mp_ville mp_v on mp_v.id_pays = res_country.id '
                            'inner join mp_agence mp_a on mp_a.id_ville = mp_v.id '
                            'where mp_v.id =  ' +str(record.id_ville_arrive.id)+'')
                id_arrive = result[0][0]

                cr.execute( 'select id from mp_tarif where montant_min <= '+"'"+str(record.montant)+"'"+' AND montant_max >= '+"'"+str(record.montant)+"'"+' AND id_pays_depart =  ' +str(id_depart)+' AND id_pays_arrive =  ' +str(id_arrive)+' AND active = True')
                result = cr.fetchall()
                if result !=[]:
                    id_tarif = result[0][0]
                    record.id_tarif = id_tarif
                else:
                    cr.execute( 'SELECT id FROM mp_tarif WHERE active = True ORDER BY id DESC LIMIT 1')
                    result = cr.fetchall()
                    id_tarif = result[0][0]
                    record.id_tarif = id_tarif
            else:
                cr.execute( 'SELECT id FROM mp_tarif WHERE active = True ORDER BY id DESC LIMIT 1')
                result = cr.fetchall()
                id_tarif = result[0][0]
                self.id_tarif = id_tarif



    @api.depends('id_expediteur.name')
    def _compute_id_agence_depart(self):
        cr =self._cr
        id_user = self.env.uid
        cr.execute( 'select mp_a.id from res_country '
                    'inner join mp_ville mp_v on mp_v.id_pays = res_country.id '
                    'inner join mp_agence mp_a on mp_a.id_ville = mp_v.id '
                    'inner join res_partner rp on rp.id_agence = mp_a.id '
                    'where rp.id =  ' +str(id_user)+'')
        result = cr.fetchall()
        id_agence = result[0][0]
        for record in self:
            record.id_agence_depart = id_agence


    @api.depends('commission','montant', 'id_ville_arrive')
    def _compute_montant_total(self):
        cr = self._cr
        id_user = self.env.uid
        if self.id_ville_arrive.id != False :
            tt = self.id_ville_arrive
            cr.execute( 'select res_country.id from res_country '
                        'inner join mp_ville mp_v on mp_v.id_pays = res_country.id '
                        'where mp_v.id =  ' +str(self.id_ville_arrive.id)+'')
            result = cr.fetchall()
            id_arrive = result[0][0]
            for record in self:

                    cr.execute( 'select res_country.id from res_country '
                                'inner join mp_ville mp_v on mp_v.id_pays = res_country.id '
                                'inner join mp_agence mp_a on mp_a.id_ville = mp_v.id '
                                'inner join res_partner rp on rp.id_agence = mp_a.id '
                                'where rp.id =  ' +str(id_user)+'')
                    result = cr.fetchall()
                    id_depart = result[0][0]

                    cr.execute( 'select mode_calcul from mp_tarif where montant_min <= '+"'"+str(record.montant)+"'"+' AND montant_max >= '+"'"+str(record.montant)+"'"+' AND id_pays_depart =  ' +str(id_depart)+' AND id_pays_arrive =  ' +str(id_arrive)+' AND active = True')
                    result = cr.fetchall()
                    if result !=[]:
                        mode_calcul = result[0][0]
                        if mode_calcul == 'montant_fixe':
                            commission_t = 0.02
                            commission_t = 1 - commission_t
                            taux = record.montant / commission_t
                            new_montant = record.montant + record.commission
                        else:
                            commission_t = record.commission*0.01
                            commission_t = 1 - commission_t
                            new_montant = record.montant / commission_t

                        record.montant_total = new_montant
                    else:
                        record.montant_total=0
        else:
            self.montant_total=0


    @api.onchange('tel_beneficiaire')
    def onchange_tel_beneficiaire(self):

        cr =self._cr
        id_user = self.env.uid
        for record in self:
            if record.tel_beneficiaire != False:
                cr.execute( 'select id from mp_client '
                            'where tel =  '+"'"+str(record.tel_beneficiaire)+"'"+'')
                result = cr.fetchall()
                if result != [] :
                    self.write({'id_beneficiaire':result[0][0]})

    @api.onchange('tel_expediteur')
    def onchange_tel_beneficiaire(self):

        cr =self._cr
        id_user = self.env.uid
        for record in self:
            if record.tel_expediteur != False:
                cr.execute( 'select id from mp_client '
                            'where tel =  '+"'"+str(record.tel_expediteur)+"'"+'')
                result = cr.fetchall()
                if result != [] :
                    self.write({'id_expediteur':result[0][0]})

    @api.onchange('id_piece_iden_expediteur', 'num_piece_expediteur')
    def onchange_num_piece_exp(self):

        cr =self._cr
        id_user = self.env.uid
        for record in self:
            if record.id_piece_iden_expediteur.id != False :
                cr.execute( 'select id from mp_client '
                            'where id_piece_iden =  ' +str(record.id_piece_iden_expediteur.id)+' '
                            'and  num_piece = '+"'"+(record.num_piece_expediteur)+"'"+'')
                result = cr.fetchall()
                if result != [] :
                    self.write({'id_expediteur':result[0][0]})


    @api.onchange('id_piece_iden_beneficiaire', 'num_piece_beneficiaire')
    def onchange_num_piece_bene(self):

        cr =self._cr
        id_user = self.env.uid
        for record in self:
            if record.id_piece_iden_beneficiaire.id != False :
                cr.execute( 'select id from mp_client '
                            'where id_piece_iden =  ' +str(record.id_piece_iden_beneficiaire.id)+' '
                            'and  num_piece = '+"'"+str(record.num_piece_beneficiaire)+"'"+'')
                result = cr.fetchall()
                if result != [] :
                    self.write({'id_beneficiaire':result[0][0]})


    @api.onchange('id_ville_arrive')
    def onchange_id_agence_arrive(self):
        for record in self:
            if record.id_agence_arrive != False:
                record.id_agence_arrive = False



    @api.constrains()
    def envoyer(self, context=None):
        #on recupere l'id de l'utilisateur conneecté
        id_user = self.env.uid
        cr =self._cr
        #requette pour recuperer l'id du compte de l'agence
        cr.execute( 'select mp_compte.id from mp_compte '
                    'inner join mp_agence mp_a on mp_compte.id_agence = mp_a.id  '
                    'where mp_a.id ='+str(self.id_agence_depart.id)+'')
        result = cr.fetchall()
        id_compte = result[0][0]

        #requette pour récupérer l'id du pays de départ
        cr.execute( 'select res_country.id from res_country '
                                'inner join mp_ville mp_v on mp_v.id_pays = res_country.id '
                                'inner join mp_agence mp_a on mp_a.id_ville = mp_v.id '
                                'inner join res_partner rp on rp.id_agence = mp_a.id '
                                'where rp.id =  ' +str(id_user)+'')
        result = cr.fetchall()
        id_depart = result[0][0]

        #requette pour récupére les information sur le compte du client
        compte_client = self.env['mp.compte_client'].search([('id_client', '=', self.id_expediteur.id )])

        #test si le compte du client n'existe pas
        if not compte_client.id:
            #si le compte du client n'exite pas on crée son compte
            mp_operation = self.env['mp.compte_client'].create({
                'id_client': self.id_expediteur.id,
            })
            #requette pour recupérer les information sir le compte du client
            compte_client = self.env['mp.compte_client'].search([('id_client', '=', self.id_expediteur.id )])

        #On crédite le compte du client
        mp_operation_client_agence = self.env['mp.operation_client_compte'].create({
            'name': 'credit',
            'montant': self.montant_total,
            'id_compte': compte_client.id,
        })

        #On debit le compte du client
        mp_operation_client_agence = self.env['mp.operation_client_compte'].create({
            'name': 'debit',
            'montant': self.montant_total,
            'id_compte': compte_client.id,
        })

        #requette pour recupérer les information sur la taxe
        taxe = self.env['mp.taxe'].search([('id_pays', '=', id_depart ),('active', '=', True),])
        valeur_taxe = 0
        #on vérifie s'il y'a une taxe de transfert d'argent pour ce pays
        if taxe.id:
            valeur_taxe = self.montant_total * taxe.valeur_taxe * 0.01

        #on credit le compte de l'agence
        mp_operation_client_agence = self.env['mp.operation_client_agence'].create({
            'name': 'credit',
            'id_compte_client': compte_client.id,
            'montant': self.montant_total,
            'id_compte_agence': id_compte,
            'taxe': valeur_taxe,
            'id_transfert': self.id,
        })



        compte_agence = self.env['mp.compte'].search([('id_agence', '=', self.id_agence_arrive.id )])

        #on debit le compte de l'agence de depart
        mp_operation_agence = self.env['mp.operation_compte'].create({
            'name': 'debit',
            'montant': self.montant,
            'id_compte_depart': id_compte,
            'id_compte_arrive': compte_agence.id,
            'id_transfert': self.id,
        })

        #on crédit le compte de l'agence d'arrivée
        mp_operation_agence = self.env['mp.operation_compte'].create({
            'name': 'credit',
            'montant': self.montant,
            'id_compte_depart': id_compte,
            'id_compte_arrive': compte_agence.id,
            'id_transfert': self.id,
        })
        tok = uuid.uuid4().hex
        self.write({'token':tok})
        self.write({'state1':'envoye'})

    @api.constrains()
    def annuler_envoi(self,context=None):
        """self.write({'state1':'draft'})
        self.write({'token':''})"""
        raise ValidationError("Cette fonctionnalité en cour de développement !")

    @api.constrains('id_beneficiaire.num_piece','id_beneficiaire.id_piece_iden')
    def retrait(self, context=None):
        id_transfert = self.id
        cr =self._cr
        cr.execute( 'select mp_client.num_piece,mp_client.id_piece_iden from mp_client '
                    'inner join mp_transfert mp_t on mp_t.id_beneficiaire = mp_client.id '
                    'where mp_t.id =  ' +str(id_transfert)+'')
        result = cr.fetchall()
        if result[0][0] == None or result[0][1] == None:
            raise ValidationError("Champs non remplis, veillez entrer les information sur le type de pièce d'identification")
        else:
            date_actu = datetime.today()
            date_actu = date_actu.date()
            date_expi= self.date_expiration_piece_id_beneficiaire
            if date_expi >= date_actu :
                id_user = self.env.uid
                cr =self._cr
                cr.execute( 'select mp_c.id from res_country '
                            'inner join mp_ville mp_v on mp_v.id_pays = res_country.id  '
                            'inner join mp_agence mp_a on mp_a.id_ville = mp_v.id  '
                            'inner join mp_compte mp_c on mp_c.id_agence = mp_a.id '
                            'inner join res_partner rp on rp.id_agence = mp_a.id '
                            'where rp.id = '+str(id_user)+'')
                result = cr.fetchall()
                id_compte = result[0][0]

                #requette pour récupére les information sur le compte du client
                compte_client = self.env['mp.compte_client'].search([('id_client', '=', self.id_beneficiaire.id)])

                #test si le compte du client n'existe pas
                if not compte_client.id:
                    #si le compte du client n'exite pas on crée son compte
                    mp_operation = self.env['mp.compte_client'].create({
                        'id_client': self.id_beneficiaire.id,
                    })
                    #requette pour recupérer les information sir le compte du client
                    compte_client = self.env['mp.compte_client'].search([('id_client', '=', self.id_beneficiaire.id )])


                #on credit le compte client
                mp_operation_client_agence = self.env['mp.operation_client_agence'].create({
                    'name': 'credit',
                    'id_compte_client': compte_client.id,
                    'montant': self.montant_total,
                    'id_compte_agence': id_compte,
                    'taxe': 0,
                    'id_transfert': self.id,
                })

                #On crédite le compte du client
                mp_operation_client_agence = self.env['mp.operation_client_compte'].create({
                    'name': 'credit',
                    'montant': self.montant,
                    'id_compte': compte_client.id,
                })

                #On debite le compte du client
                mp_operation_client_agence = self.env['mp.operation_client_compte'].create({
                    'name': 'debit',
                    'montant': self.montant,
                    'id_compte': compte_client.id,
                })
                date = datetime.today()
                self.write({'date_retrait':date})
                self.write({'state1':'retirer'})
            else:
                raise ValidationError("Date validation de la pièce d'identification dépassée")
