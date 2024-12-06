build:
	./build.sh


install:
	poetry install


dev:
	poetry run flask --app page_analyzer:app run


PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app


dev-install:
	poetry install --with dev


test-coverage: dev-install
	poetry run pytest --cov=page_analyzer --cov-report xml


test: dev-install
	poetry run pytest


lint: dev-install
	poetry run flake8 .
