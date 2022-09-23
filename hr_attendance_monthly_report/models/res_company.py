# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    customer_account_code = fields.Char()
    subtitle_attendance_monthly = fields.Char()
