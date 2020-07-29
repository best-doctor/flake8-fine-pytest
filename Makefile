style:
	flake8 .
	mdl README.md

security:
	safety check -r requirements.txt

test:
	python -m pytest --cov=flake8_fine_pytest --cov-report=xml

types:
	mypy flake8_fine_pytest

check:
	make style
	make test
	make types
	make security
