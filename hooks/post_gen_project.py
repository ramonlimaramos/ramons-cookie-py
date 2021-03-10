"""
Commands that are executed by Cookiecutter
after a project is generated
"""
import logging
import json
import pathlib
import subprocess
import os


ENVIRONEMT_ISSUE = """
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
| make could not install environment!                                         |
| Please refer to https://pypi.org/project/virtualenv/ for instructions.      |
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
"""


GREETING = """
 ____    ____  ___ ___   ___   ____   _____          __   ___    ___   __  _  ____    ___ 
|    \  /    ||   |   | /   \ |    \ / ___/         /  ] /   \  /   \ |  |/ ]|    |  /  _]
|  D  )|  o  || _   _ ||     ||  _  (   \_  _____  /  / |     ||     ||  ' /  |  |  /  [_ 
|    / |     ||  \_/  ||  O  ||  |  |\__  ||     |/  /  |  O  ||  O  ||    \  |  | |    _]
|    \ |  _  ||   |   ||     ||  |  |/  \ ||_____/   \_ |     ||     ||     \ |  | |   [_ 
|  .  \|  |  ||   |   ||     ||  |  |\    |      \     ||     ||     ||  .  | |  | |     |
|__|\_||__|__||___|___| \___/ |__|__| \___|       \____| \___/  \___/ |__|\_||____||_____|
                                                                                          
____ _  _  _ ____ _   _   /
|___ |\ |  | |  |  \_/   / 
|___ | \| _| |__|   |   .  
                           
"""


NEXT_STEPS = """
. Change to directory of your brand new project.
    cd {{cookiecutter.directory_name}}

. Then just execute:
    make
"""


def init_git():
    """
    Initializes a git repo in the newly created folder
    """
    os.system("git init")


def init_venv():
    """
    Initializes a virtualenv
    """
    subprocess.run(['{{cookiecutter.pyrunner}}', '-m', 'virtualenv', 'venv'], 
        check=True, universal_newlines=True, stdout=subprocess.PIPE)


def make():
    """
    Starts make files in order to set it up the application
    """
    os.system("make")


def send_greetings():
    """
    Sends a greeting!
    """
    print(GREETING)


def send_next_steps():
    """
    Sends a next steps
    """
    print(NEXT_STEPS)


def install_pre_commit():
    """
    Installs the git hooks through Pre-Commit
    """
    os.system("pre-commit install --install-hooks")
    os.system("pre-commit install -t pre-push")


def instal_poetry_dependencies():
    """
    Installs all the dependencies defined in poetry
    """
    os.system("poetry install")


def set_vscode_python_path():
    """
    Sets VSCode's `python.pythonPath` to the
    current interpreter managed by Poetry
    """
    result = subprocess.run(
        ["poetry", "run", "which", "python"], stdout=subprocess.PIPE, check=True
    )
    python_path = result.stdout.decode("utf-8")[:-1]

    settings_path = pathlib.Path(".vscode/settings.json")

    if not settings_path.is_file():
        logging.warning(".vscode/settings.json not found. Skipping pythonPath setting.")
        return

    settings = json.load(open(settings_path))

    if "python.pythonPath" in settings:
        logging.warning(
            "There already is a 'pythonPath' entry. Skipping pythonPath setting."
        )

    settings["python.pythonPath"] = python_path

    json.dump(settings, open(settings_path, "wt"), indent=4, sort_keys=True)


if __name__ == "__main__":
    send_greetings()
    init_git()
    send_next_steps()
    # init_venv()
    # make()
    # instal_poetry_dependencies()
    # install_pre_commit()
    # set_vscode_python_path()
