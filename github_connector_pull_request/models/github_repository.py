from odoo import api, fields, models


class GithubRepository(models.Model):
    _inherit = "github.repository"

    gh_pull_request_ids = fields.One2many(
        "github.pull.request",
        "gh_repository_id",
        string="Pull Requests",
    )
    repository_pr_qty = fields.Integer(
        string="Pull Request Quantity",
        compute="_compute_repository_pr_qty",
    )

    @api.depends("gh_pull_request_ids")
    def _compute_repository_pr_qty(self):
        for record in self:
            record.repository_pr_qty = len(record.gh_pull_request_ids)

    def action_github_pull_requests(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "github_connector_pull_request.action_github_repository_pull_request"
        )
        action["context"] = dict(self.env.context)
        action["context"]["search_default_gh_repository_id"] = self.id
        return action

    def button_sync_pull_request(self):
        for repository in self.filtered(lambda r: not r.is_ignored):
            gh_repo = repository.find_related_github_object()
            gh_prs = gh_repo.get_pulls(state="open")  # TODO configurable states
            for gh_pr in gh_prs:
                pr_id = (
                    self.env["github.pull.request"]
                    .with_context(repository_id=repository)
                    .get_from_id_or_create(
                        gh_data=gh_pr,
                    )
                )
                pr_id.update_from_github(False)
