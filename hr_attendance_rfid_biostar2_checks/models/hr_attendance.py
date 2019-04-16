# -*- coding: utf-8 -*-

from datetime import datetime
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    @api.model
    def _update_attendances_from_biostar2(self):
        """
        Register new checks from Biostar2 server
        :return:
        """
        try:
            company = self.env.user.company_id

            # Last timestamp processed
            devdt = company.biostar2_server_last_checkinout_timestamp

            # TODO if month has already changed since last update, we should also query the previous month table
            today = fields.datetime.today()
            # today = datetime.datetime.today() - datetime.timedelta(days=30)  # Only for testing purposes
            table = 't_lg%s' % today.strftime('%Y%m')
            _logger.debug('[_update_attendances_from_biostar2] Looking for events on table %s...' % table)

            DbSource = company.biostar2_server_id
            _logger.debug('[_update_attendances_from_biostar2] Connected to database!')
            res = DbSource.execute(
                query="SELECT devdt, devuid, usrid from {0}"
                      " where usrid <> %(notuser)s and evt>=4097 and evt<=4111"
                      " and devdt >= %(devdt)s order by devdt".format(table),
                execute_params={'notuser': '', 'devdt': devdt})
            _logger.info('[_update_attendances_from_biostar2] Found %s check in/out with devdt >= %s'
                         % (len(res), devdt))
            if len(res) > 0:
                last_timestamp = None
                min_secs_checks = company.biostar2_server_min_secs_between_checks
                for row in res:
                    _logger.info('[_update_attendances_from_biostar2] Read devdt=%d, devuid=%d, usrid=%s' %
                                 (row['devdt'], row['devuid'], row['usrid']))
                    attendance_result = self.env['hr.employee'].register_attendance_min_secs_checks(
                        card_code=row['usrid'],
                        action_date=fields.Datetime.to_string(datetime.utcfromtimestamp(row['devdt'])),
                        min_secs_checks=min_secs_checks)
                    if attendance_result['action'] == 'FALSE':
                        _logger.error('[_update_attendances_from_biostar2] Processing attendance: %s' %
                                      attendance_result['error_message'])
                    else:
                        _logger.info('[_update_attendances_from_biostar2] Processed %s attendance for card_code %s' %
                                     (attendance_result['rfid_card_code'], attendance_result['action']))
                    last_timestamp = row['devdt']
                # Last processed worksheet timestamp update
                company.biostar2_server_last_checkinout_timestamp = last_timestamp
                _logger.info('[_update_attendances_from_biostar2] New last timestamp: %d' % last_timestamp)

        except Exception as e:
            _logger.error('[_update_attendances_from_biostar2] Check in/out revision: %s' % e)

        _logger.debug('[_update_attendances_from_biostar2] Finished check in/out revision')
