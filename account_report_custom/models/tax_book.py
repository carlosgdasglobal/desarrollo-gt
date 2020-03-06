# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models
from odoo.tools.translate import _
import xlrd
import base64
import xlsxwriter
from io import BytesIO
from odoo.exceptions import UserError

class Taxbook(models.Model):
    _name = 'tax.book'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    state = fields.Selection([
        ('draft', 'Preparado'),
        ('done', 'Confirmado')], string='Status', default="draft")
    type = fields.Selection([
        ('in_invoice', 'Libro de compra'),
        ('out_invoice', 'Libro de venta')], string='type', default=lambda self: self._context.get('type'),
        force_save='True', readonly=True)
    name = fields.Char('Descripción', default=lambda x: _('Libro N°'), force_save='True')
    company_id = fields.Many2one('res.company', string='Compañia',
                                 default=lambda self: self.env['res.company'].search([('id', '=', 1)]).id,
                                 requiered=True)
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    datetime = fields.Datetime('Creation Date', default=fields.Datetime.now)
    user_id = fields.Many2one('res.users', "Responsible", track_visibility="onchange",
                              default=lambda self: self.env.uid)
    id_tax_book = fields.One2many('tax.book.line', 'id_tax_book', string='line')

    @api.multi
    def update_book(self):
        account_id = self.env['account.invoice']
        account = account_id.sudo().search([('type', '=', self.type), ('date_invoice', '>=', self.date_from),
                                            ('date_invoice', '<=', self.date_to), ('state','not in', ['draft'])], order='date asc')
        if account:
            for accoun in account:
                idp = 0
                tax = 0
                affected = 0
                amount_untaxed = 0
                if accoun.tax_line_ids:
                    for invoice_tax in accoun.tax_line_ids:
                        if invoice_tax.name == "IDP":
                            idp += invoice_tax.amount_total
                        else:
                            tax += invoice_tax.amount_total
                else:
                    affected = accoun.amount_total
                if self.type == 'out_invoice':
                    invoice_number_id = accoun.number
                else:
                    invoice_number_id = accoun.invoice_number_id
                amount_untaxed = accoun.amount_total - (idp + tax)
                self.id_tax_book.sudo().create({
                    'id_tax_book': self.id,
                    'invoice_id': accoun.id,
                    'type': self.type,
                    'idp': idp,
                    'affected': affected,
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': tax,
                    'invoice_number_id': invoice_number_id
                })

    @api.multi
    def delete_line(self):
        unlink = self.env['tax.book.line'].sudo().search([('id_tax_book', '=', self.id)])
        for unlink in unlink:
            self.env.cr.execute(""" DELETE FROM tax_book_line where id = %s """, (unlink.id,))

    @api.multi
    def done(self):
        if self:
            self.state = 'done'

    @api.multi
    def generate_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
        }
        return self.env.ref('account_report_custom.tax_book_report_main').report_action(self, data=data)

class Taxbookline(models.Model):
    _name = 'tax.book.line'
    id_tax_book = fields.Many2one('tax.book', string="DNI")
    id = fields.Integer('DNI')
    type = fields.Selection([
        ('in_invoice', 'Libro de compra'),
        ('out_invoice', 'Libro de venta')])
    date_invoice = fields.Date(string='Fecha', related='invoice_id.date_invoice',)
    partner_id = fields.Many2one('res.partner', 'Proveedor', readonly=True, related='invoice_id.partner_id')
    vat = fields.Char(related='partner_id.vat', string="Nit", readonly=True)
    invoice_id = fields.Many2one('account.invoice', string="Invoice", readonly=True)
    invoice_number_id = fields.Char(string='Número de factura', size=20)
    serie = fields.Char(string='Serie', size=10, related='invoice_id.serie')
    journal_currency_id = fields.Many2one('res.currency', string="Journal's Currency",
                                          related='invoice_id.currency_id',
                                          help='Utility field to express amount currency', readonly=True)
    amount_total = fields.Monetary(string='Base', related='invoice_id.amount_total',
                                   currency_field='journal_currency_id')
    idp = fields.Monetary(string='IDP', store=True, currency_field='journal_currency_id')
    affected = fields.Monetary(string='No Afecto', currency_field='journal_currency_id')
    amount_untaxed = fields.Monetary(string='Base', currency_field='journal_currency_id')
    amount_tax = fields.Monetary(string='Iva', currency_field='journal_currency_id')
    residual = fields.Monetary(string='Amount Due', currency_field='journal_currency_id', related='invoice_id.amount_total')

    @api.depends('idp', 'amount_tax')
    def _compute_affected(self):
        for rec in self:
            if not rec.idp and not rec.amount_tax:
                rec.affected = rec.amount_total
            else:
                rec.affected = 0
