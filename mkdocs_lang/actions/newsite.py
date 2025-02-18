import os
import subprocess
import yaml
import logging
from mkdocs_lang.utils import get_venv_executable, validate_language_code

def create_mkdocs_project(mkdocs_site_name, lang='en', main_project_path=None):
    # Validate the language code
    try:
        validate_language_code(lang)
    except ValueError as e:
        logging.error(e)
        return

    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    if not os.path.exists(mkdocs_lang_yml_path):
        logging.error(f"{mkdocs_lang_yml_path} does not exist.")
        return

    with open(mkdocs_lang_yml_path, 'r') as f:
        config = yaml.safe_load(f)

    # Check if the site already exists
    if any(site['name'] == mkdocs_site_name and site['lang'] == lang for site in config['websites']):
        logging.warning(f"Site {mkdocs_site_name} with language {lang} already exists in mkdocs-lang.yml. Skipping...")
        return

    github_account = config.get('github_account', 'your-github-account')  # Default value

    mkdocs_site_path = os.path.join(main_project_path, mkdocs_site_name)

    # Use the utility function to get the path to the mkdocs executable
    mkdocs_executable = get_venv_executable(main_project_path, 'mkdocs')

    # Create a new MkDocs site using the virtual environment's mkdocs
    subprocess.run([mkdocs_executable, 'new', mkdocs_site_path])
    logging.info(f"Created new MkDocs site at {mkdocs_site_path}")

    # Update mkdocs.yml with template
    mkdocs_yml_path = os.path.join(mkdocs_site_path, 'mkdocs.yml')
    mkdocs_template_path = os.path.join(main_project_path, 'mkdocs.yml.template')

    with open(mkdocs_template_path, 'r') as template_file:
        template_content = template_file.read()

    # Replace placeholders with actual values
    mkdocs_yml_content = template_content.replace('<mkdocs-project>', mkdocs_site_name).replace('<lang>', lang).replace('<github-account>', github_account)

    with open(mkdocs_yml_path, 'w') as mkdocs_yml_file:
        mkdocs_yml_file.write(mkdocs_yml_content)
    logging.info(f"Updated mkdocs.yml for {mkdocs_site_name}")

    # Append the new site to the websites list
    config['websites'].append({
        'name': mkdocs_site_name,
        'lang': lang,
        'url_repo': f"https://github.com/{github_account}/{mkdocs_site_name}"
    })

    with open(mkdocs_lang_yml_path, 'w') as f:
        yaml.safe_dump(config, f)

    logging.info(f"Added {mkdocs_site_name} to mkdocs-lang.yml")
