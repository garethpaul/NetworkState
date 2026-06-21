override SHELL := /bin/sh
override .SHELLFLAGS := -eu -c
override HASH := \#

ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override MAKEFILE_PATH := $(shell path='$(subst ','"'"',$(MAKEFILE_LIST))'; first=$${path%"$${path$(HASH)?}"}; if [ "$$first" = " " ]; then path=$${path$(HASH)?}; fi; if [ -f "$$path" ]; then printf '%s\n' "$$path"; fi)
ifeq ($(MAKEFILE_PATH),)
$(error this Makefile must be invoked directly as the checked-in Makefile)
endif
override ROOT := $(shell path='$(subst ','"'"',$(MAKEFILE_PATH))'; root=$${path%/*}; if [ "$$root" = "$$path" ]; then root=.; fi; if [ -z "$$root" ]; then root=/; fi; printf '%s\n' "$$root")

.PHONY: build check lint static-check test verify

check: verify

lint test build verify: static-check

static-check:
	/usr/bin/python3 "$(ROOT)/scripts/check-baseline.py"
	PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -m unittest discover -s "$(ROOT)/tests" -p 'test_*.py'
