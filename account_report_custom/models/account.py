# *.* coding: utf-8 -*-
# Comentario de prueba

from odoo import api, fields, models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    report_item = fields.Integer('Partida')


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    invoice_number_id = fields.Integer(string='Número de factura', size=20)
    serie = fields.Integer(string='Serie', size=10)
