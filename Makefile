WEEK ?= 04

.PHONY: test

test:
	python3 -m pytest -q weeks/week-$(WEEK)/tests
