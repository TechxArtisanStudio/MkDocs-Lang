import os
import shutil
import yaml
from mkdocs_lang.utils import analyze_project_structure

def copy_item(source_path, relative_path=None, main_project_path=None, is_directory=False, auto_confirm=False, force=False, backup=False):
    # Validate the source path
    if not os.path.exists(source_path):
        print(f"\033[91mError: Source path {source_path} does not exist.\033[0m")
        return

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

    # Print the source and target paths for confirmation
    if not auto_confirm:
        print(f"\033[94mThe following item will be copied to each site directory:\033[0m\n{source_path}")
        print("\033[94mThe item will be copied to the following directories:\033[0m")
        for exec_path in execution_paths:
            target_path = os.path.join(exec_path, os.path.basename(source_path))
            # Check if the target path is the same as the source path
            if os.path.abspath(target_path) == os.path.abspath(source_path):
                print(f"  - {target_path} \033[93m*(source path, skipping)\033[0m")
            else:
                print(f"  - {target_path}")
        confirm = input("\033[94mDo you want to proceed? (y/n): \033[0m").strip().lower()
        if confirm != 'y':
            print("\033[93mOperation cancelled.\033[0m")
            return

    # Copy the item to each site directory
    for exec_path in execution_paths:
        target_path = os.path.join(exec_path, os.path.basename(source_path))
        if os.path.abspath(target_path) == os.path.abspath(source_path):
            continue  # Skip copying to the source path

        try:
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
            print(f"\033[91mError copying to {exec_path}: {e}\033[0m") 