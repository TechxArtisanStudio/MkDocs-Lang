import os
import shutil
import yaml
import logging

def remove_site(site_name, main_project_path=None):
    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    
    if not os.path.exists(mkdocs_lang_yml_path):
        logging.error(f"{mkdocs_lang_yml_path} does not exist.")
        return

    with open(mkdocs_lang_yml_path, 'r') as f:
        config = yaml.safe_load(f)

    # Find the site in the configuration
    site_to_remove = next((site for site in config['websites'] if site['name'] == site_name), None)
    if not site_to_remove:
        logging.warning(f"Site {site_name} not found in mkdocs-lang.yml.")
        return

    # Remove the site directory
    site_path = os.path.join(main_project_path, site_name)
    if os.path.exists(site_path):
        shutil.rmtree(site_path)
        logging.info(f"Removed site directory: {site_path}")
    else:
        logging.warning(f"Site directory {site_path} does not exist.")

    # Remove the site from the configuration
    config['websites'] = [site for site in config['websites'] if site['name'] != site_name]

    with open(mkdocs_lang_yml_path, 'w') as f:
        yaml.safe_dump(config, f)

    logging.info(f"Removed {site_name} from mkdocs-lang.yml.") 