import os
import subprocess
import yaml
from mkdocs_lang.utils import find_main_project_path, get_valid_site_paths

def execute_command(command, relative_path=None, main_project_path=None, auto_confirm=False):
    # Get valid site paths
    site_paths = get_valid_site_paths(main_project_path)

    # Determine the execution paths
    execution_paths = []
    if relative_path:
        # Use the specified relative path
        for site_path in site_paths:
            exec_path = os.path.join(site_path, relative_path.lstrip('/'))  # Ensure no leading slash
            execution_paths.append(exec_path)
    else:
        # Default to running in the root of each MkDocs site
        for site_path in site_paths:
            exec_path = os.path.join(site_path, "")
            execution_paths.append(exec_path)

    # Print the execution paths for confirmation
    if not auto_confirm:
        print(f"\033[94mThe following command will be executed in each site directory:\033[0m")
        print(f"\033[93m{command}\033[0m")
        print("\033[94mThe command will be executed in the following directories:\033[0m")
        for path in execution_paths:
            if os.path.exists(path):
                print(f"  - {path}")
            else:
                print(f"  - {path} \033[93m*(directory does not exist, skipping)\033[0m")
        confirm = input("\033[94mDo you want to proceed? (y/n): \033[0m").strip().lower()
        if confirm != 'y':
            print("\033[93mOperation cancelled.\033[0m")
            return

    # Execute the command in each site directory
    for exec_path in execution_paths:
        if not os.path.exists(exec_path):
            continue  # Skip if the directory does not exist
        try:
            subprocess.run(command, shell=True, cwd=exec_path, check=True)
            print(f"\033[92mExecuted command in {exec_path}\033[0m")
        except subprocess.CalledProcessError as e:
            print(f"\033[91mError executing command in {exec_path}: {e}\033[0m") 