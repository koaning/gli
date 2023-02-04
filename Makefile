install:
	python -m pip install --upgrade -r dev-requirements.txt

clean: 
	isort gli
	black gli
	rm -rf gli/**/__pycache__
