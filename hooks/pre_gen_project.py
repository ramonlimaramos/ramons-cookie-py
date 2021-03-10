import re
import sys
import subprocess as sp
from subprocess import CalledProcessError

VIRTUALENV_INSTALL_INSTRUCTIONS = """
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
| virtualenv is not installed!                                                |
| Please refer to https://pypi.org/project/virtualenv/ for instructions.      |
| In most systems, a `pip install virtualenv` is enough.                      |
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
"""

PYTHON_INSTALL_INSTRUCTIONS = """
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
| {{cookiecutter.pyrunner}} is not installed!                                 |
| Please refer to https://www.python.org/download for instructions.           |
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
"""

MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'
module_name = '{{cookiecutter.pkg_name}}'


def check_py_version(cmd):
    """
    checks if `cmd` exists in the current shell
    """

    # Usually, I check for existence using `which`
    # Apparently, this is not a good practice
    # see: https://stackoverflow.com/a/677212/2713733

    # If we're running Python 2
    if sys.version_info < (3,):
        sys.exit('This boilerplate does not support python 2 only python3.6+')

    # If we're running Python 3
    from shutil import which

    return which(cmd) is not None


def exist_internal_cmd(cmd):

    try:
        sp.run(cmd, stdout=sp.PIPE, check=True, universal_newlines=True)
        return True
    except CalledProcessError as e:
        return False


if __name__ == '__main__':

    if not re.match(MODULE_REGEX, module_name):
        print('ERROR: The directory name (%s) is not a valid Python module name. Please do not use a - and use _ instead' % module_name)
        #Exit to cancel project
        sys.exit(1)

    if not check_py_version('{{cookiecutter.pyrunner}}'):
        sys.exit(PYTHON_INSTALL_INSTRUCTIONS)

    if not exist_internal_cmd(['{{cookiecutter.pyrunner}}', '-m', 'virtualenv', '-h']):
        sys.exit(VIRTUALENV_INSTALL_INSTRUCTIONS)