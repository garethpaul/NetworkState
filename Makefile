.PHONY: build check lint static-check test verify

check: verify

lint test build verify: static-check

static-check:
	python3 scripts/check-baseline.py
