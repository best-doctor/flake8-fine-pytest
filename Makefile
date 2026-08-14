.PHONY: install style types test coverage readme requirements check

install:
	uv sync --group dev
	uv run pre-commit install

style:
	uv run flake8 .

types:
	uv run mypy flake8_fine_pytest

test:
	uv run pytest

coverage:
	uv run pytest --cov --cov-report=xml --cov-report=term-missing

readme:
	uv run pre-commit run markdownlint-cli2 --all-files

requirements:
	uv run pip-audit --skip-editable

check: style types test requirements
