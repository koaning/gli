install:
	python -m pip install --upgrade -r dev-requirements.txt
	python -m pip install -e . 

clean: 
	isort gli
	black gli
	rm -rf gli/**/__pycache__
