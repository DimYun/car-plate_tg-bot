install:
	pip install -r requirements.txt

run_app:
	PYTHONPATH=. python main.py

lint:
	PYTHONPATH=. tox .
	PYTHONPATH=. isort .