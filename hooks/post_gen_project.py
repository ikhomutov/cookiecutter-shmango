import os
import shutil
import subprocess


def remove_travis_file():
    os.remove(".travis.yml")


def remove_gitlabci_file():
    os.remove(".gitlab-ci.yml")


def remove_drf_files():
    shutil.rmtree(os.path.join("{{ cookiecutter.project_slug }}", "apps", "api"))


def remove_functional_tests():
    shutil.rmtree(os.path.join("tests", "functional"))


def initialize_git():
    subprocess.call(['git', 'init'])


def initialize_venv():
    try:
        subprocess.call(['python3.7', '-m', 'venv', 'venv'])
        subprocess.call(['venv/bin/pip', 'install', '-r', 'requirements/dev.txt'])
        if "{{ cookiecutter.initialize_git }}".lower() != "n":
            subprocess.call(['venv/bin/pre-commit', 'install'])
    except FileNotFoundError:
        print("ERROR: No executable file found for python 3.7")


def main():

    if "{{ cookiecutter.ci_tool }}".lower() != "travis":
        remove_travis_file()

    if "{{ cookiecutter.ci_tool }}".lower() != "gitlab":
        remove_gitlabci_file()

    if "{{ cookiecutter.use_rest_framework }}".lower() != "y":
        remove_drf_files()
        remove_functional_tests()

    if "{{ cookiecutter.initialize_git }}".lower() != "n":
        initialize_git()

    if "{{ cookiecutter.initialize_venv }}".lower() != "n":
        initialize_venv()


if __name__ == "__main__":
    main()
