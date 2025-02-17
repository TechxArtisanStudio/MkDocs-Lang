import os
import subprocess
import yaml
from mkdocs_lang.utils import find_main_project_path

def execute_command(command, relative_path=None, main_project_path=None, auto_confirm=False):
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

    # Determine the execution paths
    execution_paths = []
    for site_path in site_paths:
        if relative_path:
            exec_path = os.path.join(site_path, relative_path)
        else:
            exec_path = site_path
        execution_paths.append(exec_path)

    # Print the execution paths for confirmation
    if not auto_confirm:
        print(f"\033[94mThe following command will be executed in each site directory:\033[0m\n{command}")
        print("\033[94mThe command will be executed in the following directories:\033[0m")
        for path in execution_paths:
            print(f"  - {path}")
        confirm = input("\033[94mDo you want to proceed? (y/n): \033[0m").strip().lower()
        if confirm != 'y':
            print("\033[93mOperation cancelled.\033[0m")
            return

    # Execute the command in each site directory
    for exec_path in execution_paths:
        try:
            # print(f"Debug: Executing command in {exec_path}")
            subprocess.run(command, shell=True, cwd=exec_path, check=True)
            print(f"\033[92mExecuted command in {exec_path}\033[0m")
        except subprocess.CalledProcessError as e:
            print(f"\033[91mError executing command in {exec_path}: {e}\033[0m") 