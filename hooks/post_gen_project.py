import os


def remove_travis_file():
    os.remove(".travis.yml")


def remove_gitlabci_file():
    os.remove(".gitlab-ci.yml")


def main():

    if "{{ cookiecutter.ci_tool }}".lower() != "travis":
        remove_travis_file()

    if "{{ cookiecutter.ci_tool }}".lower() != "gitlab":
        remove_gitlabci_file()


if __name__ == "__main__":
    main()
