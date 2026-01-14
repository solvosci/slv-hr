# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import logging

logger = logging.getLogger(__name__)

def pre_init_hook(env):
    logger.info("Creating field has_attachment on hr_leave")
    env.cr.execute("""
        ALTER TABLE hr_leave ADD COLUMN IF NOT EXISTS has_attachment boolean;
    """)

    logger.info("Computing field has_attachment on hr.leave")
    env.cr.execute("""
        UPDATE hr_leave SET has_attachment = TRUE
        WHERE id IN (
            SELECT res_id FROM ir_attachment
            WHERE res_model = 'hr.leave'
        );
    """)
