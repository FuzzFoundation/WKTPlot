PROJ_BASE=$(shell pwd)
PYTHONVENV=$(PROJ_BASE)/venv
ifeq ($(OS),Windows_NT)
	VENVPYTHON=$(PYTHONVENV)/Scripts/python
else
	VENVPYTHON=$(PYTHONVENV)/bin/python
endif

PHONY: init
init:
	@echo "Creating virtual environment 'venv'."
	python3 -m venv venv || python -m venv venv
	$(VENVPYTHON) -m pip install --upgrade setuptools pip

PHONY: develop
develop:
	@echo "Installing wktplot, with editible modules ('python -m pip install --editable .[test]')"
	$(VENVPYTHON) -m pip install --editable .[test]

PHONY: build
build:
	$(VENVPYTHON) -m pip install build
	$(VENVPYTHON) -m build --wheel

PHONY: clean
clean:
	@echo "Removing build artifacts"
	rm -rf $(PROJ_BASE)/build
	rm -rf $(PROJ_BASE)/dist
	rm -rf $(PROJ_BASE)/src/*.egg-info
	rm -rf $(PROJ_BASE)/docs/_build/*
	rm -f $(PROJ_BASE)/*coverage*

PHONY: sparkling
sparkling: clean
	rm -rf $(PROJ_BASE)/venv*

PHONY: test
test:
	$(VENVPYTHON) -m flake8 .
	$(VENVPYTHON) -m pytest
