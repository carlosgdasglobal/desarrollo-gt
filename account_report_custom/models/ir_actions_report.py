# -*- coding: utf-8 -*-

from odoo import api, models

class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.model
    def _build_wkhtmltopdf_args(
            self,
            paperformat_id,
            landscape,
            specific_paperformat_args=None,
            set_viewport_size=False):
        command_args = super(IrActionsReport, self)._build_wkhtmltopdf_args(paperformat_id,
                                                                            landscape,
                                                                            specific_paperformat_args,
                                                                            set_viewport_size)
        return command_args
        command_args.extend(['--page-offset', '8'])
        return command_args