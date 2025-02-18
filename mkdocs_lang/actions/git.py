import os
import subprocess
import yaml
import logging

def execute_git_command(command, main_project_path=None, auto_confirm=False):
    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    
    if not os.path.exists(mkdocs_lang_yml_path):
        logging.error(f"{mkdocs_lang_yml_path} does not exist.")
        return

    with open(mkdocs_lang_yml_path, 'r') as f:
        config = yaml.safe_load(f)

    # Prepare the list of site paths
    site_paths = [os.path.join(main_project_path, site['name']) for site in config.get('websites', []) if os.path.exists(os.path.join(main_project_path, site['name']))]

    # Print the execution paths for confirmation
    if not auto_confirm:
        logging.info("The following git command will be executed in each site directory:")
        logging.info(f"git {command}")
        logging.info("The command will be executed in the following directories:")
        for path in site_paths:
            logging.info(f"  - {path}")
        confirm = input("Do you want to proceed? (y/n): ").strip().lower()
        if confirm != 'y':
            logging.info("Operation cancelled.")
            return

    # Execute the git command in each site directory
    for site_path in site_paths:
        try:
            result = subprocess.run(
                f"git {command}",
                shell=True,
                cwd=site_path,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logging.info(f"Executed git command in {site_path}")
            logging.info(f"Output:\n{result.stdout}")
            if result.stderr:
                logging.warning(f"Errors:\n{result.stderr}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing git command in {site_path}: {e}")
            logging.error(f"Output:\n{e.stdout}")
            logging.error(f"Errors:\n{e.stderr}") 