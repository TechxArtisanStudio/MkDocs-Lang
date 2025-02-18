import os
import yaml
import logging

def update_github_account(main_project_path=None, github_account=None):
    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    
    if not os.path.exists(mkdocs_lang_yml_path):
        logging.error(f"{mkdocs_lang_yml_path} does not exist.")
        return

    with open(mkdocs_lang_yml_path, 'r') as f:
        config = yaml.safe_load(f)

    # Update the GitHub account in mkdocs-lang.yml
    config['github_account'] = github_account

    # Save the updated mkdocs-lang.yml
    with open(mkdocs_lang_yml_path, 'w') as f:
        yaml.safe_dump(config, f)

    logging.info(f"Updated GitHub account to {github_account} in {mkdocs_lang_yml_path}") 