define green_color
	@echo -e "\033[1;32m$1\033[0m"
endef

install:
	$(call green_color,Installing dependencies)
	poetry install --no-root

run:
	$(call green_color,Running main script)
	poetry run python a_maze_ing.py config.txt

debug:
	$(call green_color,Running in debug mode)
	poetry run python -m pdb a_maze_ing.py config.txt

clean:
	$(call green_color,Cleaning temporary files)
	rm -rf __pycache__ .mypy_cache

lint:
	$(call green_color,Running flake8)
	poetry run flake8 .
	$(call green_color,Running mypy)
	poetry run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	
alo:
	$(call green_color,Running all checks)
	poetry run python -c "print('Hello, World!')"