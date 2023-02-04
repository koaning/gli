.PHONY: docs

install:
	python -m pip install --upgrade -r dev-requirements.txt

clean: 
	isort gli
	black gli
	rm -rf gli/**/__pycache__

check:
	interrogate --ignore-semiprivate --ignore-private --ignore-module -vv
	flake8 gli

docs:
	python gli/docstuff.py
	mkdocs serve
