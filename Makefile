# Makefile for LBO Model Generator

.PHONY: help install test clean format lint

help:
	@echo "LBO Model Generator - Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean generated files"
	@echo "  make format     - Format code (requires black)"
	@echo "  make lint       - Run linter (requires pylint)"

install:
	pip install -r requirements.txt

test:
	python -m pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf output/*.xlsx
	rm -rf *.egg-info
	rm -rf build/
	rm -rf dist/

format:
	black src/ tests/

lint:
	pylint src/ tests/

