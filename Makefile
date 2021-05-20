style:
	flake8 .

test:
	python -m pytest

coverage:
	python -m pytest --cov=flake8_fine_pytest --cov-report=xml

readme:
	mdl README.md

types:
	mypy flake8_fine_pytest

requirements:
	safety check -r requirements_dev.txt

check:
	make style
	make types
	make test
	make requirements
