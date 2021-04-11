PROJ_BASE=$(shell pwd)
PYTHONVER=python3.9
PYTHONVENV=$(PROJ_BASE)/venv
VENVPYTHON=$(PYTHONVENV)/bin/$(PYTHONVER)

install: bootstrap
	@echo "Installing WKTPlot"
	$(VENVPYTHON) setup.py install
	@echo "\nYou may want to activate the virtual environmnent with 'source venv/bin/activate'\n"

develop: bootstrap
	@echo "Installing WKTPlot, with editible modules ('python setup.py develop')"
	$(VENVPYTHON) setup.py develop
	@echo "\nYou may want to activate the virtual environmnent with 'source venv/bin/activate'\n"

bootstrap:
	@echo "Creating virtual environment 'venv' for development."
	$(PYTHONVER) -m virtualenv -p $(PYTHONVER) venv
	@echo "Installing python modules from requirements.txt"
	$(VENVPYTHON) -m pip install -r requirements.txt

clean_build:
	@echo "Removing build artifacts"
	rm -rf $(PROJ_BASE)/build
	rm -rf $(PROJ_BASE)/dist
	rm -rf $(PROJ_BASE)/*.egg-info

build: clean_build
	@echo "Building python source distribution and wheel"
	$(VENVPYTHON) setup.py sdist bdist_wheel

upload:
	$(VENVPYTHON) -m twine upload dist/*

test:
	$(VENVPYTHON) -m pip install -r ci-cd-requirements.txt
	$(VENVPYTHON) -m tox

clean:
	@echo "Removing Python virtual environment 'venv'."
	rm -rf $(PYTHONVENV)
	rm -rf .tox

sparkling: clean
	rm -rf *.whl
	find . -name \*~ | xargs rm -f
	rm -rf dist build src/*.egg-info
	rm -rf **/__pycache__
	rm -rf docs/_build/*
	rm -f src/version.py
	rm -rf htmlcov
	rm -rf coverage.xml
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -f .coverage
	rm -rf .vscode

.PHONY: install develop bootstrap clean_build build test clean sparkling upload
