import sys
from mkdocs_lang.cli import main

if __name__ == '__main__':
    # Pass None for main_project_path, let cli.py handle it
    main(sys.argv[1:], None)
