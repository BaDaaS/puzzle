.DEFAULT_GOAL := help

# Variables
PYTHON_VERSION := 3.13
POETRY := poetry run
DOCKER_REGISTRY := ghcr.io/badaas
DOCKER_IMAGE_NAME := puzzle
DOCKER_TAG := latest

# Help and setup targets
.PHONY: help
help: ## Ask for help!
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install Python version and dependencies
	pyenv install $(PYTHON_VERSION) --skip-existing
	poetry install

.PHONY: setup
setup: install ## Complete setup including dependencies and database
	cp -f example.env .env
	$(POETRY) python manage.py migrate
	@echo "Setup complete! Run 'make createsuperuser' to create an admin user."

.PHONY: createsuperuser
createsuperuser: ## Create Django superuser
	$(POETRY) python manage.py createsuperuser

.PHONY: migrate
migrate: ## Run database migrations
	$(POETRY) python manage.py migrate

.PHONY: makemigrations
makemigrations: ## Create new database migrations
	$(POETRY) python manage.py makemigrations

.PHONY: test
test: ## Run tests
	$(POETRY) pytest

.PHONY: lint
lint: ## Check code with ruff
	$(POETRY) ruff check

.PHONY: format
format: ## Format code with ruff
	$(POETRY) ruff format

.PHONY: format-check
format-check: ## Check if code is properly formatted
	$(POETRY) ruff format --check

.PHONY: check
check: lint test check-trailing-whitespace lint-dockerfiles lint-bash check-md changelog-check ## Run all checks (lint + test + whitespace + dockerfile + bash + markdown + changelog)

.PHONY: clean
clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

.PHONY: fix-trailing-whitespace
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

.PHONY: check-trailing-whitespace
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

.PHONY: lint-dockerfiles
lint-dockerfiles: ## Check all Dockerfiles using hadolint
	@if [ "$$GITHUB_ACTIONS" = "true" ]; then \
		OUTPUT=$$(find . -name "Dockerfile*" -type f -exec hadolint --ignore DL3008 {} \;); \
		if [ -n "$$OUTPUT" ]; then \
			echo "$$OUTPUT"; \
			exit 1; \
		fi; \
	else \
		OUTPUT=$$(find . -name "Dockerfile*" -type f -exec sh -c 'docker run --rm -i hadolint/hadolint hadolint --ignore DL3008 - < "$$1"' _ {} \;); \
		if [ -n "$$OUTPUT" ]; then \
			echo "$$OUTPUT"; \
			exit 1; \
		fi; \
	fi

.PHONY: lint-bash
lint-bash: ## Check all shell scripts using shellcheck
	@echo "Running shellcheck on shell scripts..."
	@find . -name "*.sh" \
		-not -path "./.venv/*" \
		-not -path "./venv/*" \
		-not -path "./.git/*" \
		-not -path "./node_modules/*" \
		-print0 | xargs -0 shellcheck
	@echo "Shellcheck completed successfully!"

.PHONY: check-md
check-md: ## Check if markdown files are properly formatted
	@echo "Checking markdown formatting..."
	npx prettier --check "**/*.md"
	@echo "Markdown format check completed."

.PHONY: format-md
format-md: ## Format all markdown files to wrap at 80 characters
	@echo "Formatting markdown files..."
	npx prettier --write "**/*.md"
	@echo "Markdown files have been formatted to 80 characters."

.PHONY: changelog-check
changelog-check: ## Check if CHANGELOG.md has unreleased entries
	@if ! grep -q "## \[Unreleased\]" CHANGELOG.md; then \
		echo "Error: CHANGELOG.md missing [Unreleased] section"; \
		exit 1; \
	fi
	@echo "CHANGELOG.md format is valid."

.PHONY: changelog-release
changelog-release: ## Move unreleased entries to new version (requires VERSION)
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION is required. Usage: make changelog-release VERSION=1.0.0"; \
		exit 1; \
	fi
	@sed -i 's/## \[Unreleased\]/## [Unreleased]\n\n### Added\n\n### Changed\n\n### Fixed\n\n## [$(VERSION)] - $(shell date +%Y-%m-%d)/' CHANGELOG.md
	@echo "Released version $(VERSION) in CHANGELOG.md"

.PHONY: dev
dev: ## Start development server
	$(POETRY) python manage.py runserver

.PHONY: infrastructure
infrastructure: ## Start infrastructure services (Redis and InfluxDB)
	./infrastructure/redis.sh &
	./infrastructure/influxdb.sh &
	@echo "Infrastructure services started in background"

# Management commands
.PHONY: populate-currencies
populate-currencies: ## Populate database with currencies
	$(POETRY) python manage.py populate_with_currencies

.PHONY: populate-exchanges
populate-exchanges: ## Populate database with exchanges
	$(POETRY) python manage.py populate_with_exchanges

.PHONY: get-trades
get-trades: ## Fetch trades from exchanges
	$(POETRY) python manage.py get_trades

.PHONY: get-balance
get-balance: ## Get exchange balances
	$(POETRY) python manage.py get_exchange_balance

.PHONY: get-price
get-price: ## Get current prices
	$(POETRY) python manage.py get_price

# Docker targets
.PHONY: docker-build
docker-build: ## Build Docker image
	docker build -t $(DOCKER_REGISTRY)/$(DOCKER_IMAGE_NAME):$(DOCKER_TAG) \
		-f infrastructure/Dockerfile .

.PHONY: docker-push
docker-push: ## Push Docker image to registry
	docker push $(DOCKER_REGISTRY)/$(DOCKER_IMAGE_NAME):$(DOCKER_TAG)

.PHONY: docker-login
docker-login: ## Login to GitHub Container Registry
	echo $(GITHUB_TOKEN) | docker login ghcr.io -u $(GITHUB_ACTOR) --password-stdin

.PHONY: docker-compose-up
docker-compose-up: ## Start all services with docker-compose
	cd infrastructure && docker-compose up -d

.PHONY: docker-compose-down
docker-compose-down: ## Stop all services with docker-compose
	cd infrastructure && docker-compose down

.PHONY: docker-compose-logs
docker-compose-logs: ## Show logs from docker-compose services
	cd infrastructure && docker-compose logs -f

# Website targets
.PHONY: website-install
website-install: ## Install website dependencies
	cd docs && if [ -f package-lock.json ]; then npm ci; else npm install; fi

.PHONY: website-dev
website-dev: ## Start website development server
	cd docs && npm run start

.PHONY: website-build
website-build: ## Build website for production
	cd docs && npm run build

.PHONY: website-serve
website-serve: ## Serve built website locally
	cd docs && npm run serve

.PHONY: website-clear
website-clear: ## Clear website build cache
	cd docs && npm run clear

.PHONY: website-check
website-check: ## Check website for broken links and issues
	cd docs && npm run typecheck

.PHONY: website-deploy
website-deploy: website-build ## Build and prepare website for deployment
	@echo "Website built successfully in docs/build/"
	@echo "Ready for GitHub Pages deployment"

# Legacy documentation aliases (for backward compatibility)
.PHONY: docs-install
docs-install: website-install ## Alias for website-install
.PHONY: docs-dev
docs-dev: website-dev ## Alias for website-dev  
.PHONY: docs-build
docs-build: website-build ## Alias for website-build
.PHONY: docs-serve
docs-serve: website-serve ## Alias for website-serve
.PHONY: docs-clear
docs-clear: website-clear ## Alias for website-clear

