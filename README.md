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

1. ~~test within makefile environment~~

## Resources

https://www.digitalocean.com/community/tutorials/

how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application

https://docs.sqlalchemy.org/en/20/orm/quickstart.html

https://python-poetry.org/docs/basic-usage/

https://dev.to/drcloudycoder/develop-python-cli-with-subcommands-using-click-4892

https://dev.to/bowmanjd/build-command-line-tools-with-python-poetry-4mnc

https://towardsdatascience.com/here-is-the-reason-why-sqlalchemy-is-so-popular-43b489d3fb00
