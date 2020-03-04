# *.* coding: utf-8 -*-
# Comentario de prueba

from odoo import api, fields, models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    report_item = fields.Integer('Partida')