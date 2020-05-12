check:
	flake8 .
	mypy flake8_fine_pytest
	python -m pytest --cov=flake8_fine_pytest --cov-report=xml
	mdl README.md
	safety check -r requirements.txt
