.SILENT:
# assumes that \program files\git\usr\bin is on path AND sh.exe in same folder is remove/renamed

.PHONY: help
help:
	echo Default makefile commands
	cat Makefile | grep -i ".title=" | tail -n +2 | sed -e "s/.title=/ -\> /g" -e "s/^/\t/"

.PHONY: cmd1
cmd1.title=does X
cmd1:
	@echo $($(@).title)


.PHONY: cmd2
cmd2.title=does Y
cmd2:
	@echo $($(@).title)

.PHONY: cmd3
cmd3.title=does Z
cmd3:
	@echo $($(@).title)

.PHONY: cmd4
cmd4.title=does A
cmd4:
	@echo $($(@).title)
