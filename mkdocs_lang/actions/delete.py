import os
import shutil
import yaml
from mkdocs_lang.utils import find_main_project_path, get_valid_site_paths

def delete_item(target_path, relative_path=None, main_project_path=None, is_directory=False, auto_confirm=False):
    # Get valid site paths
    site_paths = get_valid_site_paths(main_project_path)

    # Determine the relative path for the target
    if relative_path:
        target_rel_path = os.path.join(relative_path.lstrip('/'), os.path.basename(target_path))
    else:
        # Use the current working directory to determine the relative path
        current_dir = os.getcwd()
        if '/docs' in current_dir:
            docs_index = current_dir.index('/docs') + len('/docs')
            # Append the target file name to the relative path
            target_rel_path = os.path.join(current_dir[docs_index:].lstrip('/'), os.path.basename(target_path))
        else:
            print("\033[91mError: Current directory is not within a valid '/docs' path.\033[0m")
            return

    # Print the target paths for confirmation
    if not auto_confirm:
        print(f"\033[94mThe following item will be deleted from each site directory:\033[0m\n{target_path}")
        print("\033[94mThe item will be deleted from the following directories:\033[0m")
        for path in site_paths:
            full_target_path = os.path.join(path, 'docs', target_rel_path)
            if os.path.exists(path):
                print(f"  - {full_target_path}")
            else:
                print(f"  - {full_target_path} \033[93m*(directory does not exist, skipping)\033[0m")
        confirm = input("\033[94mDo you want to proceed? (y/n): \033[0m").strip().lower()
        if confirm != 'y':
            print("\033[93mOperation cancelled.\033[0m")
            return

    # Delete the item from each site directory
    for site_path in site_paths:
        if not os.path.exists(site_path):
            continue  # Skip if the directory does not exist
        try:
            full_target_path = os.path.join(site_path, 'docs', target_rel_path)
            print(f"Attempting to delete: {full_target_path} (is_directory={is_directory})")  # Debug statement
            if is_directory:
                shutil.rmtree(full_target_path)
            else:
                os.remove(full_target_path)
            
            print(f"\033[92mDeleted {full_target_path}\033[0m")
        except Exception as e:
            print(f"\033[91mError deleting from {site_path}: {e}\033[0m") 