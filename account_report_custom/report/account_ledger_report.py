# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
import dateutil


class AccountLedgerReport(models.AbstractModel):
    _name = 'report.account_report_custom.account_ledger_report'
    _description = 'Generación del libro mayor'

    def change_to_positive(self, value):
        if value >= 0:
            return value
        else:
            return value * -1

    @api.model
    def _get_report_values(self, docids, data):
        data = data['data']['form']
        date_from = fields.Date.from_string(data.get('date_from'))
        date_to = fields.Date.from_string(data.get('date_to'))
        res = {}
        account_id = self.env['account.account'].search([])
        for account in account_id:
            account_name = account.name.upper()
            total_debit = 0
            total_credit = 0
            saldo = 0
            account_move_line = self.env['account.move.line'].search(
                [('account_id', '=', account.id), ('date', '>=', date_from), ('date', '<=', date_to)], order='date asc')
            if account_move_line:
                for account_line in account_move_line:
                    fecha = str(account_line.date)
                    fecha = dateutil.parser.parse(fecha)
                    fecha = fecha.strftime('%d/%m/%Y')
                    total_debit += account_line.debit
                    total_credit += account_line.credit
                    if total_debit > total_credit:
                        name_balance = 'Saldo Deudor'
                    else:
                        name_balance = 'Saldo Acreedor'
                    total = total_debit - total_credit
                    if account_name not in res:
                        saldo = account_line.debit - account_line.credit
                        res.update({
                            account_name: {
                                'name': account_name,
                                'code': account.code,
                                'total_debit': total_debit,
                                'total_credit': total_credit,
                                'total': self.change_to_positive(total),
                                'name_balance': name_balance,
                                'value': [{
                                    'name': account_line.report_item,
                                    'fecha': fecha,
                                    'debit': account_line.debit,
                                    'credit': account_line.credit,
                                    'saldo': self.change_to_positive(saldo),
                                }]
                            }
                        })
                    else:
                        if account_line.debit != 0:
                            saldo += account_line.debit
                        else:
                            saldo -= account_line.credit
                        res[account_name]['total_debit'] = total_debit
                        res[account_name]['total_credit'] = total_credit
                        res[account_name]['total'] = self.change_to_positive(total)
                        res[account_name]['name_balance'] = name_balance
                        exist = False
                        for item in res[account_name]['value']:
                            if item['name'] == account_line.report_item:
                                exist = True
                                item['debit'] += account_line.debit
                                item['credit'] += account_line.credit
                                item['saldo'] = self.change_to_positive(saldo)
                        if not exist:
                            res[account_name]['value'].append({
                                    'name': account_line.report_item,
                                    'fecha': fecha,
                                    'debit': account_line.debit,
                                    'credit': account_line.credit,
                                    'saldo': self.change_to_positive(saldo)
                                })
        res_list = sorted(res.items())
        docargs = {
                'doc_ids': docids,
                'docs': self.env['account.invoice'].sudo().browse(1),
                'de_account': res_list,
                'fecha_inicio': date_from,
                'fecha_final': date_to,
        }
        return docargs

