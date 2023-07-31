import base64
import logging
from datetime import datetime
from urllib.request import urlopen

from github import Github
from github.GithubException import UnknownObjectException
from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

_GITHUB_URL = "https://github.com/"


class AbstractGithubModel(models.AbstractModel):
    """
    This abstract model is used to share all features related to github model.
    Note that some fields and function have to be defined in the inherited
    model.
    """

    _inherit = "abstract.github.model"

    @api.model
    def create_from_name(self, name):
        """Call Github API, using a URL using github name. Load data and
        Create Odoo object accordingly, if the odoo object doesn't exist.

        :param name: the github name to load
        :return: The created object

        :Example:

        >>> self.env['github_organization'].create_from_name('OCA')
        >>> self.env['github_repository'].create_from_name('OCA/web')
        """
        if self._name == "github.pull.request":
            gh_api = self.get_github_connector()
            repository_id = self.env.context.get("repository_id", False)
            if not repository_id:
                raise UserError(_("No repository ID provided"))
            gh_repo = gh_api.get_repo(repository_id.github_name)
            gh_pr = gh_repo.get_pull(int(name))
            data = []
            if not gh_pr:
                raise UserError(
                    _("Pull request %s not found on repo %s") % name,
                    repository_id.github_name,
                )
            data.append(self.get_odoo_data_from_github(gh_pr))
            return self._create_from_github_data(data)

        else:
            return super().create_from_name(name)

    # overwrite to handle create vals list
    @api.model
    def _create_from_github_data(self, data, extra_data=None):
        if isinstance(data, dict):
            data = [data]
        extra_data = extra_data and extra_data or {}
        for d in data:
            d.update(extra_data)
        return self.create(data)
