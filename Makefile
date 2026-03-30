PYTHON := .venv/bin/python
PYTEST := $(PYTHON) -m pytest
RUN := PYTHONPATH=src $(PYTHON) main.py

.PHONY: all test run clean

all: test run

test:
	PYTHONPATH=src $(PYTEST) tests

run:
	$(RUN)

clean:
	rm -rf output .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
