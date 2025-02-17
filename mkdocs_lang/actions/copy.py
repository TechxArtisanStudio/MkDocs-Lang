import os
import shutil
import yaml
from mkdocs_lang.utils import find_main_project_path

def copy_item(source_path, relative_path=None, main_project_path=None, is_directory=False, auto_confirm=False, force=False, backup=False):
    # Validate the source path
    if not os.path.exists(source_path):
        print(f"\033[91mError: Source path {source_path} does not exist.\033[0m")
        return

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
        # Use the specified relative path
        source_rel_path = os.path.join(relative_path, os.path.basename(source_path))
    else:
        # Determine if the source path is within any MkDocs website
        source_rel_path = None
        for site_path in site_paths:
            if source_path.startswith(site_path):
                source_rel_path = os.path.relpath(source_path, start=site_path)
                break

        # If the source path is not within any MkDocs website, use a default relative path
        if source_rel_path is None:
            source_rel_path = os.path.relpath(source_path, start=os.path.dirname(source_path))

    # print(f"Debug: Source relative path is {source_rel_path}")

    # Print the source and target paths for confirmation
    if not auto_confirm:
        print(f"\033[94mThe following item will be copied to each site directory:\033[0m\n{source_path}")
        print("\033[94mThe item will be copied to the following directories:\033[0m")
        for path in site_paths:
            # Correctly combine the site path with the relative path
            target_path = os.path.join(path, source_rel_path.lstrip('/'))
            # print(f"Debug: Target path for site {path} is {target_path}")
            if target_path == source_path:
                print(f"  - {target_path} \033[93m*(source path, skipping)\033[0m")
            else:
                print(f"  - {target_path}")
        confirm = input("\033[94mDo you want to proceed? (y/n): \033[0m").strip().lower()
        if confirm != 'y':
            print("\033[93mOperation cancelled.\033[0m")
            return

    # Copy the item to each site directory
    for site_path in site_paths:
        try:
            target_path = os.path.join(site_path, source_rel_path.lstrip('/'))
            # print(f"Debug: Copying to target path {target_path}")
            if target_path == source_path:
                # print(f"Debug: Skipping copy to source path {source_path}")
                continue  # Skip copying to the source path

            target_dir = os.path.dirname(target_path)
            os.makedirs(target_dir, exist_ok=True)

            # Handle backup if needed
            if backup and os.path.exists(target_path):
                backup_path = f"{target_path}.bak"
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                shutil.move(target_path, backup_path)
                print(f"\033[93mBackup created: {backup_path}\033[0m")

            # Handle overwrites
            if os.path.exists(target_path) and not force:
                print(f"\033[93mWarning: {target_path} already exists. Use --force to overwrite.\033[0m")
                continue

            if is_directory:
                shutil.copytree(source_path, target_path, dirs_exist_ok=True)
            else:
                shutil.copy2(source_path, target_path)
            
            print(f"\033[92mCopied {source_path} to {target_path}\033[0m")
        except Exception as e:
            print(f"\033[91mError copying to {site_path}: {e}\033[0m") 