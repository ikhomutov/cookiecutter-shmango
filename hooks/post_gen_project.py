import os
import shutil
import subprocess


def remove_travis_file():
    os.remove(".travis.yml")


def remove_gitlabci_file():
    os.remove(".gitlab-ci.yml")


def remove_drf_files():
    shutil.rmtree(
        os.path.join("{{ cookiecutter.project_slug }}", "apps", "api")
    )


def remove_custom_user_app():
    shutil.rmtree(
        os.path.join("{{ cookiecutter.project_slug }}", "apps", "users")
    )


def remove_custom_user_tests():
    shutil.rmtree(os.path.join("tests", "unit", "user"))


def remove_docker_files():
    shutil.rmtree("docker")
    os.remove("docker-compose.yaml")
    os.remove("compose.env.example")


def remove_celery_files():
    os.remove(os.path.join("{{ cookiecutter.project_slug }}", "celery.py"))


def remove_heroku_files():
    os.remove("Procfile")
    os.remove("runtime.txt")
    os.remove("requirements.txt")


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

    if "{{ cookiecutter.use_rest_framework }}".lower() == "n":
        remove_drf_files()

    if "{{ cookiecutter.custom_user_model }}".lower() == "n":
        remove_custom_user_app()
        remove_custom_user_tests()

    if "{{ cookiecutter.use_docker }}".lower() == "n":
        remove_docker_files()

    if "{{ cookiecutter.use_celery }}".lower() == "n":
        remove_celery_files()

    if "{{ cookiecutter.heroku_deploy }}".lower() == "n":
        remove_heroku_files()

    if "{{ cookiecutter.initialize_git }}".lower() != "n":
        initialize_git()

    if "{{ cookiecutter.initialize_venv }}".lower() != "n":
        initialize_venv()


if __name__ == "__main__":
    main()
