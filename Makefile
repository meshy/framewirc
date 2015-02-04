SHELL := /bin/bash

help:
	@echo "Usage:"
	@echo " make test | Run the tests."

test:
	@coverage run -m unittest discover
	@coverage report --show-missing
	@flake8

release:
	python setup.py register sdist bdist_wheel upload
