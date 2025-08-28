.PHONY: default fmt-check fmt lint lint-fix type-check

default: fmt-check lint type-check

fmt-check:
	uvx ruff format . --check --diff

fmt:
	uvx ruff format .

lint:
	uvx ruff check .

lint-fix:
	uvx ruff check . --fix

type-check:
	uv run pyright
