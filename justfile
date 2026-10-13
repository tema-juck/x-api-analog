@a_default:
    just --list

@dev:
    uv run fastapi dev app/main.py

@check:
    uv run ruff check
    uv run ruff format --check

@lint:
    uv run ruff check --fix

@format:
    uv run ruff format