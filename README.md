# pycli-click-loguru-db

Template for creating new CLI with connections to DB and loguru

[Best practices markdown reference](https://www.markdownguide.org/basic-syntax/#overview)
[Quarto markdown reference](https://quarto.org/docs/authoring/markdown-basics.html)

## Features to add

1. pycli config  (see config file processing. Store/update vars in config file)

1. pycli versions (check to see if desired environment is set up)
   a. check pyenv version
   b. check poetry version
   c. check python version
   d. check make version
   e. check sed version
   f. check grep version
   g. check OS type/version (e.g. mac / linux / windows / powershell)
   enable additional checks to be stored in config file

## Things to do

1. ~~get test harness running~~

1. flask api back end to a database

1. click front end to run queries through the api and display results

1. add pyreporter functionality for gsheets push and pull?

1. explore how to install on new computer.

1. test within makefile environment

## Config file processing

This order was borrowed from [pylint docs](https://pylint.pycqa.org/en/latest/user_guide/usage/run.html).

1. pylintrc in the current working directory

1. .pylintrc in the current working directory

1. pyproject.toml in the current working directory, providing it has at least one tool.pylint. section. The pyproject.toml must prepend section names with tool.pylint., for example [tool.pylint.'MESSAGES CONTROL']. They can also be passed in on the command line.

1. setup.cfg in the current working directory, providing it has at least one pylint. section

1. If the current working directory is in a Python package, Pylint searches up the hierarchy of Python packages until it finds a pylintrc file. This allows you to specify coding standards on a module-by-module basis. Of course, a directory is judged to be a Python package if it contains an __init__.py file.

1. The file named by environment variable PYLINTRC

1. if you have a home directory which isn't /root:

1. .pylintrc in your home directory

1. .config/pylintrc in your home directory

1. /etc/pylintrc

## Resources

https://www.digitalocean.com/community/tutorials/

how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application

https://docs.sqlalchemy.org/en/20/orm/quickstart.html

https://python-poetry.org/docs/basic-usage/

https://dev.to/drcloudycoder/develop-python-cli-with-subcommands-using-click-4892

https://dev.to/bowmanjd/build-command-line-tools-with-python-poetry-4mnc

https://towardsdatascience.com/here-is-the-reason-why-sqlalchemy-is-so-popular-43b489d3fb00
