import os
import shutil


def remove_travis_file():
    os.remove(".travis.yml")


def remove_gitlabci_file():
    os.remove(".gitlab-ci.yml")


def remove_drf_files():
    shutil.rmtree(os.path.join("{{ cookiecutter.project_slug }}", "apps", "api"))


def remove_functional_tests():
    shutil.rmtree(os.path.join("tests", "functional"))


def main():

    if "{{ cookiecutter.ci_tool }}".lower() != "travis":
        remove_travis_file()

    if "{{ cookiecutter.ci_tool }}".lower() != "gitlab":
        remove_gitlabci_file()

    if "{{ cookiecutter.use_rest_framework }}".lower() != "y":
        remove_drf_files()
        remove_functional_tests()


if __name__ == "__main__":
    main()
