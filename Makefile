check:
	flake8 .
	mypy .
	python -m pytest --cov=flake8_fine_pytest --cov-report=xml
	mdl README.md
	safety check -r requirements.txt
