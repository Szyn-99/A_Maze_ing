POETRY=poetry
SHELL := /bin/bash

define CECHO
	@echo -e "\033[1;32m$1\033[0m"
endef

install:
	$(call CECHO,Installing dependencies with Poetry...)
	$(POETRY) install --no-root

run:
	$(call CECHO,Running main script in Poetry environment...)
	$(POETRY) run python a_maze_ing.py config.txt

debug:
	$(call CECHO,Running in debug mode with Poetry...)
	$(POETRY) run python -m pdb a_maze_ing.py config.txt

clean:
	$(call CECHO,Cleaning temporary files...)
	rwm -rf __pycache__ .mypy_cache

lint:
	$(call CECHO,Running flake8...)
	$(POETRY) run flake8 .
	$(call CECHO,Running mypy...)
	$(POETRY) run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	