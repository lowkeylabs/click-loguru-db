''' DOCSTRING for utils_init.py
'''
import os
import sys
#import configparser
from functools import partial
import click

import click_config_file
from loguru import logger
from tomlkit import table,loads,document

DEFAULT_LOG_LEVEL = "SUCCESS"  # TRACE,DEBUG,INFO,SUCCESS,WARNING,ERROR,CRITICAL


CONFIG_FILE1 = "".join(["~/.",os.path.basename( sys.argv[0] ),"/",os.path.basename( sys.argv[0] ),".toml"])
CONFIG_FILE2 = os.path.join(os.getcwd(),"".join([os.path.basename( sys.argv[0] ),".toml"]))

click.option = partial(click.option, show_default=True)

## Modify myprovider to look for configuration in these places:
## This order was borrowed from [pylint docs](https://pylint.pycqa.org/en/latest/user_guide/usage/run.html).
##
# a. pylintrc in the current working directory
# b. .pylintrc in the current working directory
# c. pyproject.toml in the current working directory, providing it has at least one tool.pylint. section.
#    The pyproject.toml must prepend section names with tool.pylint., for example [tool.pylint.'MESSAGES CONTROL'].
#    They can also be passed in on the command line.
# d. setup.cfg in the current working directory, providing it has at least one pylint. section
# e. If the current working directory is in a Python package, Pylint searches up the hierarchy of Python packages
#    until it finds a pylintrc file. This allows you to specify coding standards on a module-by-module basis. Of
#    course, a directory is judged to be a Python package if it contains an __init__.py file.
# f. The file named by environment variable PYLINTRC
# g. if you have a home directory which isn't /root:
# h. .pylintrc in your home directory
# i. .config/pylintrc in your home directory
# j. /etc/pylintrc


def myprovider(file_path, cmd_name):
    """ myprovider """
    unused_file_path = file_path
    config = document()
    try:
        logger.trace(f"searching: {CONFIG_FILE2}")
        with open(CONFIG_FILE2,'r',encoding='utf-8') as file:
            config = loads(file.read())
        logger.info(f"Using: {CONFIG_FILE2}")
    except FileNotFoundError:  # pylint: disable=broad-except
        logger.debug(f"Not found: {CONFIG_FILE2}")
        try:
            logger.trace(f"searching:{CONFIG_FILE1}")
            with open(os.path.expanduser(CONFIG_FILE1),'r',encoding='utf-8') as file:
                config = loads(file.read())
            logger.info(f"Using: {CONFIG_FILE1}")
        except FileNotFoundError:  # pylint: disable=broad-except
            logger.debug(f"Not found: {CONFIG_FILE1}")
            config = document()
            logger.info("No configuration files found")
    if config.get(cmd_name):
        pass
    else:
        config.add(cmd_name,table())
    return config[cmd_name]

click_config_file.configuration_option = partial(click_config_file.configuration_option,
    implicit=True,provider=myprovider)
