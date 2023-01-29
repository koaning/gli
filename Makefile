install:
	python -m pip install -r dev-requirements.txt

clean: 
	isort gli
	black gli
