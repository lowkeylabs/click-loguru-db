import os, sys
import click
from loguru import logger
import click_config_file
import configparser
import tomlkit
from tomlkit import *

default_log_level = "SUCCESS"  # TRACE,DEBUG,INFO,SUCCESS,WARNING,ERROR,CRITICAL

CONFIG_FILE1 = "".join(["~/.config/",os.path.basename( sys.argv[0] ),".toml"])
CONFIG_FILE2 = os.path.join(os.getcwd(),"".join([os.path.basename( sys.argv[0] ),".toml"]))

from functools import partial
import click
click.option = partial(click.option, show_default=True)


def myprovider2(file_path, cmd_name):
    config = configparser.ConfigParser(strict=False)
    config.read(CONFIG_FILE1)
    if not cmd_name in config.sections():
        config.add_section(cmd_name)
    return config[cmd_name]


def myprovider(file_path, cmd_name):
    try:
        config = tomlkit.loads(open(CONFIG_FILE2).read())
#        click.echo(f"found: {CONFIG_FILE2}")
    except Exception as e:
#        click.echo(f"failed: {str(e)}")
        try:
#            click.echo(f"found:{CONFIG_FILE1}")
            config = tomlkit.loads(open(os.path.expanduser(CONFIG_FILE1)).read())
        except Exception as e:
#            click.echo(f"failed again:{str(e)}")
            config = tomlkit.document()
    if tb := config.get(cmd_name):
        pass
    else:
        config.add(cmd_name,table())
    return config[cmd_name]

click_config_file.configuration_option= partial(click_config_file.configuration_option,implicit=True,provider=myprovider)
