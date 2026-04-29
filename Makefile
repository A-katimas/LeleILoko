PYTHON		= uv run python3
UV			= uv
VENV		= .venv
SRC			= Flyin.py

TMP_DIRS	= __pycache__ .mypy_cache .ruff_cache
#CONFIG		?= maps/easy/01_linear_path.txt
CONFIG		?= maps/medium/02_circular_loop.txt


install:
	@echo ">>> Installation de uv..."
	curl -LsSf https://astral.sh/uv/install.sh | sh
	@echo ">>> Sync des dépendances (prod + dev)..."
	$(UV) sync --dev
	@echo ">>> OK — projet prêt !"


run:
	@echo ">>> Lancement de la simulation..."
	$(UV) run $(SRC) $(CONFIG)


debug:
	@uv run python -m pdb $(SRC)

lint:
	@echo ">>> flake8..."
	$(UV) run flake8 .
	@echo ">>> mypy..."
	$(UV) run mypy .
	@echo ">>> Lint OK !"

lint-strict:
	@echo ">>> flake8 (strict)..."
	$(UV) run flake8 --max-line-length=79 .
	@echo ">>> mypy --strict..."
	$(UV) run mypy mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .
	@echo ">>> Lint strict OK !"

clean:
	@echo ">>> Suppression des fichiers temporaires..."
	rm -rf $(TMP_DIRS)
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "__pycache__" -delete
	@echo ">>> Clean OK !"

fclean: clean
	@echo ">>> Suppression du venv..."
	rm -rf $(VENV)
	@echo ">>> FClean OK !"

.PHONY: run install debug clean fclean lint lint-strict