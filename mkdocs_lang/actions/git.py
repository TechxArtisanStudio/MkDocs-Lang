import os
import subprocess
import yaml

def execute_git_command(command, main_project_path=None, auto_confirm=False):
    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    
    if not os.path.exists(mkdocs_lang_yml_path):
        print(f"\033[91mError: {mkdocs_lang_yml_path} does not exist.\033[0m")
        return

    with open(mkdocs_lang_yml_path, 'r') as f:
        config = yaml.safe_load(f)

    # Prepare the list of site paths
    site_paths = [os.path.join(main_project_path, site['name']) for site in config.get('websites', []) if os.path.exists(os.path.join(main_project_path, site['name']))]

    # Print the execution paths for confirmation
    if not auto_confirm:
        print(f"\033[94mThe following git command will be executed in each site directory:\033[0m")
        print(f"\033[93mgit {command}\033[0m")
        print("\033[94mThe command will be executed in the following directories:\033[0m")
        for path in site_paths:
            print(f"  - {path}")
        confirm = input("\033[94mDo you want to proceed? (y/n): \033[0m").strip().lower()
        if confirm != 'y':
            print("\033[93mOperation cancelled.\033[0m")
            return

    # Execute the git command in each site directory
    for site_path in site_paths:
        try:
            subprocess.run(f"git {command}", shell=True, cwd=site_path, check=True)
            print(f"\033[92mExecuted git command in {site_path}\033[0m")
        except subprocess.CalledProcessError as e:
            print(f"\033[91mError executing git command in {site_path}: {e}\033[0m") 