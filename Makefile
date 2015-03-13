SHELL := /bin/sh

LOCALPATH := ./src
PYTHONPATH := $(LOCALPATH)/
PYTHON_BIN := PYTHONPATH=$(PYTHONPATH) $(VIRTUAL_ENV)/bin

.PHONY: clean cleanall coverage register sdist showenv test upload

showenv:
	@echo 'Environment:'
	@echo '-----------------------'
	@python -c "import sys; print 'sys.path:', sys.path"
	@echo 'PYTHONPATH:' $(PYTHONPATH)

clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
	-rm -rf htmlcov
	-rm -rf .coverage
	-rm -rf build
	-rm -rf dist
	-rm -rf src/*.egg-info
	-rm -rf interlinears/__pycache__

cleanall: clean
	-rm -rf .tox

test: clean
	-$(PYTHON_BIN)/coverage run $(LOCALPATH)/interlinears/tests.py

coverage:
	$(PYTHON_BIN)/coverage html --include="$(LOCALPATH)/*" --omit="*/test*"

register:
	python setup.py register

sdist:
	python setup.py sdist

upload: sdist
	python setup.py sdist upload
	make clean
