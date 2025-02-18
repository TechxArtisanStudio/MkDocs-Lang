import os
import subprocess
import yaml
import logging
from mkdocs_lang.utils import validate_language_code

def clone_repo(url_repo, lang='en', main_project_path=None, dry_run=False):
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

    # Determine the site name from the repository URL
    site_name = url_repo.split('/')[-1].replace('.git', '')

    # Check if the site already exists in the configuration
    if any(site['name'] == site_name for site in config['websites']):
        logging.warning(f"Site {site_name} already exists in mkdocs-lang.yml. Skipping...")
        return

    # Handle dry-run by adding to repos.txt
    if dry_run:
        repos_txt_path = os.path.join(main_project_path, 'repos.txt')
        with open(repos_txt_path, 'a') as f:
            f.write(f"{url_repo} --lang={lang}\n")
        logging.info(f"Added {url_repo} with language {lang} to repos.txt (dry-run).")
        return

    # Clone the repository
    site_path = os.path.join(main_project_path, site_name)
    subprocess.run(['git', 'clone', url_repo, site_path], check=True)
    logging.info(f"Cloned repository to {site_path}")

    # Add the site to the configuration
    config['websites'].append({
        'name': site_name,
        'lang': lang,
        'url_repo': url_repo
    })

    with open(mkdocs_lang_yml_path, 'w') as f:
        yaml.safe_dump(config, f)

    logging.info(f"Added {site_name} to mkdocs-lang.yml.")

def clone_repos_from_file(batch_file=None, main_project_path=None):
    if batch_file is None:
        batch_file = os.path.join(main_project_path, 'repos.txt')

    if not os.path.exists(batch_file):
        logging.error(f"Error: Batch file {batch_file} does not exist.")
        return

    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    if not os.path.exists(mkdocs_lang_yml_path):
        logging.error(f"Error: {mkdocs_lang_yml_path} does not exist.")
        return

    with open(mkdocs_lang_yml_path, 'r') as f:
        config = yaml.safe_load(f)

    with open(batch_file, 'r') as f:
        lines = f.readlines()

    repos_to_clone = []

    for line in lines:
        # Skip comments and empty lines
        if line.strip().startswith('#') or not line.strip():
            continue

        # Correctly parse the line
        parts = line.strip().split(' --lang=')
        if len(parts) != 2:
            logging.warning(f"Skipping invalid line: {line.strip()}")
            continue

        url_repo = parts[0]
        lang = parts[1]
        site_name = url_repo.split('/')[-1].replace('.git', '')

        # Check if the site is already in the config
        if any(site['name'] == site_name for site in config['websites']):
            logging.warning(f"Site {site_name} already exists in mkdocs-lang.yml. Skipping...")
            continue

        repos_to_clone.append((url_repo, lang))

    if repos_to_clone:
        logging.info("The following repositories will be cloned:")
        for url_repo, lang in repos_to_clone:
            logging.info(f"  - {url_repo} with language {lang}")

        confirm = input("Do you want to proceed with cloning these repositories? (y/n): ").strip().lower()
        if confirm == 'y':
            for url_repo, lang in repos_to_clone:
                clone_repo(url_repo, lang, main_project_path)
        else:
            logging.info("Cloning operation cancelled.")
    else:
        logging.info("No new repositories to clone.")

def clone_repos_from_mkdocs_lang(main_project_path=None):
    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    
    if not os.path.exists(mkdocs_lang_yml_path):
        logging.error(f"Error: {mkdocs_lang_yml_path} does not exist.")
        return

    with open(mkdocs_lang_yml_path, 'r') as f:
        config = yaml.safe_load(f)

    for site in config.get('websites', []):
        site_name = site['name']
        site_path = os.path.join(main_project_path, site_name)
        if not os.path.exists(site_path):
            subprocess.run(['git', 'clone', site['url_git'], site_path])
            logging.info(f"\033[92mCloned {site['url_git']} into {site_path}\033[0m")  # Green for successful clone
        else:
            logging.warning(f"Project {site_name} already exists at {site_path}")  # Yellow for existing project