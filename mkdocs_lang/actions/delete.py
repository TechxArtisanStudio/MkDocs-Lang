import os
import shutil
import yaml
import logging
from mkdocs_lang.utils import get_valid_site_paths, analyze_project_structure

def delete_item(target_path, relative_path=None, main_project_path=None, is_directory=False, auto_confirm=False):
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

    # Check if the target files exist
    target_exists = False
    for exec_path in execution_paths:
        full_target_path = os.path.join(exec_path, os.path.basename(target_path))
        if os.path.exists(full_target_path):
            target_exists = True
            break

    # Print the target paths for confirmation
    if not auto_confirm:
        logging.info("The following item will be deleted from each site directory:")
        logging.info(target_path)
        logging.info("The item will be deleted from the following directories:")
        for exec_path in execution_paths:
            full_target_path = os.path.join(exec_path, os.path.basename(target_path))
            if os.path.exists(full_target_path):
                logging.info(f"  - {full_target_path}")
            else:
                logging.warning(f"  - {full_target_path} *(file does not exist, skipping)")
        if not target_exists:
            logging.warning("None of the target files exist. Operation will be skipped.")
            return
        confirm = input("Do you want to proceed? (y/n): ").strip().lower()
        if confirm != 'y':
            logging.info("Operation cancelled.")
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
            logging.info(f"Deleted {full_target_path}")
        except Exception as e:
            logging.error(f"Error deleting from {exec_path}: {e}") 