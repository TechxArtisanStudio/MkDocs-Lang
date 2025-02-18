import os
import subprocess
import yaml
from mkdocs_lang.utils import get_venv_executable, validate_language_code

def create_mkdocs_project(mkdocs_site_name, lang='en', main_project_path=None):
    # Validate the language code
    try:
        validate_language_code(lang)
    except ValueError as e:
        print(e)
        return

    github_account = 'your-github-account'  # Default value

    # Read github_account from mkdocs-lang.yml
    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    if os.path.exists(mkdocs_lang_yml_path):
        with open(mkdocs_lang_yml_path, 'r') as f:
            config = yaml.safe_load(f)
            github_account = config.get('github_account', github_account)

    mkdocs_site_path = os.path.join(main_project_path, mkdocs_site_name)

    # Use the utility function to get the path to the mkdocs executable
    mkdocs_executable = get_venv_executable(main_project_path, 'mkdocs')

    # Create a new MkDocs site using the virtual environment's mkdocs
    subprocess.run([mkdocs_executable, 'new', mkdocs_site_path])
    print(f"Created new MkDocs site at {mkdocs_site_path}")

    # Update mkdocs.yml with template
    mkdocs_yml_path = os.path.join(mkdocs_site_path, 'mkdocs.yml')
    mkdocs_template_path = os.path.join(main_project_path, 'mkdocs.yml.template')

    with open(mkdocs_template_path, 'r') as template_file:
        template_content = template_file.read()

    # Replace placeholders with actual values
    mkdocs_yml_content = template_content.replace('<mkdocs-project>', mkdocs_site_name).replace('<lang>', lang).replace('<github-account>', github_account)

    with open(mkdocs_yml_path, 'w') as mkdocs_yml_file:
        mkdocs_yml_file.write(mkdocs_yml_content)
    print(f"Updated mkdocs.yml for {mkdocs_site_name}")

    # Update mkdocs-lang.yml
    with open(mkdocs_lang_yml_path, 'r') as f:
        config = yaml.safe_load(f)

    # Append the new site to the websites list
    config['websites'].append({
        'name': mkdocs_site_name,
        'lang': lang,
        'url_repo': f"https://github.com/{github_account}/{mkdocs_site_name}"
    })

    with open(mkdocs_lang_yml_path, 'w') as f:
        yaml.safe_dump(config, f)

    print(f"Added {mkdocs_site_name} to mkdocs-lang.yml")
