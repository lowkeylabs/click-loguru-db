.SILENT:
# assumes that \program files\git\usr\bin is on path AND sh.exe in same folder is remove/renamed

.PHONY: commands
commands:
	echo Default makefile commands
	cat Makefile | grep -i ".title=" | tail -n +2 | sed -e "s/.title=/ -\> /g" -e "s/^/\t/"

.PHONY: test
test.title=run pytest
test:
	poetry run pytest


.PHONY: lint
lint.title=run pylint on src folder
lint:
	echo Running pylint
	poetry run pylint ./src

.PHONY: coverage
coverage.title=run coverage
coverage:
	poetry run coverage report -m

.PHONY: all
all.title=run test lint coverage
all: test lint coverage
	@echo.
