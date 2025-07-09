.PHONY: help install test test-models test-routes test-coverage clean build run dev stop logs init-db reset-db lint format check docker-build docker-run docker-dev docker-stop docker-clean

# Docker-based commands
install:
	@echo "📦 Building Docker image with dependencies..."
	docker-compose -f docker/docker-compose.yml build

# Database commands
init-db:
	@echo "🗄️ Initializing database with sample data..."
	docker-compose -f docker/docker-compose.yml run --rm blog-api-dev python src/utils/init_db.py

reset-db:
	@echo "⚠️ Resetting database..."
	docker-compose -f docker/docker-compose.yml run --rm blog-api-dev python src/utils/init_db.py --reset
	docker-compose -f docker/docker-compose.yml run --rm blog-api-dev python src/utils/init_db.py

# Development commands
run:
	@echo "🚀 Starting API server in Docker..."
	docker-compose -f docker/docker-compose.yml up --build

dev:
	@echo "🔧 Starting API server in Docker development mode..."
	docker-compose -f docker/docker-compose.yml --profile dev up --build

# Testing commands
test:
	@echo "🧪 Running all unit tests in Docker..."
	docker-compose -f docker/docker-compose.yml run --rm blog-api-dev python -m unittest discover tests/ -v

# Code quality commands (Docker-based)
lint:
	@echo "🔍 Running linting in Docker..."
	docker-compose -f docker/docker-compose.yml run --rm blog-api-dev python -m flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics
	docker-compose -f docker/docker-compose.yml run --rm blog-api-dev python -m flake8 src --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	@echo "✨ Formatting code in Docker..."
	docker-compose -f docker/docker-compose.yml run --rm blog-api-dev python -m black src tests --line-length 100
	docker-compose -f docker/docker-compose.yml run --rm blog-api-dev python -m isort src tests --profile black

check: lint
	@echo "✅ Running all code quality checks in Docker..."
	docker-compose -f docker/docker-compose.yml run --rm blog-api-dev python -m py_compile src/main.py
	@echo "All checks passed!"

# Local testing (without Docker)
test-local:
	@echo "🧪 Running all unit tests locally..."
	python -m unittest discover tests/ -v

# Docker commands
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -f docker/Dockerfile -t blog-api .

docker-run:
	@echo "🐳 Running API in Docker..."
	docker-compose -f docker/docker-compose.yml up --build

docker-dev:
	@echo "🐳 Running API in Docker development mode..."
	docker-compose -f docker/docker-compose.yml --profile dev up --build

docker-stop:
	@echo "🛑 Stopping Docker containers..."
	docker-compose -f docker/docker-compose.yml down

docker-clean:
	@echo "🧹 Cleaning up Docker..."
	docker-compose -f docker/docker-compose.yml down --volumes --remove-orphans
	docker system prune -f

# Utility commands
logs:
	@echo "📋 Showing Docker logs..."
	docker-compose -f docker/docker-compose.yml logs -f

clean:
	@echo "🧹 Cleaning up temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	rm -f data/blog.db

# Docker utility commands
shell:
	@echo "🐚 Opening shell in Docker container..."
	docker-compose -f docker/docker-compose.yml run --rm blog-api-dev /bin/bash

exec:
	@echo "🔧 Executing command in running container..."
	docker-compose -f docker/docker-compose.yml exec blog-api-dev /bin/bash

# Quick development workflow
quick-start: clean install init-db test dev
	@echo "🎉 Quick start completed! API should be running on http://localhost:8001"

# Production deployment preparation
prod-check: clean install test lint
	@echo "✅ Production checks completed!"

# Development setup for new contributors
setup: install init-db
	@echo "🎯 Development environment setup completed!"
	@echo "Run 'make dev' to start the development server"
	@echo "Run 'make test' to run tests"
	@echo "Run 'make help' to see all available commands"

