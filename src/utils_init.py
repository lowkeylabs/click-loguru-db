import os, sys
import click
from loguru import logger
import click_config_file
import configparser

default_log_level = "SUCCESS"  # TRACE,DEBUG,INFO,SUCCESS,WARNING,ERROR,CRITICAL

CONFIG_FILE = "".join([ "/home/john/.config/",os.path.basename( sys.argv[0] ),".ini"])

def myprovider(file_path, cmd_name):
    config = configparser.ConfigParser(strict=False)
    config.read(CONFIG_FILE)
    if not cmd_name in config.sections():
        config.add_section(cmd_name)
    return config[cmd_name]

def MyConfig(f):
    def wrapper():
        return click_config_file.configuration_option(f(),implicit=True,config_file_name=CONFIG_FILE,provider=myprovider)
    return wrapper

