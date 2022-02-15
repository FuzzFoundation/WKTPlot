PROJ_BASE=$(shell pwd)
PYTHONVENV=$(PROJ_BASE)/venv
ifeq ($(OS),Windows_NT)
	VENVPYTHON=$(PYTHONVENV)/Scripts/python
else
	VENVPYTHON=$(PYTHONVENV)/bin/python
endif

PHONY: help
help: ## Show this help menu.
	@echo "Usage: make [TARGET ...]"
	@echo ""
	@grep --no-filename -E '^[a-zA-Z_%-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-10s %s\n", $$1, $$2}'

PHONY: init
init: ## Create Python virtual environment for local development.
	@echo "Creating virtual environment 'venv'."
	python3 -m venv venv || python -m venv venv
	$(VENVPYTHON) -m pip install --upgrade setuptools pip pip-tools

PHONY: develop
develop: ## Install `wktplot` library in editable mode.
	init
	@echo "Installing wktplot, with editible modules"
	$(VENVPYTHON) -m pip install --editable .[test]

PHONY: build
build: ## Build `wktplot` wheel.
	$(VENVPYTHON) -m pip install build
	$(VENVPYTHON) -m build --wheel

PHONY: clean
clean: ## Remove build & testing artifacts.
	@echo "Removing build artifacts"
	rm -rf $(PROJ_BASE)/build
	rm -rf $(PROJ_BASE)/dist
	rm -rf $(PROJ_BASE)/src/*.egg-info
	rm -rf $(PROJ_BASE)/docs/_build/*
	rm -f $(PROJ_BASE)/coverage.xml
	rm -f $(PROJ_BASE)/.coverage

PHONY: sparkling
sparkling: ## Remove build & testing artifacts. Also deletes virtual environment.
	clean
	rm -rf $(PROJ_BASE)/venv*
	rm -rf $(PROJ_BASE)/.pytest_cache

PHONY: test
test:  ## Run unittests and flake8.
	$(VENVPYTHON) -m flake8 .
	$(VENVPYTHON) -m pytest
