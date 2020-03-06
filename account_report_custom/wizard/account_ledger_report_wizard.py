# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import date

class AccountLedgerReportWizard(models.TransientModel):
    _name = "account.ledger.report.wizard"
    _description = "Wizard para libro mayor"

    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date', default=lambda x: date.today())

    @api.multi
    def check_report(self):
        data = {}
        data['form'] = self.read(['date_from', 'date_to'])[0]
        return self.print_report(data)

    @api.multi
    def print_report(self, data):
        active_ids = self.env.context.get('active_ids', [])
        datas = {
            'ids': active_ids,
            'model': 'account.invoice',
            'data': data
        }
        return self.env.ref('account_report_custom.account_ledger_report_main').report_action([], data=datas)
