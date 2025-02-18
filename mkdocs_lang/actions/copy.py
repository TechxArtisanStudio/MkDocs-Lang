import os
import shutil
import yaml
import logging
from mkdocs_lang.utils import analyze_project_structure

def copy_item(source_path, relative_path=None, main_project_path=None, is_directory=False, auto_confirm=False, force=False, backup=False):
    # Validate the source path
    if not os.path.exists(source_path):
        logging.error(f"Source path {source_path} does not exist.")
        return

    # Analyze the project structure to get the main project path and combined paths
    main_project_path, is_inside_mkdocs_website, combined_paths = analyze_project_structure()

    if not is_inside_mkdocs_website:
        logging.error("The current directory is not inside a MkDocs website.")
        return

    # Determine the execution paths
    execution_paths = []
    for combined_path in combined_paths:
        exec_path = os.path.join(combined_path, relative_path or "")
        execution_paths.append(exec_path)

    # Print the source and target paths for confirmation
    if not auto_confirm:
        logging.info("The following item will be copied to each site directory:")
        logging.info(source_path)
        logging.info("The item will be copied to the following directories:")
        for exec_path in execution_paths:
            target_path = os.path.join(exec_path, os.path.basename(source_path))
            if os.path.abspath(target_path) == os.path.abspath(source_path):
                logging.warning(f"  - {target_path} *(source path, skipping)")
            else:
                logging.info(f"  - {target_path}")
        confirm = input("Do you want to proceed? (y/n): ").strip().lower()
        if confirm != 'y':
            logging.info("Operation cancelled.")
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
                logging.info(f"Backup created: {backup_path}")

            # Handle overwrites
            if os.path.exists(target_path) and not force:
                logging.warning(f"{target_path} already exists. Use --force to overwrite.")
                continue

            if is_directory:
                shutil.copytree(source_path, target_path, dirs_exist_ok=True)
            else:
                shutil.copy2(source_path, target_path)
            
            logging.info(f"Copied {source_path} to {target_path}")
        except Exception as e:
            logging.error(f"Error copying to {exec_path}: {e}") 