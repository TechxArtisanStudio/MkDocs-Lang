import os
import subprocess
import yaml
import sys

def create_project(main_project_path, github_account=None):
    main_project_path = os.path.abspath(main_project_path)
    
    if not os.path.exists(main_project_path):
        os.makedirs(main_project_path)

    # Create a Python virtual environment
    venv_path = os.path.join(main_project_path, 'venv')
    subprocess.run(['python', '-m', 'venv', venv_path])
    print(f"Created virtual environment at {venv_path}")

    # Create mkdocs-lang.yml
    mkdocs_lang_yml_path = os.path.join(main_project_path, 'mkdocs-lang.yml')
    with open(mkdocs_lang_yml_path, 'w') as f:
        yaml.dump({
            'main_project_path': main_project_path,
            'venv_path': venv_path,
            'github_account': github_account or 'your-github-account',
            'websites': []
        }, f)
    print(f"Created mkdocs-lang.yml at {mkdocs_lang_yml_path}")

    # Create mkdocs.yml.template
    mkdocs_yml_template_path = os.path.join(main_project_path, 'mkdocs.yml.template')
    with open(mkdocs_yml_template_path, 'w') as f:
        f.write("site_name: <mkdocs-project>\n")
        f.write("nav:\n")
        f.write("  - Home: index.md\n")
        f.write("theme:\n")
        f.write("  name: material\n")
        f.write("  language: <lang>\n")
        f.write("url_repo: https://github.com/<github-account>/<mkdocs-project>\n")
    print(f"Created mkdocs.yml.template at {mkdocs_yml_template_path}")

    # Create requirements.txt
    requirements_txt_path = os.path.join(main_project_path, 'requirements.txt')
    with open(requirements_txt_path, 'w') as f:
        f.write("mkdocs-material\n")
    print(f"Created requirements.txt at {requirements_txt_path}")

    # Install requirements
    pip_executable = os.path.join(venv_path, 'Scripts', 'pip') if sys.platform == 'win32' else os.path.join(venv_path, 'bin', 'pip')
    subprocess.run([pip_executable, 'install', '-r', requirements_txt_path])
    print(f"Installed requirements from {requirements_txt_path}")

    # Create repos.txt template
    repos_txt_path = os.path.join(main_project_path, 'repos.txt')
    with open(repos_txt_path, 'w') as f:
        f.write("# Example:\n")
        f.write("# git@github.com:username/repo.git --lang=en\n")
    print(f"Created repos.txt template at {repos_txt_path}")

    # Print a highlighted message for the user
    print("Please navigate to your new project directory:")
    print("\033[93m" + f"cd {main_project_path}\033[0m")