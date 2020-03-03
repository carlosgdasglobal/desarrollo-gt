# -*- coding: utf-8 -*-

from odoo import api, fields, models

class AccountJournalReportWizard(models.TransientModel):
    _name = 'account.journal.report.wizard'

    date_from = fields.Date('Desde', required=True)
    date_to = fields.Date('Hasta', required=True)

    @api.multi
    def generate_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_from': self.date_from.strftime('%d/%m/%Y'),
                'date_to': self.date_to.strftime('%d/%m/%Y')
            }
        }
        return self.env.ref('account_report_custom.account_journal_report').report_action(self, data=data)