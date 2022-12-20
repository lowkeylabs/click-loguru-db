"""
Search for config file and assign it.
"""
import os
import sys
import argparse
from functools import partial

import xdg
from loguru import logger
from tomlkit import table,loads,document,dumps

import click
import click_config_file


DEFAULT_LOG_LEVEL="WARNING"
program_name = os.path.basename( sys.argv[0] ).lower()
config_file_name = (program_name + '.toml').lower()
ENV_CONFIG = program_name.upper()
ENV_LOG_LEVEL = program_name+"_LOG_LEVEL"

# Do quick check of command line for log level prior to doing anything else!

logger.trace(f"sys.argv[1:]:{sys.argv[1:]}")
parser = argparse.ArgumentParser(exit_on_error=False,add_help=False)
parser.add_argument('--log-level', default=DEFAULT_LOG_LEVEL, type=str)
parser.add_argument('--config', default=None, type=str)

args, unknown = parser.parse_known_args() # pylint: disable=multiple-statements

log_level = DEFAULT_LOG_LEVEL # pylint: disable=invalid-name

if args.log_level is not None:
    log_level = args.log_level
if os.environ.get(ENV_LOG_LEVEL) is not None:
    log_level = os.environ.get(ENV_LOG_LEVEL)
logger.remove()
logger.add(sys.stderr, level=log_level)
logger.info(f"Using log level: {args.log_level}")
logger.trace(f"Config file set on command line: {args.config}")


config = document()

logger.trace(f"Inside {__file__}")


# See: https://dirs.dev/
# https://github.com/dirs-dev/directories-rs

def log_dirs():
    """ log directories """
    global config # pylint: disable=global-statement,global-variable-not-assigned,invalid-name
    global args # pylint: disable=global-statement,global-variable-not-assigned,invalid-name
    files = {}
    files["command_line"] = args.config
    files["ENV:"+ENV_CONFIG] = os.environ.get(ENV_CONFIG)
    files["current_dir1"] = os.path.join(os.getcwd(),".config","."+config_file_name)
    files["current_dir2"] = os.path.join(os.getcwd(),".config",config_file_name)
    files["current_dir3"] = os.path.join(os.getcwd(),"config","."+config_file_name)
    files["current_dir4"] = os.path.join(os.getcwd(),"config",config_file_name)
    files["current_dir5"] = os.path.join(os.getcwd(),"."+config_file_name)
    files["current_dir6"] = os.path.join(os.getcwd(),config_file_name)

    files["config_folder1"] = os.path.join(xdg.xdg_config_home(),"."+program_name,"."+config_file_name)
    files["config_folder2"] = os.path.join(xdg.xdg_config_home(),"."+program_name,config_file_name)
    files["config_folder3"] = os.path.join(xdg.xdg_config_home(),program_name,"."+config_file_name)
    files["config_folder4"] = os.path.join(xdg.xdg_config_home(),program_name,config_file_name)
    files["config_folder5"] = os.path.join(xdg.xdg_config_home(),"."+config_file_name)
    files["config_folder6"] = os.path.join(xdg.xdg_config_home(),config_file_name)

    files["home_dir1"] = os.path.join(os.path.expanduser("~"),"."+program_name,"."+config_file_name)
    files["home_dir2"] = os.path.join(os.path.expanduser("~"),"."+program_name,config_file_name)
    files["home_dir3"] = os.path.join(os.path.expanduser("~"),program_name,"."+config_file_name)
    files["home_dir4"] = os.path.join(os.path.expanduser("~"),program_name,config_file_name)
    files["home_dir5"] = os.path.join(os.path.expanduser("~"),"."+config_file_name)
    files["home_dir6"] = os.path.join(os.path.expanduser("~"),config_file_name)

#    files["path_to_cache"] = xdg.xdg_cache_home()
#    files["path_to_data"] = xdg.xdg_data_home()
#    files["path_to_state"] = xdg.xdg_state_home()

#    files["program_name"] = os.path.basename( sys.argv[0])
#    files["path_to_program"] = os.path.dirname(os.path.realpath(__file__))
#    files["config_file_name"] = config_file_name
#    files["ENV_HOME"] = ENV_HOME
#    files["ENV:"+ENV_HOME] = os.environ.get(ENV_HOME)

    for f,g in files.items(): # pylint: disable=invalid-name
        logger.trace(f"{f}: {g}")

    for f,g in files.items(): # pylint: disable=invalid-name
        if g is not None:
            try:
                with open(g,'r',encoding='utf-8') as file:
                    config = loads(file.read())
                    logger.info(f"Using config file: {g}")
                    break
            except IOError:
                pass
    if config == document():
        logger.info("Using empty config file")

log_dirs()

click.option = partial(click.option, show_default=True)

def myprovider(file_path, cmd_name):
    """ myprovider """
    unused_file_path = file_path
    if config.get(cmd_name):
        pass
    else:
        config.add(cmd_name,table())
    return config[cmd_name]

click_config_file.configuration_option = partial(click_config_file.configuration_option,
    implicit=False,provider=myprovider, hidden=True)


# userhome: %USERPROFILE%
#$XDG_DATA_HOME = %LOCALAPPDATA%
#$XDG_DATA_DIRS = %APPDATA%
#$XDG_CONFIG_HOME = %LOCALAPPDATA%
#$XDG_CONFIG_DIRS = %APPDATA%
#$XDG_CACHE_HOME = %TEMP%
#$XDG_RUNTIME_DIR = %TEMP%


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
