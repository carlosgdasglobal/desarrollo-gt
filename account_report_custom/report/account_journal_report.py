# -*- coding: utf-8 -*-

from odoo import _, api, models
from collections import OrderedDict
from datetime import date, datetime
import locale

class AccountJournalReport(models.AbstractModel):
    _name = 'report.account_report_custom.account_journal_report'
    _description = 'Generación del libro diario'

    def date_format(self, date):
        locale.setlocale(locale.LC_ALL, 'es_GT.utf8')
        return date.strftime('%d/%b/%Y')

    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = datetime.strptime(data['form']['date_from'], '%Y-%m-%d')
        date_to = datetime.strptime(data['form']['date_to'], '%Y-%m-%d')
        currency = self.env.user.company_id.currency_id
        docs = OrderedDict()
        account_move_line = self.env['account.move.line'].search([('date', '>=', date_from), ('date', '<=', date_to)],
                                                                 order='date asc, account_id asc')
        item = 0
        for line in account_move_line:
            date = line.date
            date_string = str(date)
            if date_string not in docs:
                item += 1
                docs[date_string] = {
                    'date': date,
                    'item': item,
                    'debit_lines': [],
                    'credit_lines': []
                }
            exist = False
            if line.debit != 0:
                line_type = 'debit_lines'
            else:
                line_type = 'credit_lines'
            for account_line in docs[date_string][line_type]:
                if line.account_id.code in account_line.values():
                    account_line['account_debit'] += line.debit
                    account_line['account_credit'] += line.credit
                    exist = True
                    break

            if not exist:
                docs[date_string][line_type].append(
                    {
                        'account_code': line.account_id.code,
                        'account_name': line.account_id.name,
                        'account_debit': line.debit,
                        'account_credit': line.credit
                    }
                )

            line.write({
                'report_item': item
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_from': date_from,
            'date_to': date_to,
            'currency': currency,
            'docs': docs,
            'report': self
        }
