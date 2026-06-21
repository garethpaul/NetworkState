override SHELL := /bin/sh
override .SHELLFLAGS := -eu -c
override HASH := \#

ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override MAKEFILE_PATH := $(shell path='$(subst ','"'"',$(MAKEFILE_LIST))'; first=$${path%"$${path$(HASH)?}"}; if [ "$$first" = " " ]; then path=$${path$(HASH)?}; fi; if [ -f "$$path" ]; then printf '%s\n' "$$path"; fi)
ifeq ($(MAKEFILE_PATH),)
$(error this Makefile must be invoked as the only Makefile)
endif
override ROOT := $(shell path='$(subst ','"'"',$(MAKEFILE_PATH))'; root=$${path%/*}; if [ "$$root" = "$$path" ]; then root=.; fi; if [ -z "$$root" ]; then root=/; fi; printf '%s\n' "$$root")
override MAKEFILE_LIST_GUARD = $(if $(shell expected='$(subst ','"'"',$(MAKEFILE_PATH))'; actual='$(subst ','"'"',$(MAKEFILE_LIST))'; first=$${actual%"$${actual$(HASH)?}"}; if [ "$$first" = " " ]; then actual=$${actual$(HASH)?}; fi; if [ "$$actual" = "$$expected" ]; then :; else printf '%s\n' fail; fi),$(error additional Makefiles are not allowed; invoke this Makefile as the only Makefile))

.PHONY: build check lint static-check test verify
.SECONDEXPANSION:
build check lint static-check test verify: $$(MAKEFILE_LIST_GUARD)

check: verify

lint test build verify: static-check

static-check:
	/usr/bin/python3 "$(ROOT)/scripts/check-baseline.py"
	PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -m unittest discover -s "$(ROOT)/tests" -p 'test_*.py'
