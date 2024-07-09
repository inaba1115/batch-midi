.PHONY: all lint test

all: lint test

lint:
	poetry run black .
	poetry run isort . --profile black
	poetry run flake8 .
	poetry run mypy .

test:
	poetry run python -m unittest
