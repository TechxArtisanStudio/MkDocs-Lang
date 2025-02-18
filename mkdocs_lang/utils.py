import os
import yaml

def get_main_project_path(provided_path=None):
    """
    Determine the main project path. If a path is provided, use it.
    Otherwise, check if mkdocs-lang.yml exists in the current directory.
    """
    if provided_path is not None:
        return provided_path

    if os.path.exists('mkdocs-lang.yml'):
        return os.getcwd()

    print("Error: mkdocs-lang.yml not found in the current directory. Please specify the main project path.")
    return None

def find_main_project_path():
    """
    Traverse up the directory tree to find the main project path containing mkdocs-lang.yml.
    """
    current_path = os.getcwd()
    while current_path != os.path.dirname(current_path):  # Traverse up to the root
        mkdocs_lang_yml_path = os.path.join(current_path, 'mkdocs-lang.yml')
        if os.path.exists(mkdocs_lang_yml_path):
            with open(mkdocs_lang_yml_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get('main_project_path', current_path)
        current_path = os.path.dirname(current_path)
    
    print("Error: mkdocs-lang.yml not found. Please specify the --project path.")
    return None

def get_venv_executable(main_project_path, executable_name):
    """
    Get the path to an executable within the virtual environment.
    """
    venv_path = os.path.join(main_project_path, 'venv')
    if os.name == 'nt':
        return os.path.join(venv_path, 'Scripts', f'{executable_name}.exe')
    else:
        return os.path.join(venv_path, 'bin', executable_name)

def get_valid_site_paths(main_project_path):
    """
    Retrieve the list of valid site paths from mkdocs-lang.yml.
    """
    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    
    if not os.path.exists(mkdocs_lang_yml_path):
        print(f"\033[91mError: {mkdocs_lang_yml_path} does not exist.\033[0m")
        return []

    with open(mkdocs_lang_yml_path, 'r') as f:
        config = yaml.safe_load(f)

    # Prepare the list of site paths using the 'path' key from mkdocs-lang.yml
    site_paths = [site['path'] for site in config.get('websites', []) if 'path' in site]

    # Filter out non-existent paths
    valid_site_paths = [path for path in site_paths if os.path.exists(path)]
    for path in site_paths:
        if not os.path.exists(path):
            print(f"\033[93mWarning: Site path {path} does not exist.\033[0m")

    return valid_site_paths 