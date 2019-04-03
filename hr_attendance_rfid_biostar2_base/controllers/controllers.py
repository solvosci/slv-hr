# -*- coding: utf-8 -*-
from odoo import http

# class HrAttendanceRfidBiostar2Base(http.Controller):
#     @http.route('/hr_attendance_rfid_biostar2_base/hr_attendance_rfid_biostar2_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_attendance_rfid_biostar2_base/hr_attendance_rfid_biostar2_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_attendance_rfid_biostar2_base.listing', {
#             'root': '/hr_attendance_rfid_biostar2_base/hr_attendance_rfid_biostar2_base',
#             'objects': http.request.env['hr_attendance_rfid_biostar2_base.hr_attendance_rfid_biostar2_base'].search([]),
#         })

#     @http.route('/hr_attendance_rfid_biostar2_base/hr_attendance_rfid_biostar2_base/objects/<model("hr_attendance_rfid_biostar2_base.hr_attendance_rfid_biostar2_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_attendance_rfid_biostar2_base.object', {
#             'object': obj
#         })