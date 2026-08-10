run:
	uv run my-app

install:
	uv sync

build:
	uv build

lint:
	uv run ruff check .

fix:
	uv run ruff check --fix

test:
	uv run pytest