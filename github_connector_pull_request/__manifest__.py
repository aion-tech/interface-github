{
    "name": "github_connector_pull_request",
    "summary": "Extend OCA's github_connector by adding a pull request model",
    "description": "",
    "website": "https://aion-tech.it/",
    # https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    "category": "Uncategorized",
    "version": "14.0.1.0.0",
    "depends": [
        "github_connector",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/pull_request_views.xml",
        "wizards/view_wizard_load_github_model.xml",
    ],
}
