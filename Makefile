.PHONY: check test build up down clean

check:
	@echo "Checking backend..."
	cd backend && ruff check . && ruff format --check . && mypy app/
	@echo "Checking frontend..."
	cd frontend && npm run lint && npm run typecheck

test:
	@echo "Testing backend..."
	cd backend && pytest tests/
	@echo "Testing frontend..."
	cd frontend && npm run test

build:
	@echo "Building docker images..."
	docker-compose -f infra/docker-compose.yml build

up:
	@echo "Starting services..."
	docker-compose -f infra/docker-compose.yml up -d

down:
	@echo "Stopping services..."
	docker-compose -f infra/docker-compose.yml down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf backend/dist backend/build backend/*.egg-info
	rm -rf frontend/dist frontend/node_modules
