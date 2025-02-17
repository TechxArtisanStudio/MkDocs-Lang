import os
import subprocess
import yaml
from mkdocs_lang.utils import get_main_project_path

def clone_repo(repo_url, lang='en', main_project_path=None, dry_run=False):
    # Use the utility function to determine the main project path
    main_project_path = get_main_project_path(main_project_path)
    if main_project_path is None:
        return

    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    
    if not os.path.exists(mkdocs_lang_yml_path):
        print(f"\033[91mError: {mkdocs_lang_yml_path} does not exist.\033[0m")  # Red for error
        return

    with open(mkdocs_lang_yml_path, 'r') as f:
        config = yaml.safe_load(f)

    project_name = os.path.splitext(os.path.basename(repo_url))[0]
    project_path = os.path.join(main_project_path, project_name)

    if not dry_run:
        # Run the git clone command without capturing output
        result = subprocess.run(['git', 'clone', repo_url, project_path])
        if result.returncode == 0:
            print(f"\033[92mCloned {repo_url} into {project_path}\033[0m")  # Green for success
        else:
            print(f"\033[91mError cloning {repo_url}\033[0m")  # Red for error
            return
    else:
        # Print the dry-run message in yellow
        print(f"\033[93mDry run: Would clone {repo_url} into {project_path}\033[0m")

    if repo_url.startswith("git@"):
        repo_url_https = repo_url.replace("git@", "https://").replace(":", "/").replace(".git", "")
    elif repo_url.startswith("https///"):
        repo_url_https = repo_url.replace("https///", "https://")
    else:
        repo_url_https = repo_url

    # Check if the project is already in the config
    existing_project = next((site for site in config['websites'] if site['name'] == project_name), None)
    if existing_project:
        existing_project.update({
            'lang': lang,
            'repo_url': repo_url_https,
            'git_url': repo_url
        })
    else:
        config['websites'].append({
            'name': project_name,
            'lang': lang,
            'repo_url': repo_url_https,
            'git_url': repo_url
        })

    with open(mkdocs_lang_yml_path, 'w') as f:
        yaml.safe_dump(config, f)

    print(f"Added {project_name} to mkdocs-lang.yml with repo_url: {repo_url_https} and git_url: {repo_url}")  # Success message

def clone_repos_from_file(batch_file=None, main_project_path=None):
    if batch_file is None:
        if main_project_path is None:
            if os.path.exists('mkdocs-lang.yml'):
                main_project_path = os.getcwd()
            else:
                print("Error: mkdocs-lang.yml not found in the current directory. Please specify the --project path.")
                return
        batch_file = os.path.join(main_project_path, 'repos.txt')

    if not os.path.exists(batch_file):
        print(f"Error: Batch file {batch_file} does not exist.")
        return

    with open(batch_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split()
        if len(parts) < 2:
            print(f"Skipping invalid line: {line.strip()}")
            continue

        repo_url = parts[0]
        lang_flag = parts[1]
        lang = lang_flag.split('=')[1] if '=' in lang_flag else 'en'

        clone_repo(repo_url, lang, main_project_path)

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
            subprocess.run(['git', 'clone', site['git_url'], project_path])
            print(f"\033[92mCloned {site['git_url']} into {project_path}\033[0m")  # Green for successful clone
        else:
            print(f"\033[93mProject {project_name} already exists at {project_path}\033[0m")  # Yellow for existing project