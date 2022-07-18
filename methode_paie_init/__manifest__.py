# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Methode de paiement',
    'category': 'paie',
    'description': """
    'version': '1.0',
The module adds Microsoft user in res user.
===========================================
""",
    'depends': ['base_setup'],
    'data': [
        'views/client_view.xml',
        'views/transfert_view.xml',
        'views/search_transfert_view.xml',
        'views/search_transfert_revendication_view.xml',
        'views/compte_client_view.xml',
        'views/moceansms.xml',

        'wizard/ville_view.xml',
        'wizard/tarif_view.xml',
        'wizard/type_piece_identite_view.xml',
        'wizard/compte_view.xml',
        'wizard/agence_view.xml',
        'wizard/taxes_view.xml',

        'moceansms_data.xml',
        'mp_menu.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
