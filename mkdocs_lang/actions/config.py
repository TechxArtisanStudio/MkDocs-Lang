import os
import yaml
from mkdocs_lang.utils import get_main_project_path

def update_github_account(main_project_path=None, github_account=None):
    # Use the utility function to determine the main project path
    main_project_path = get_main_project_path(main_project_path)
    if main_project_path is None:
        return

    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    
    if not os.path.exists(mkdocs_lang_yml_path):
        print(f"Error: {mkdocs_lang_yml_path} does not exist.")
        return

    with open(mkdocs_lang_yml_path, 'r') as f:
        config = yaml.safe_load(f)

    # Update the GitHub account in mkdocs-lang.yml
    config['github_account'] = github_account

    # Update the url_repo in each project's mkdocs.yml and mkdocs-lang.yml
    # for project in config.get('projects', []):
    #     project_name = project['name']
    #     project_path = os.path.join(main_project_path, project_name)
    #     mkdocs_yml_path = os.path.join(project_path, 'mkdocs.yml')

    #     # Update the url_repo in mkdocs-lang.yml
    #     project['url_repo'] = f"https://github.com/{github_account}/{project_name}"

    #     if os.path.exists(mkdocs_yml_path):
    #         with open(mkdocs_yml_path, 'r') as f:
    #             mkdocs_config = yaml.safe_load(f)

    #         # Update the url_repo in mkdocs.yml
    #         mkdocs_config['url_repo'] = project['url_repo']

    #         with open(mkdocs_yml_path, 'w') as f:
    #             yaml.safe_dump(mkdocs_config, f)

    #         print(f"Updated url_repo in {mkdocs_yml_path}")

    # Save the updated mkdocs-lang.yml
    with open(mkdocs_lang_yml_path, 'w') as f:
        yaml.safe_dump(config, f)

    print(f"Updated GitHub account to {github_account} in {mkdocs_lang_yml_path}") 