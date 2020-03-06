# -*- coding: utf-8 -*-

from odoo import _, api, models
from collections import OrderedDict
from datetime import date, datetime

class TaxBookReport(models.AbstractModel):
    _name = 'report.account_report_custom.tax_book_report'
    _description = 'Generación del libro de Compras/Ventas'

    @api.model
    def _get_report_values(self, docids, data=None):
        ids = data.get('ids')
        model = data.get('model')
        docs = self.env[model].browse(ids)

        return {
            'doc_ids': ids,
            'doc_model': model,
            'docs': docs
        }
