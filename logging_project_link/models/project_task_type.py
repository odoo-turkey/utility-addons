from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    default_log_save = fields.Boolean(string="Save logs", default=False)

    @api.constrains("default_log_save")
    def _check_default_log_save(self):
        for task in self:
            if (
                task.default_log_save
                and self.search_count([("default_log_save", "=", True)]) > 1
            ):
                raise ValidationError(
                    _("There is already a default task type that we save logs.")
                )
