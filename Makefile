.PHONY: help install setup migrate test lint format check clean dev infrastructure
.DEFAULT_GOAL := help

# Variables
PYTHON_VERSION := 3.13
POETRY := poetry run
DOCKER_REGISTRY := ghcr.io/badaas
DOCKER_IMAGE_NAME := puzzle
DOCKER_TAG := latest

help: ## Ask for help!
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install Python version and dependencies
	pyenv install $(PYTHON_VERSION) --skip-existing
	poetry install

setup: install ## Complete setup including dependencies and database
	cp -f example.env .env
	$(POETRY) python manage.py migrate
	@echo "Setup complete! Run 'make createsuperuser' to create an admin user."

createsuperuser: ## Create Django superuser
	$(POETRY) python manage.py createsuperuser

migrate: ## Run database migrations
	$(POETRY) python manage.py migrate

makemigrations: ## Create new database migrations
	$(POETRY) python manage.py makemigrations

test: ## Run tests
	$(POETRY) pytest

lint: ## Check code with ruff
	$(POETRY) ruff check

format: ## Format code with ruff
	$(POETRY) ruff format

format-check: ## Check if code is properly formatted
	$(POETRY) ruff format --check

check: lint test check-trailing-whitespace lint-dockerfiles lint-bash check-md changelog-check ## Run all checks (lint + test + whitespace + dockerfile + bash + markdown + changelog)

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

fix-trailing-whitespace: ## Remove trailing whitespaces from all files
	@echo "Removing trailing whitespaces from all files..."
	@find . -type f \
		\( \
		-name "*.py" -o -name "*.toml" -o -name "*.md" -o -name "*.yaml" \
		-o -name "*.yml" -o -name "*.json" -o -name "*.sh" -o -name "*.env" \
		-o -name "*.txt" -o -name "*.cfg" -o -name "*.ini" \
		\) \
		-not -path "./.venv/*" \
		-not -path "./venv/*" \
		-not -path "./.git/*" \
		-not -path "./db.sqlite3" \
		-not -path "./__pycache__/*" \
		-not -path "./*/migrations/*" \
		-exec sed -i'' -e "s/[[:space:]]*$$//" {} + && \
		echo "Trailing whitespaces removed."

check-trailing-whitespace: ## Check for trailing whitespaces in source files
	@echo "Checking for trailing whitespaces..."
	@files_with_trailing_ws=$$(find . -type f \( \
		-name "*.py" -o -name "*.toml" -o -name "*.md" -o -name "*.yaml" \
		-o -name "*.yml" -o -name "*.json" -o -name "*.sh" -o -name "*.env" \
		-o -name "*.txt" -o -name "*.cfg" -o -name "*.ini" \
		\) \
		-not -path "./.venv/*" \
		-not -path "./venv/*" \
		-not -path "./.git/*" \
		-not -path "./db.sqlite3" \
		-not -path "./__pycache__/*" \
		-not -path "./*/migrations/*" \
		-exec grep -l "[[:space:]]$$" {} + 2>/dev/null || true); \
	if [ -n "$$files_with_trailing_ws" ]; then \
		echo "Files with trailing whitespaces found:"; \
		echo "$$files_with_trailing_ws"; \
		echo "Run 'make fix-trailing-whitespace' to fix them."; \
		exit 1; \
	else \
		echo "No trailing whitespaces found."; \
	fi

lint-dockerfiles: ## Check all Dockerfiles using hadolint
	@if [ "$$GITHUB_ACTIONS" = "true" ]; then \
		OUTPUT=$$(find . -name "Dockerfile*" -type f -exec hadolint {} \;); \
		if [ -n "$$OUTPUT" ]; then \
			echo "$$OUTPUT"; \
			exit 1; \
		fi; \
	else \
		OUTPUT=$$(find . -name "Dockerfile*" -type f -exec sh -c 'docker run --rm -i hadolint/hadolint < "$$1"' _ {} \;); \
		if [ -n "$$OUTPUT" ]; then \
			echo "$$OUTPUT"; \
			exit 1; \
		fi; \
	fi

lint-bash: ## Check all shell scripts using shellcheck
	@echo "Running shellcheck on shell scripts..."
	@find . -name "*.sh" \
		-not -path "./.venv/*" \
		-not -path "./venv/*" \
		-not -path "./.git/*" \
		-not -path "./node_modules/*" \
		-print0 | xargs -0 shellcheck
	@echo "Shellcheck completed successfully!"

check-md: ## Check if markdown files are properly formatted
	@echo "Checking markdown formatting..."
	npx prettier --check "**/*.md"
	@echo "Markdown format check completed."

format-md: ## Format all markdown files to wrap at 80 characters
	@echo "Formatting markdown files..."
	npx prettier --write "**/*.md"
	@echo "Markdown files have been formatted to 80 characters."

changelog-check: ## Check if CHANGELOG.md has unreleased entries
	@if ! grep -q "## \[Unreleased\]" CHANGELOG.md; then \
		echo "Error: CHANGELOG.md missing [Unreleased] section"; \
		exit 1; \
	fi
	@echo "CHANGELOG.md format is valid."

changelog-release: ## Move unreleased entries to new version (requires VERSION)
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION is required. Usage: make changelog-release VERSION=1.0.0"; \
		exit 1; \
	fi
	@sed -i 's/## \[Unreleased\]/## [Unreleased]\n\n### Added\n\n### Changed\n\n### Fixed\n\n## [$(VERSION)] - $(shell date +%Y-%m-%d)/' CHANGELOG.md
	@echo "Released version $(VERSION) in CHANGELOG.md"

dev: ## Start development server
	$(POETRY) python manage.py runserver

infrastructure: ## Start infrastructure services (Redis and InfluxDB)
	./infrastructure/redis.sh &
	./infrastructure/influxdb.sh &
	@echo "Infrastructure services started in background"

# Management commands
populate-currencies: ## Populate database with currencies
	$(POETRY) python manage.py populate_with_currencies

populate-exchanges: ## Populate database with exchanges
	$(POETRY) python manage.py populate_with_exchanges

get-trades: ## Fetch trades from exchanges
	$(POETRY) python manage.py get_trades

get-balance: ## Get exchange balances
	$(POETRY) python manage.py get_exchange_balance

get-price: ## Get current prices
	$(POETRY) python manage.py get_price

# Docker targets
docker-build: ## Build Docker image
	docker build -t $(DOCKER_REGISTRY)/$(DOCKER_IMAGE_NAME):$(DOCKER_TAG) \
		-f infrastructure/Dockerfile .

docker-push: ## Push Docker image to registry
	docker push $(DOCKER_REGISTRY)/$(DOCKER_IMAGE_NAME):$(DOCKER_TAG)

docker-login: ## Login to GitHub Container Registry
	echo $(GITHUB_TOKEN) | docker login ghcr.io -u $(GITHUB_ACTOR) --password-stdin

docker-compose-up: ## Start all services with docker-compose
	cd infrastructure && docker-compose up -d

docker-compose-down: ## Stop all services with docker-compose
	cd infrastructure && docker-compose down

docker-compose-logs: ## Show logs from docker-compose services
	cd infrastructure && docker-compose logs -f

