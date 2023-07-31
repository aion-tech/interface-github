from github.Repository import Repository
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GithubPullRequest(models.Model):
    _name = "github.pull.request"
    _inherit = ["abstract.github.model"]
    _description = "Rpresents a GitHub pull request"
    _github_login_field = "number"

    name = fields.Char(string="Number", required=True)
    gh_repository_id = fields.Many2one(
        "github.repository",
        string="Github Repository",
        required=True,
    )
    pr_user = fields.Char(string="User")
    pr_title = fields.Char(string="Title")
    pr_description = fields.Char(string="Description")
    pr_head_ref = fields.Char(string="Head Ref")
    pr_head_url = fields.Char(string="Head URL", compute="_compute_pr_head_url")

    @api.constrains("name", "github_url")
    def _check_unique_pr(self):
        if (
            self.search_count(
                [
                    ("name", "=", self.name),
                    ("github_url", "=", self.github_url),
                ]
            )
            > 1
        ):
            raise ValidationError(
                _("A pull request with the same number and url already exists\n%s - %s")
                % (self.name, self.github_url)
            )

    def _compute_pr_head_url(self):
        for rec in self:
            rec.pr_head_url = (
                f"{rec.gh_repository_id.github_url}/tree/{rec.pr_head_ref}"
            )

    @api.model
    def get_odoo_data_from_github(self, gh_data):
        res = super().get_odoo_data_from_github(gh_data)
        pull_request = gh_data
        res.update(
            {
                "name": pull_request.number,
                "pr_user": pull_request.user.login,
                "pr_title": pull_request.title,
                "pr_description": pull_request.body,
                "gh_repository_id": self.env.context["repository_id"].id,
                "pr_head_ref": pull_request.head.ref,
            }
        )

        return res

    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)

    def find_related_github_object(self, obj_id=None):
        """Query Github API to find the related object"""
        self.ensure_one()
        gh_repo: Repository = self.gh_repository_id.find_related_github_object()
        return gh_repo.get_pull(int(self.name))
