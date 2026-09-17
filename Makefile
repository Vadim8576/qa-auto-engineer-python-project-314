install:
	uv sync

build:
	uv build

lint:
	uv run ruff check .

fix:
	uv run ruff check --fix

test:
	test:
	APP_BASE_URL=$(or $(APP_BASE_URL),http://localhost:5173) \
	SELENIUM_MANAGER_DISABLE=true \
	uv run python -m pytest
	
start-app:
	docker run --rm -p 5173:5173 hexletprojects/qa_auto_python_testing_kanban_board_project_ru_app