PROJ_BASE=$(shell pwd)
PYTHONVENV=$(PROJ_BASE)/venv
VENVPYTHON=$(PYTHONVENV)/bin/python

PHONY: init
init:
	@echo "Creating virtual environment 'venv' for development."
	python3 -m venv venv || python -m venv venv
	$(VENVPYTHON) -m pip install --upgrade setuptools pip
	@echo "\nYou may want to activate the virtual environmnent with 'source venv/bin/activate'\n"

PHONY: develop
develop:
	@echo "Installing wktplot, with editible modules ('python -m pip install --editable .[test]')"
	$(VENVPYTHON) -m pip install --editable .[test]

PHONY: build
build:
	flake8 .
	$(VENVPYTHON) -m pip install build
	$(VENVPYTHON) -m build

PHONY: clean
clean:
	@echo "Removing build artifacts"
	rm -rf $(PROJ_BASE)/build
	rm -rf $(PROJ_BASE)/dist
	rm -rf $(PROJ_BASE)/src/*.egg-info
	rm -rf $(PROJ_BASE)/docs/_build/*
	rm -f $(PROJ_BASE)/*coverage*
	rm -rf $(PROJ_BASE)/tests/htmlcov

PHONY: sparkling
sparkling: clean
	rm -rf $(PROJ_BASE)/venv*

PHONY: upload
upload:
	$(VENVPYTHON) -m twine upload dist/*

PHONY: test
test:
	rm -f .coverage
	rm -rf tests/htmlcov
	$(VENVPYTHON) -m tox
	$(VENVPYTHON) -m flake8 .
