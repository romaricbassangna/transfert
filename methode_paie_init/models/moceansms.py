# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from odoo.exceptions import UserError, ValidationError
import requests
import time
import logging

#logging.basicConfig(filename="E:/moceansms.log")
#_logger = logging.getLogger(__name__)


class SMSConnection (models.Model):
    _name = "moceansms.smsconnection"

    name = fields.Char(string='Connection Name', required=True, size=100)
    api_key = fields.Text(string='API Key', required=True,
                          help='mocean-api-key')
    api_secret = fields.Text(
        string='API Secret', required=True, help='mocean-api-secret')
    sender_name = fields.Char(string='Sender Name',
                              required=True, size=100, help='mocean-from')
    history_id = fields.One2many(
        'moceansms.smshistory', 'connection_id', "History")
    queue_line = fields.One2many(
        "mp.transfert", "connection_id", readonly=True)


class SMSHistory(models.Model):
    _name = "moceansms.smshistory"
    connection_id = fields.Many2one(
        'moceansms.smsconnection', 'Connection', ondelete='set null')
    recipient = fields.Text(string="Recipient", required=True)
    message = fields.Text(string="Message", required=True)
    state = fields.Char(size=10, string="status")
    sent_time = fields.Datetime(
        'Action Time', readonly=True,  default=fields.Datetime.now())
    user_id = fields.Many2one("res.users", "Username")


