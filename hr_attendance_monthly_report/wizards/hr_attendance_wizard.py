# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields
from datetime import date, datetime, timedelta


class HrAttendanceWizard(models.TransientModel):
    _name = 'hr.attendance.wizard'

    employee_ids = fields.Many2many('hr.employee')
    month_year = fields.Datetime()

    def calculate_time(self, days, seconds):
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60 if ((seconds % 3600) // 60) >= 10 else "0%s" % ((seconds % 3600) // 60)
        seconds = (seconds % 60) if (seconds % 60) >= 10 else "0%s" % (seconds % 60)

        return "%s:%s:%s" % (hours, minutes, seconds)

    def generate_report_by_employee_month(self):
        hr_attendance_ids = self.env['hr.attendance']
        if not self.month_year.month == 12:
            last_day_month = date(self.month_year.year, self.month_year.month, 1).replace(month=self.month_year.month + 1) - timedelta(days=1)
        else:
            last_day_month = date(self.month_year.year, self.month_year.month, 1).replace(month=1)
            last_day_month = last_day_month.replace(year=self.month_year.year+1)
            last_day_month = last_day_month - timedelta(days=1)

        json = {
            'employee_ids': [],
            'company_name': self.env.company.name,
            'company_vat': self.env.company.vat,
            'company_ccc': self.env.company.customer_account_code,
            'company_subtitle': self.env.company.subtitle_attendance_monthly,
            'month': self.month_year.strftime('%B').capitalize(),
            'year': self.month_year.year,
            'lang': self.env.company.partner_id.lang
        }
        negative = True
        for employee in self.employee_ids:
            # If employee have a contract then hours_week from contract else employee
            date_contract = date(self.month_year.year, self.month_year.month, 1)
            # contract_id = employee.contract_ids.filtered(lambda x: x.date_start >= date_contract and (x.date_end == False or x.date_end <= date_contract))
            # if not contract_id:
            #     hours_week = employee.resource_calendar_id.name
            #     hours_day = employee.resource_calendar_id.hours_per_day
            # elif len(contract_id) == 1:
            #     hours_week = contract_id.resource_calendar_id.name
            #     hours_day = contract_id.resource_calendar_id.hours_per_day
            # else:
            #     hours_week = ""
            #     hours_day = employee.resource_calendar_id.hours_per_day
            #     pass
            ###################
            date_contract = fields.Date.context_today(self, fields.Datetime.to_datetime(date_contract))
            first_day = fields.Datetime.to_datetime(date_contract)
            if not self.month_year.month == 12:
                last_day = fields.Datetime.to_datetime(date_contract.replace(month=date_contract.month + 1))
            else:
                last_day = fields.Datetime.to_datetime(date_contract.replace(month=1))
                last_day = last_day.replace(year=date_contract.year + 1)


            hours_week = employee.resource_calendar_id.name
            list_time = employee.list_work_time_per_day(first_day, last_day)
            ###################
            json_employee = {
                'employee_name': employee.name,
                'employee_naf': employee.ssnid,
                'employee_vat': employee.identification_id,
                'employee_contract': employee.name,
                'employee_working_day': employee.name,
                'hours_week': hours_week,
                'days': [],
                'total_hours': timedelta(seconds=0),
                'exceeded_hours': timedelta(seconds=0)
            }
            cont_day = 0
            total_exceeded_days = timedelta(seconds=0)
            total_negavite = False
            for day in range(1, last_day_month.day + 1):
                today = date(self.month_year.year, self.month_year.month, day)
                date_order = fields.Date.context_today(self, fields.Datetime.to_datetime(today))
                hours_day = 0

                # date_start_order = fields.Datetime.to_datetime(today).strftime("%Y-%m-%d 00:00:00")
                # date_end_order = fields.Datetime.to_datetime(today).strftime("%Y-%m-%d 23:59:59")

                # date_order = fields.Date.context_today(self, day)

                absence = False
                hr_leave_id = self.env['hr.leave'].search([('employee_id', '=', employee.id), ('date_from', '<=', today), ('date_to', '>=', today)], limit=1)
                if hr_leave_id:
                    # Baja laboral
                    if hr_leave_id.holiday_status_id.type_hr_report == 'sick_leave':
                        absence = "sick_leave"
                    # Dia libre
                    elif hr_leave_id.holiday_status_id.type_hr_report == 'day_off':
                        absence = "day_off"
                    # Vacaciones
                    elif hr_leave_id.holiday_status_id.type_hr_report == 'holidays':
                        absence = "holidays"
                    # Festivo
                    elif hr_leave_id.holiday_status_id.type_hr_report == 'public_holiday':
                        absence = "public_holiday"

                # Saturday and Sunday -> Public Holiday
                if today.weekday() == 5 or today.weekday() == 6:
                    absence = "public_holiday"
                if cont_day != len(list_time):
                    if list_time[cont_day][0].day == day:
                        hours_day = list_time[cont_day][1]
                        cont_day += 1

                hr_attendance_ids = employee.attendance_ids.filtered(lambda x: fields.Datetime.context_timestamp(self, x.check_in).date() == date_order).sorted("check_in")

                # hr_attendance_ids = employee.attendance_ids.filtered(lambda x: x.check_in >= fields.Datetime.to_datetime(date_start_order) and x.check_out <= fields.Datetime.to_datetime(date_end_order)).sorted("check_in")
                morning_entry = False
                morning_exit = False
                morning_time = False
                afternoon_entry = False
                afternoon_exit = False
                afternoon_time = False
                total_day = False
                total_exceeded = False

                negative = False
                if len(hr_attendance_ids) == 1:
                    morning_entry = fields.Datetime.context_timestamp(self, hr_attendance_ids[0].check_in).strftime("%H:%M:%S")
                    morning_exit = fields.Datetime.context_timestamp(self, hr_attendance_ids[0].check_out).strftime("%H:%M:%S")
                    morning_time = hr_attendance_ids[0].check_out - hr_attendance_ids[0].check_in
                    total_day = morning_time
                    if total_day > timedelta(hours=hours_day):
                        total_exceeded = total_day - timedelta(hours=hours_day)
                    else:
                        total_exceeded = timedelta(hours=hours_day) - total_day
                        negative = True
                    if hr_leave_id.holiday_status_id.type_hr_report == 'day_off':
                        shift_ids = self.employee_ids.resource_calendar_id.attendance_ids.filtered(lambda x: x.dayofweek == str(today.weekday()))
                        time_total_day = shift_ids[0].hour_to - shift_ids[0].hour_from
                        if len(shift_ids) > 1:
                            time_afternoon = shift_ids[1].hour_to - shift_ids[1].hour_from
                            time_total_day = time_total_day + time_afternoon
                        if timedelta(hours=time_total_day) > total_day:
                            total_exceeded = timedelta(hours=time_total_day) - total_day
                            negative = True
                        else:
                            total_exceeded = total_day - timedelta(hours=time_total_day)
                            negative = False

                elif len(hr_attendance_ids) >= 2:
                    morning_entry = fields.Datetime.context_timestamp(self, hr_attendance_ids[0].check_in).strftime("%H:%M:%S")
                    morning_exit = fields.Datetime.context_timestamp(self, hr_attendance_ids[0].check_out).strftime("%H:%M:%S")
                    morning_time = hr_attendance_ids[0].check_out - hr_attendance_ids[0].check_in
                    afternoon_entry = fields.Datetime.context_timestamp(self, hr_attendance_ids[1].check_in).strftime("%H:%M:%S")
                    afternoon_exit = fields.Datetime.context_timestamp(self, hr_attendance_ids[1].check_out).strftime("%H:%M:%S")
                    afternoon_time = hr_attendance_ids[1].check_out - hr_attendance_ids[1].check_in
                    total_day = morning_time + afternoon_time
                    if total_day > timedelta(hours=hours_day):
                        total_exceeded = total_day - timedelta(hours=hours_day)
                    else:
                        total_exceeded = timedelta(hours=hours_day) - total_day
                        negative = True
                elif hours_day > 0 and len(hr_attendance_ids) == 0:
                    total_day = timedelta(hours=0)
                    total_exceeded = timedelta(hours=hours_day)
                    negative = True

                    if hr_leave_id.holiday_status_id.type_hr_report == 'day_off':
                        shift_ids = self.employee_ids.resource_calendar_id.attendance_ids.filtered(lambda x: x.dayofweek == str(today.weekday()))
                        time_total_day = shift_ids[0].hour_to - shift_ids[0].hour_from
                        if len(shift_ids) > 1:
                            time_afternoon = shift_ids[1].hour_to - shift_ids[1].hour_from
                            time_total_day = time_total_day + time_afternoon
                        total_exceeded = timedelta(hours=time_total_day) - total_day

                new_day = {
                    'day': day,
                    'total_day': total_day,
                    'total_exceeded': total_exceeded,
                    'negative': negative,
                    'absence': absence,
                    'morning': {
                        'entry': morning_entry,
                        'exit': morning_exit,
                        'time': morning_time
                    },
                    'afternoon': {
                        'entry': afternoon_entry,
                        'exit': afternoon_exit,
                        'time': afternoon_time
                    },
                }
                if total_day or total_day == timedelta(hours=0):
                    json_employee['total_hours'] += total_day
                    if not total_negavite:
                        if negative:
                            if json_employee['exceeded_hours'] > total_exceeded:
                                json_employee['exceeded_hours'] -= total_exceeded
                            else:
                                json_employee['exceeded_hours'] = total_exceeded - json_employee['exceeded_hours']
                                total_negavite = True
                        else:
                            json_employee['exceeded_hours'] += total_exceeded
                    else:
                        if negative:
                            json_employee['exceeded_hours'] += total_exceeded
                        else:
                            if json_employee['exceeded_hours'] > total_exceeded:
                                json_employee['exceeded_hours'] -= total_exceeded
                            else:
                                json_employee['exceeded_hours'] = total_exceeded - json_employee['exceeded_hours']
                                total_negavite = False
                json_employee['days'].append(new_day)

            json_employee['total_hours'] = self.calculate_time(json_employee['total_hours'].days, json_employee['total_hours'].seconds)
            json_employee['exceeded_hours'] = self.calculate_time(json_employee['exceeded_hours'].days, json_employee['exceeded_hours'].seconds)
            if total_negavite:
                json_employee['exceeded_hours'] = '%s %s' % ('-', json_employee['exceeded_hours'])
            json['employee_ids'].append(json_employee)
        return self.env.ref("hr_attendance_monthly_report.action_report_hr_attendance_monthly").report_action(None, data=json)
