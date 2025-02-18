import os
import yaml
import json
from contextlib import contextmanager
from difflib import get_close_matches
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)

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

# Load language data from JSON file
LANGUAGE_FILE_PATH = os.path.join(os.path.dirname(__file__), 'languages.json')
# print(f"Loading language data from: {LANGUAGE_FILE_PATH}")
with open(LANGUAGE_FILE_PATH, 'r') as f:
    LANGUAGE_DATA = json.load(f)

def validate_language_code(lang):
    """
    Validate the language code against the list of supported languages.
    Suggest similar codes if the input is incorrect.
    """
    if lang not in LANGUAGE_DATA:
        suggestions = get_close_matches(lang, LANGUAGE_DATA.keys(), n=3)
        suggestion_text = f" Did you mean: {', '.join(suggestions)}?" if suggestions else ""
        raise ValueError(f"Error: Unsupported language code '{lang}'.{suggestion_text}")

def find_main_project_path():
    """
    Traverse up the directory tree to find the main project path containing mkdocs-lang.yml.
    """
    current_path = Path.cwd()
    while current_path != current_path.parent:
        mkdocs_lang_yml_path = current_path / 'mkdocs-lang.yml'
        if mkdocs_lang_yml_path.exists():
            return current_path
        current_path = current_path.parent
    logging.error("mkdocs-lang.yml not found. Please specify the --project path.")
    return None

def load_project_config(main_project_path):
    """
    Load the mkdocs-lang.yml configuration file.
    """
    mkdocs_lang_yml_path = main_project_path / 'mkdocs-lang.yml'
    try:
        with open(mkdocs_lang_yml_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error("Failed to load configuration from %s: %s", mkdocs_lang_yml_path, e)
        return None

def is_inside_mkdocs_website(main_project_path, valid_site_paths):
    """
    Check if the current directory is inside a MkDocs website.
    """
    for site_path in valid_site_paths:
        if Path.cwd().is_relative_to(site_path):
            relative_path = Path.cwd().relative_to(site_path)
            return True, relative_path
    return False, None

def calculate_combined_paths(valid_site_paths, relative_path):
    """
    Calculate combined paths based on valid site paths and the relative path.
    """
    combined_paths = []
    for site_path in valid_site_paths:
        combined_path = site_path / (relative_path or "")
        if combined_path.exists():
            combined_paths.append(combined_path)
    return combined_paths

def analyze_project_structure():
    """
    Analyze the project structure to find the main project path containing mkdocs-lang.yml.
    Determine if the current working directory is inside a MkDocs website and calculate the relative path.
    """
    main_project_path = find_main_project_path()
    if not main_project_path:
        return None, None, None

    config = load_project_config(main_project_path)
    if not config:
        return None, None, None

    valid_site_paths = get_valid_site_paths(main_project_path)
    inside_mkdocs, relative_path = is_inside_mkdocs_website(main_project_path, valid_site_paths)
    combined_paths = calculate_combined_paths(valid_site_paths, relative_path)

    logging.info("Is inside MkDocs website: %s", inside_mkdocs)
    if inside_mkdocs:
        logging.info("Relative path to MkDocs root: %s", relative_path)
        logging.info("Combined valid paths: %s", combined_paths)

    return main_project_path, inside_mkdocs, combined_paths

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