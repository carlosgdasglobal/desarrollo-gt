# -*- coding: utf-8 -*-

{
    'name': 'Reportes Contables Personalizados',
    'author': 'Andy quijada / Kelvis pernia ',
    'version': '1.0',
    'summary': 'Invoices & Payments',
    'description': """
        Formatos personalizados para reportes contables
    """,
    'category': 'account',
    'depends': ['account', 'account_accountant', 'web'],
    'data': [
        'report/account_journal_report_view.xml',
        'report/account_ledger_report_view.xml',
        'report/tax_book_report_view.xml',
        'report/report_data.xml',
        'wizard/account_journal_report_wizard_view.xml',
        'wizard/account_ledger_report_wizard_view.xml',
        'views/account_invoice_view.xml',
        'views/tax_book_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
