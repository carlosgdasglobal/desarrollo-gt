# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import date

class AccountJournalReportWizard(models.TransientModel):
    _name = 'account.journal.report.wizard'
    _description = 'wizard del libro diario'

    date_from = fields.Date('Desde', required=True)
    date_to = fields.Date('Hasta', required=True, default=lambda x: date.today())

    @api.multi
    def generate_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_from': self.date_from,
                'date_to': self.date_to
            }
        }
        return self.env.ref('account_report_custom.account_journal_report_main').report_action(self, data=data)
