import os
import subprocess
import yaml
import logging
from mkdocs_lang.utils import get_valid_site_paths, analyze_project_structure

def execute_command(command, relative_path=None, main_project_path=None, auto_confirm=False):
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

    # Print the execution paths for confirmation
    if not auto_confirm:
        logging.info("The following command will be executed in each site directory:")
        logging.info(command)
        logging.info("The command will be executed in the following directories:")
        for path in execution_paths:
            if os.path.exists(path):
                logging.info(f"  - {path}")
            else:
                logging.warning(f"  - {path} *(directory does not exist, skipping)")
        confirm = input("Do you want to proceed? (y/n): ").strip().lower()
        if confirm != 'y':
            logging.info("Operation cancelled.")
            return

    # Execute the command in each site directory
    for exec_path in execution_paths:
        if not os.path.exists(exec_path):
            continue  # Skip if the directory does not exist
        try:
            subprocess.run(command, shell=True, cwd=exec_path, check=True)
            logging.info(f"Executed command in {exec_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing command in {exec_path}: {e}") 