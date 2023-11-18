"""
PYCLI initialization
"""
import os
from pathlib import Path
import sys
import argparse
from functools import partial
from urllib.request import build_opener
import xdg
from loguru import logger
from tomlkit import table,loads,document,dumps

import click
import click_config_file


DEFAULT_LOG_LEVEL="WARNING"
CURRENT_LOG_LEVEL=DEFAULT_LOG_LEVEL
logger.remove()
logger.add(sys.stderr, level=CURRENT_LOG_LEVEL)

program_name = os.path.basename( sys.argv[0] ).lower()
## program_name = "builder" # pylint: disable=invalid-name


config_file_name = (program_name + '.toml').lower() # pylint: disable=invalid-name
ENV_CONFIG = program_name.upper()
ENV_LOG_LEVEL = ENV_CONFIG+"_LOG_LEVEL"
config = document()


def quick_arg_list():
    ''' a quick peek at arg list prior to CLICK running '''
    parser = argparse.ArgumentParser(exit_on_error=False,add_help=False)
    parser.add_argument('--log-level', default=DEFAULT_LOG_LEVEL, type=str)
    parser.add_argument('--config', default=None, type=str)
    (args, unknown) = parser.parse_known_args() # pylint: disable=unused-variable
    return args


def set_log_level( new_log_level, msg = "" ):
    ''' set log level only if log level is changed '''
    global CURRENT_LOG_LEVEL # pylint: disable=invalid-name,global-variable-not-assigned,global-statement
    if new_log_level is not None:
        if new_log_level != CURRENT_LOG_LEVEL:
            CURRENT_LOG_LEVEL = new_log_level
            logger.remove()
            logger.add(sys.stderr, level=CURRENT_LOG_LEVEL)
            logger.debug(f"Setting log level to {CURRENT_LOG_LEVEL} {msg}")


def init_logger_and_level( args ):
    ''' init logger and level using apprpriate '''
    log_level = DEFAULT_LOG_LEVEL # pylint: disable=invalid-name
    msg = ""
    if args.log_level is not None:
        log_level = args.log_level
        msg = "(command line arg)"
    if os.environ.get(ENV_LOG_LEVEL) is not None:
        log_level = os.environ.get(ENV_LOG_LEVEL)
        msg = "(environment variable)"
    set_log_level( log_level,msg )

# See: https://dirs.dev/
# https://github.com/dirs-dev/directories-rs

def search_and_set_config(args):
    """ Search lots of places for config file """
    global config_file_name # pylint: disable=invalid-name,global-variable-not-assigned, global-statement
    tempconfig = document()
    files = {}

    # highest priorities are command line then environment
    files["command_line"] = args.config
    files["ENV:"+ENV_CONFIG] = os.environ.get(ENV_CONFIG)

    # look in current folder structure.  Current folder first
    files["current_dir"] = os.path.join(os.getcwd(),config_file_name)

    # Look for config and .config folders/files under current directory
    files["current_dir1"] = os.path.join(os.getcwd(),".config","."+config_file_name)
    files["current_dir2"] = os.path.join(os.getcwd(),".config",config_file_name)
    files["current_dir3"] = os.path.join(os.getcwd(),"config","."+config_file_name)
    files["current_dir4"] = os.path.join(os.getcwd(),"config",config_file_name)
    files["current_dir5"] = os.path.join(os.getcwd(),"."+config_file_name)

    # look up the parent directory chain to the drive root/anchor
    path = Path(os.getcwd()).resolve()
    i = 0
    while path.absolute() != path.parent.absolute():
        i = i + 1
        pathdir = path.parent.absolute()
        logger.trace(f"parent_dir{i}  {path}  {path.anchor}")
        files[f"parent_dir{i}"] = os.path.join(pathdir,"."+config_file_name)
        i = i + 1
        files[f"parent_dir{i}"] = os.path.join(pathdir,config_file_name)
        path = Path(pathdir).resolve()

    # look in XDG config home.  Does not use %APPDATA%, assumes .config
    files["config_folder1"] = os.path.join(xdg.xdg_config_home(),"."+program_name,"."+config_file_name)
    files["config_folder2"] = os.path.join(xdg.xdg_config_home(),"."+program_name,config_file_name)
    files["config_folder3"] = os.path.join(xdg.xdg_config_home(),program_name,"."+config_file_name)
    files["config_folder4"] = os.path.join(xdg.xdg_config_home(),program_name,config_file_name)
    files["config_folder5"] = os.path.join(xdg.xdg_config_home(),"."+config_file_name)
    files["config_folder6"] = os.path.join(xdg.xdg_config_home(),config_file_name)

    # look in user home
    files["home_dir1"] = os.path.join(os.path.expanduser("~"),"."+program_name,"."+config_file_name)
    files["home_dir2"] = os.path.join(os.path.expanduser("~"),"."+program_name,config_file_name)
    files["home_dir3"] = os.path.join(os.path.expanduser("~"),program_name,"."+config_file_name)
    files["home_dir4"] = os.path.join(os.path.expanduser("~"),program_name,config_file_name)
    files["home_dir5"] = os.path.join(os.path.expanduser("~"),"."+config_file_name)
    files["home_dir6"] = os.path.join(os.path.expanduser("~"),config_file_name)

    # now that list is build log it to TRACE
    for (key,value) in files.items():
        logger.trace(f"{key}: {value}")

    # search each folder attempting to use config file
    for (key,value) in files.items():
        if value is not None:
            try:
                with open(value,'r',encoding='utf-8') as file:
                    tempconfig = loads(file.read())
                    logger.debug(f"current log level: {CURRENT_LOG_LEVEL}")
                    logger.debug(f"Using config file ({key}): {value}")
                    config_file_name = value
                    break
            except IOError:
                pass
    # set empty config
    if tempconfig == document():
        logger.debug("Using empty config file")

    return tempconfig

tempargs = quick_arg_list()
init_logger_and_level( tempargs )

# write messages now that logger is set up
logger.trace(f"Inside {__file__}")
logger.trace(f"sys.argv[1:]:{sys.argv[1:]}")
#logger.info(f"Using log level: {CURRENT_LOG_LEVEL}")

# Now that logger is set, set up config with tracing

config = search_and_set_config( tempargs )
if "log_level" in config.keys():
    set_log_level( config["log_level"],"(config file)" )

# helpers using "partial" to change signatures


def myprovider( file_path, cmd_name ):  # pylint: disable=unused-argument
    """ Used by "click_config_file" to set click arg defaults from values in a config file """
    global config # pylint: disable=invalid-name,global-variable-not-assigned
    if config.get(cmd_name):
        pass
    else:
        config.add(cmd_name,table())
    logger.trace(f"command={cmd_name} - dictionary:{config[cmd_name]}")
    return config[cmd_name]

click.option = partial(click.option, show_default=True)

click_config_file.configuration_option = partial(
    click_config_file.configuration_option,implicit=False, provider=myprovider, hidden=True
    )



## other documentation of places to look using XDG standard

#    files["path_to_cache"] = xdg.xdg_cache_home()
#    files["path_to_data"] = xdg.xdg_data_home()
#    files["path_to_state"] = xdg.xdg_state_home()

# windows assignments
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
