SHELL := /bin/bash

help:
	@echo "Usage:"
	@echo " make test | Run the tests."

test:
	@coverage run -m py.test
	@coverage report
	@flake8
	@isort --check

release:
	python setup.py register sdist bdist_wheel upload
