import os
import shutil
import yaml
from mkdocs_lang.utils import get_main_project_path

def remove_site(site_name, main_project_path=None):
    # Use the utility function to determine the main project path
    main_project_path = get_main_project_path(main_project_path)
    if main_project_path is None:
        return

    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    
    if not os.path.exists(mkdocs_lang_yml_path):
        print(f"\033[91mError: {mkdocs_lang_yml_path} does not exist.\033[0m")  # Red for error
        return

    with open(mkdocs_lang_yml_path, 'r') as f:
        config = yaml.safe_load(f)

    # Find the site in the configuration
    site_to_remove = next((site for site in config['websites'] if site['name'] == site_name), None)
    if not site_to_remove:
        print(f"\033[93mWarning: Site {site_name} not found in mkdocs-lang.yml.\033[0m")  # Yellow for warning
        return

    # Remove the site directory
    site_path = os.path.join(main_project_path, site_name)
    if os.path.exists(site_path):
        shutil.rmtree(site_path)
        print(f"\033[92mRemoved site directory: {site_path}\033[0m")  # Green for success
    else:
        print(f"\033[93mWarning: Site directory {site_path} does not exist.\033[0m")  # Yellow for warning

    # Remove the site from the configuration
    config['websites'] = [site for site in config['websites'] if site['name'] != site_name]

    with open(mkdocs_lang_yml_path, 'w') as f:
        yaml.safe_dump(config, f)

    print(f"\033[92mRemoved {site_name} from mkdocs-lang.yml.\033[0m")  # Green for success 