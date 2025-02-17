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