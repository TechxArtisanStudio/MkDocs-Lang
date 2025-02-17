import os
import shutil
import yaml
from mkdocs_lang.utils import find_main_project_path

def delete_item(target_path, relative_path=None, main_project_path=None, is_directory=False, auto_confirm=False):
    # Determine the main project path if not provided
    if main_project_path is None:
        main_project_path = find_main_project_path()
    
    if main_project_path is None:
        print("\033[91mError: Main project path could not be determined.\033[0m")
        return

    # print(f"Debug: Main project path is {main_project_path}")

    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    
    if not os.path.exists(mkdocs_lang_yml_path):
        print(f"\033[91mError: {mkdocs_lang_yml_path} does not exist.\033[0m")
        return

    with open(mkdocs_lang_yml_path, 'r') as f:
        config = yaml.safe_load(f)

    # Prepare the list of site paths
    site_paths = []
    for site in config.get('websites', []):
        site_name = site['name']
        site_path = os.path.join(main_project_path, site_name)
        
        if os.path.exists(site_path):
            site_paths.append(site_path)
        else:
            print(f"\033[93mWarning: Site path {site_path} does not exist.\033[0m")

    # print(f"Debug: Site paths are {site_paths}")

    # Determine the relative path for the target
    if relative_path:
        target_rel_path = os.path.join(relative_path, os.path.basename(target_path))
    else:
        if os.path.isabs(target_path):
            # If absolute, determine the relative path from the MkDocs site
            for site_path in site_paths:
                if target_path.startswith(site_path):
                    target_rel_path = os.path.relpath(target_path, start=site_path)
                    break
            else:
                print("\033[91mError: Target path is not within any MkDocs site.\033[0m")
                return
        else:
            # If relative, assume it's relative to the current working directory
            current_dir = os.getcwd()
            for site_path in site_paths:
                if current_dir.startswith(site_path):
                    target_rel_path = os.path.relpath(os.path.join(current_dir, target_path), start=site_path)
                    break
            else:
                print("\033[91mError: Current directory is not within any MkDocs site.\033[0m")
                return

    # Print the target paths for confirmation
    if not auto_confirm:
        print(f"\033[94mThe following item will be deleted from each site directory:\033[0m\n{target_path}")
        print("\033[94mThe item will be deleted from the following directories:\033[0m")
        for path in site_paths:
            full_target_path = os.path.join(path, target_rel_path)
            # print(f"Debug: Full target path for site {path} is {full_target_path}")
            print(f"  - {full_target_path}")
        confirm = input("\033[94mDo you want to proceed? (y/n): \033[0m").strip().lower()
        if confirm != 'y':
            print("\033[93mOperation cancelled.\033[0m")
            return

    # Delete the item from each site directory
    for site_path in site_paths:
        try:
            full_target_path = os.path.join(site_path, target_rel_path)
            # print(f"Debug: Attempting to delete {full_target_path}")
            if is_directory:
                shutil.rmtree(full_target_path)
            else:
                os.remove(full_target_path)
            
            print(f"\033[92mDeleted {full_target_path}\033[0m")
        except Exception as e:
            print(f"\033[91mError deleting from {site_path}: {e}\033[0m") 