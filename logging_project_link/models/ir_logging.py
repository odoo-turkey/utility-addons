from odoo import api, models, fields


class IrLogging(models.Model):
    _inherit = "ir.logging"

    def action_add_to_tasks(self):
        aw_obj = self.env["ir.actions.act_window"]
        action = aw_obj.for_xml_id("logging_project_link", "logging_link_wizard")
        return action
