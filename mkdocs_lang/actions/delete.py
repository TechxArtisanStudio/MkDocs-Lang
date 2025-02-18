import os
import shutil
import yaml
from mkdocs_lang.utils import get_valid_site_paths, analyze_project_structure

def delete_item(target_path, relative_path=None, main_project_path=None, is_directory=False, auto_confirm=False):
    # Analyze the project structure to get the main project path and combined paths
    main_project_path, is_inside_mkdocs_website, combined_paths = analyze_project_structure()

    if not is_inside_mkdocs_website:
        print("\033[91mError: The current directory is not inside a MkDocs website.\033[0m")
        return

    # Determine the execution paths
    execution_paths = []
    for combined_path in combined_paths:
        exec_path = os.path.join(combined_path, relative_path or "")
        execution_paths.append(exec_path)

    # Check if the target files exist
    target_exists = False
    for exec_path in execution_paths:
        full_target_path = os.path.join(exec_path, os.path.basename(target_path))
        if os.path.exists(full_target_path):
            target_exists = True
            break

    # Print the target paths for confirmation
    if not auto_confirm:
        print(f"\033[94mThe following item will be deleted from each site directory:\033[0m\n{target_path}")
        print("\033[94mThe item will be deleted from the following directories:\033[0m")
        for exec_path in execution_paths:
            full_target_path = os.path.join(exec_path, os.path.basename(target_path))
            if os.path.exists(full_target_path):
                print(f"  - {full_target_path}")
            else:
                print(f"  - {full_target_path} \033[93m*(file does not exist, skipping)\033[0m")
        if not target_exists:
            print("\033[93mWarning: None of the target files exist. Operation will be skipped.\033[0m")
            return
        confirm = input("\033[94mDo you want to proceed? (y/n): \033[0m").strip().lower()
        if confirm != 'y':
            print("\033[93mOperation cancelled.\033[0m")
            return

    # Delete the item from each site directory
    for exec_path in execution_paths:
        full_target_path = os.path.join(exec_path, os.path.basename(target_path))
        if not os.path.exists(full_target_path):
            continue  # Skip if the file does not exist
        try:
            if is_directory:
                shutil.rmtree(full_target_path)
            else:
                os.remove(full_target_path)
            print(f"\033[92mDeleted {full_target_path}\033[0m")
        except Exception as e:
            print(f"\033[91mError deleting from {exec_path}: {e}\033[0m") 