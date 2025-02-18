import os
import subprocess
import yaml
from mkdocs_lang.utils import get_main_project_path

def clone_repo(url_repo, lang='en', main_project_path=None, dry_run=False):
    # Use the utility function to determine the main project path
    main_project_path = get_main_project_path(main_project_path)
    if main_project_path is None:
        return

    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    repos_txt_path = os.path.join(main_project_path, 'repos.txt')
    
    if not os.path.exists(mkdocs_lang_yml_path):
        print(f"\033[91mError: {mkdocs_lang_yml_path} does not exist.\033[0m")  # Red for error
        return

    with open(mkdocs_lang_yml_path, 'r') as f:
        config = yaml.safe_load(f)

    project_name = os.path.splitext(os.path.basename(url_repo))[0]
    project_path = os.path.join(main_project_path, project_name)

    # Check if the project is already in the config
    existing_project = next((site for site in config['websites'] if site['name'] == project_name), None)
    if existing_project:
        if os.path.exists(project_path):
            print(f"\033[93mProject {project_name} already exists in mkdocs-lang.yml and the directory {project_path} exists.\033[0m")  # Yellow for existing project and directory
            return
        else:
            print(f"\033[93mProject {project_name} already exists in mkdocs-lang.yml but the directory {project_path} does not exist.\033[0m")  # Yellow for existing project but missing directory
    else:
        # If the project is not in the config, check if the directory exists
        if os.path.exists(project_path):
            print(f"\033[93mProject directory {project_path} already exists but is not listed in mkdocs-lang.yml.\033[0m")  # Yellow for existing directory but missing config
            return

    if dry_run:
        # Append to repos.txt without cloning
        with open(repos_txt_path, 'a') as f:
            f.write(f"{url_repo} --lang {lang}\n")
        print(f"Added {url_repo} --lang {lang} to repos.txt (dry run)")
        return

    if not os.path.exists(project_path):
        # Run the git clone command without capturing output
        result = subprocess.run(['git', 'clone', url_repo, project_path])
        if result.returncode == 0:
            print(f"\033[92mCloned {url_repo} into {project_path}\033[0m")  # Green for success
        else:
            print(f"\033[91mError cloning {url_repo}\033[0m")  # Red for error
            return

    if not existing_project:
        if url_repo.startswith("git@"):
            # Extract the domain and path, then prepend "https://"
            url_repo_https = "https://" + url_repo.split("git@")[1].replace(":", "/").replace(".git", "")
        elif url_repo.startswith("https://"):
            url_repo_https = url_repo
        else:
            url_repo_https = url_repo.replace("https///", "https://")

        # Add the new project to the config
        config['websites'].append({
            'name': project_name,
            'lang': lang,
            'url_repo': url_repo_https,
            'url_git': url_repo
        })

        with open(mkdocs_lang_yml_path, 'w') as f:
            yaml.safe_dump(config, f)

        print(f"Added {project_name} to mkdocs-lang.yml with url_repo: {url_repo_https} and url_git: {url_repo}")  # Success message

def clone_repos_from_file(batch_file=None, main_project_path=None):
    main_project_path = get_main_project_path(main_project_path)
    if main_project_path is None:
        return

    if batch_file is None:
        batch_file = os.path.join(main_project_path, 'repos.txt')

    if not os.path.exists(batch_file):
        print(f"Error: Batch file {batch_file} does not exist.")
        return

    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    if not os.path.exists(mkdocs_lang_yml_path):
        print(f"Error: {mkdocs_lang_yml_path} does not exist.")
        return

    with open(mkdocs_lang_yml_path, 'r') as f:
        config = yaml.safe_load(f)

    with open(batch_file, 'r') as f:
        lines = f.readlines()

    repos_to_clone = []

    for line in lines:
        parts = line.strip().split()
        if len(parts) < 3 or parts[1] != '--lang':
            print(f"Skipping invalid line: {line.strip()}")
            continue

        url_repo = parts[0]
        lang = parts[2]
        project_name = os.path.splitext(os.path.basename(url_repo))[0]

        # Check if the project is already in the config
        existing_project = next((site for site in config['websites'] if site['name'] == project_name), None)
        if existing_project:
            print(f"\033[93m{url_repo}\033[0m with language \033[93m{lang}\033[0m already exists in mkdocs-lang.yml. Skipping")
            continue

        repos_to_clone.append((url_repo, lang))

    if repos_to_clone:
        print("The following repositories will be cloned:")
        for url_repo, lang in repos_to_clone:
            print(f"  - {url_repo} with language {lang}")

        confirm = input("Do you want to proceed with cloning these repositories? (y/n): ").strip().lower()
        if confirm == 'y':
            for url_repo, lang in repos_to_clone:
                clone_repo(url_repo, lang, main_project_path)
        else:
            print("Cloning operation cancelled.")
    else:
        print("No new repositories to clone.")

def clone_repos_from_mkdocs_lang(main_project_path=None):
    # Use the utility function to determine the main project path
    main_project_path = get_main_project_path(main_project_path)
    if main_project_path is None:
        return

    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    
    if not os.path.exists(mkdocs_lang_yml_path):
        print(f"Error: {mkdocs_lang_yml_path} does not exist.")
        return

    with open(mkdocs_lang_yml_path, 'r') as f:
        config = yaml.safe_load(f)

    for site in config.get('websites', []):
        project_name = site['name']
        project_path = os.path.join(main_project_path, project_name)
        if not os.path.exists(project_path):
            subprocess.run(['git', 'clone', site['url_git'], project_path])
            print(f"\033[92mCloned {site['url_git']} into {project_path}\033[0m")  # Green for successful clone
        else:
            print(f"\033[93mProject {project_name} already exists at {project_path}\033[0m")  # Yellow for existing project