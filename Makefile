SHELL := /bin/bash

RED := \033[0;31m
GREEN := \033[0;32m
PURPLE := \033[1;35m
RESET := \033[0m
FAILURE := (echo -e "${RED}FAILURE${RESET}" && exit 1)
SUCCESS := echo -e "${GREEN}SUCCESS${RESET}"
RESULT := && ${SUCCESS} || ${FAILURE}

help:
	@echo "Usage:"
	@echo " make test | Run the tests."

test:
	@echo -e "${PURPLE}Run tests:${RESET}"
	@coverage run -m py.test ${RESULT}
	@echo -e "\n${PURPLE}Check for untested code:${RESET}"
	@coverage report ${RESULT}
	@echo -e "\n${PURPLE}Check for flake8 violations:${RESET}"
	@flake8 ${RESULT}
	@echo -e "\n${PURPLE}Check for unsorted imports:${RESET}"
	@isort --check ${RESULT}

release:
	python setup.py register sdist bdist_wheel upload
