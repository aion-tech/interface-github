from odoo import fields, models


class WizardLoadGithubModel(models.TransientModel):
    _inherit = "wizard.load.github.model"

    github_type = fields.Selection(
        selection_add=[("pr", "Pull Request")],
        ondelete={"pr": "cascade"},
    )
    repository_id = fields.Many2one(
        "github.repository",
        string="Github Repository",
    )

    def button_create_from_github(self):
        for wizard in self:
            if wizard.github_type == "pr":
                github_model = self.env["github.pull.request"]
                ctx = self.env.context.copy()
                ctx.update(repository_id=wizard.repository_id)
                # TODO create / update
                my_obj = github_model.with_context(ctx).create_from_name(wizard.name)
                # TODO - does child_update make sense for PRs?
                # if wizard.child_update:
                #     my_obj.update_from_github(True)

            else:
                super().button_create_from_github()
