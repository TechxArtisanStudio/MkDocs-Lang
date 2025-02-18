import os
import yaml
from contextlib import contextmanager

@contextmanager
def change_directory(path):
    """
    Context manager for changing the current working directory.
    """
    original_directory = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(original_directory)

def analyze_project_structure():
    """
    Analyze the project structure to find the main project path containing mkdocs-lang.yml.
    Determine if the current working directory is inside a MkDocs website and calculate the relative path.
    """
    # Debugging: Print the current working directory
    print(f"Debug [1]: Current working directory = {os.getcwd()}")

    current_path = os.getcwd()
    main_project_path = None
    is_inside_mkdocs_website = False
    relative_path_to_mkdocs_root = None
    combined_paths = []

    while current_path != os.path.dirname(current_path):  # Traverse up to the root
        mkdocs_lang_yml_path = os.path.join(current_path, 'mkdocs-lang.yml')
        if os.path.exists(mkdocs_lang_yml_path):
            with open(mkdocs_lang_yml_path, 'r') as f:
                config = yaml.safe_load(f)
                main_project_path = config.get('main_project_path', current_path)

            # Debugging: Print the found path or None
            print(f"Debug [2]: Found main_project_path = {main_project_path}")

            # Check if the current directory is inside a MkDocs website
            valid_site_paths = get_valid_site_paths(main_project_path)
            for site_path in valid_site_paths:
                if os.path.commonpath([os.getcwd(), site_path]) == site_path:
                    is_inside_mkdocs_website = True
                    relative_path_to_mkdocs_root = os.path.relpath(os.getcwd(), site_path)
                    break

            # Calculate combined paths
            for site_path in valid_site_paths:
                combined_path = os.path.join(site_path, relative_path_to_mkdocs_root or "")
                if os.path.exists(combined_path):
                    combined_paths.append(combined_path)

            break

        current_path = os.path.dirname(current_path)
    
    if main_project_path is None:
        print("Error: mkdocs-lang.yml not found. Please specify the --project path.")
    
    # Print the additional information
    print(f"Debug [3]: Is inside MkDocs website: {is_inside_mkdocs_website}")
    if is_inside_mkdocs_website:
        print(f"Debug [4]: Relative path to MkDocs root: {relative_path_to_mkdocs_root}")
        print(f"Debug [7]: Combined valid paths: {combined_paths}")

    return main_project_path, is_inside_mkdocs_website, combined_paths

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
    # If 'path' is not present, assume the directory name matches the site name
    site_paths = [
        os.path.join(main_project_path, site.get('path', site['name']))
        for site in config.get('websites', [])
    ]

    # Debugging: Print the extracted site paths
    print(f"Debug [5]: Extracted site paths: {site_paths}")

    # Filter out non-existent paths
    valid_site_paths = [path for path in site_paths if os.path.exists(path)]
    
    # Debugging: Print valid site paths
    print(f"Debug [6]: Valid site paths: {valid_site_paths}")

    for path in site_paths:
        if not os.path.exists(path):
            print(f"\033[93mWarning: Site path {path} does not exist.\033[0m")

    return valid_site_paths

def get_venv_executable(main_project_path, executable_name):
    """
    Get the path to an executable within the virtual environment.
    """
    venv_path = os.path.join(main_project_path, 'venv')
    if os.name == 'nt':
        return os.path.join(venv_path, 'Scripts', f'{executable_name}.exe')
    else:
        return os.path.join(venv_path, 'bin', executable_name)

def validate_and_analyze_project_path(project_path):
    """
    Validate the specified project path and analyze the project structure.
    """
    mkdocs_lang_yml_path = os.path.join(project_path, 'mkdocs-lang.yml')
    if not os.path.exists(mkdocs_lang_yml_path):
        print(f"\033[91mError: {mkdocs_lang_yml_path} does not exist. Please specify a valid mklang project path.\033[0m")
        return None, None, None

    # Use the context manager to temporarily change the directory
    with change_directory(project_path):
        # Analyze the project structure
        return analyze_project_structure()