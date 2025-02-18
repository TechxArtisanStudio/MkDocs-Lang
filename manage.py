import sys
from mkdocs_lang.cli import main
from mkdocs_lang.utils import find_main_project_path

if __name__ == '__main__':
    # Determine the main project path
    main_project_path = find_main_project_path()
    if main_project_path is None:
        print("\033[91mError: mkdocs-lang.yml not found. Please specify the --project path.\033[0m")
        sys.exit(1)

    # Pass the main project path to the CLI
    main(sys.argv[1:], main_project_path)
