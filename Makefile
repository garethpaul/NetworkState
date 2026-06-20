override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

.PHONY: build check lint static-check test verify

check: verify

lint test build verify: static-check

static-check:
	python3 "$(ROOT)/scripts/check-baseline.py"
