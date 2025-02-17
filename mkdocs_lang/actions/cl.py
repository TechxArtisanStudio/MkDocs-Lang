import os
import subprocess
import yaml
from mkdocs_lang.utils import find_main_project_path

def execute_command(command, main_project_path=None, auto_confirm=False):
    # Use the utility function to determine the main project path
    main_project_path = find_main_project_path() if main_project_path is None else main_project_path
    if main_project_path is None:
        return

    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    
    if not os.path.exists(mkdocs_lang_yml_path):
        print(f"\033[91mError: {mkdocs_lang_yml_path} does not exist.\033[0m")
        return

    with open(mkdocs_lang_yml_path, 'r') as f:
        config = yaml.safe_load(f)

    # Calculate the relative path from the current directory to the main project path
    current_path = os.getcwd()

    # Detect the current MkDocs site
    current_site = None
    for site in config.get('websites', []):
        site_name = site['name']
        site_path = os.path.join(main_project_path, site_name)
        if current_path.startswith(site_path):
            current_site = site_name
            break

    if current_site:
        relative_path = os.path.relpath(current_path, os.path.join(main_project_path, current_site))
    else:
        print("\033[91mError: Current directory is not within any known MkDocs site.\033[0m")
        return

    # Prepare the list of site paths
    site_paths = []
    for site in config.get('websites', []):
        site_name = site['name']
        site_target_path = os.path.join(main_project_path, site_name, relative_path)
        
        # Ensure the path is correct by removing redundant segments
        site_target_path = os.path.normpath(site_target_path)
        if os.path.exists(site_target_path):
            site_paths.append(site_target_path)
        else:
            print(f"\033[93mWarning: Site path {site_target_path} does not exist.\033[0m")

    # Print the command and paths for confirmation
    if not auto_confirm:
        print(f"\033[94mThe following command will be executed in each site directory:\033[0m\n{command}")
        print("\033[94mThe command will be applied to the following directories:\033[0m")
        for path in site_paths:
            print(f"  - {path}")
        confirm = input("\033[94mDo you want to proceed? (y/n): \033[0m").strip().lower()
        if confirm != 'y':
            print("\033[93mOperation cancelled.\033[0m")
            return

    # Execute the command in each site directory
    for site_path in site_paths:
        print(f"\033[92mExecuting command in {site_path}: {command}\033[0m")
        subprocess.run(command, shell=True, cwd=site_path) 