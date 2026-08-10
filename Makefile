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

start:
	docker run --rm -p 5173:5173 hexletprojects/qa_auto_python_testing_kanban_board_project_ru_app