# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Development Commands

**Setup:**

```bash
# Install Python version and dependencies
pyenv install 3.13
poetry install
cp -f example.env .env
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
```

**Infrastructure:**

```bash
# Start required services
./infrastructure/influxdb.sh
./infrastructure/redis.sh
```

**Development:**

```bash
# Run development server
make dev

# Run tests
make test

# Lint and format code
make lint
make format

# Check for trailing whitespaces
make check-trailing-whitespace

# Fix trailing whitespaces
make fix-trailing-whitespace

# Run all checks (lint + test + whitespace check)
make check

# Database migrations
make makemigrations
make migrate

# Management commands
make populate-currencies
make populate-exchanges
make get-trades
make get-balance
make get-price
```

## Architecture

Puzzle is a Django-based asset management application with the following core
components:

### Apps Structure

- **trading/**: Cryptocurrency and financial trading functionality
  - Exchange integrations via CCXT library (Kraken, Coinbase)
  - Trade model with double-entry accounting legs
  - Price fetching and ticker management
- **accounting/**: Double-entry accounting system
  - Entity and Account models for business/personal entities
  - Account types: Asset, Liabilities, Equity, Revenue, Expenses, Receivable,
    Payable
  - Account subtypes for different financial instruments
- **common/**: Shared utilities and models
  - Currency model (FIAT/Crypto)
  - Utility classes for Price, Volume, Quantity
  - InfluxDB and Redis integration helpers

### Data Storage

- **PostgreSQL**: Primary relational database for trades, accounts, entities
- **InfluxDB**: Time-series data for price history and market data
- **Redis**: Middleware for real-time communication between processes

### Key Models

- `Trade`: Financial transactions with automatic leg creation
- `Account`: Chart of accounts with entity and currency relationships
- `Entity`: Business entities (companies, individuals)
- `Currency`: FIAT and cryptocurrency definitions
- `Exchange`: Trading platform integrations

### Exchange API Pattern

All exchange integrations inherit from `AbstractAPI` in
`trading/exchange_api/base.py` and implement:

- `get_trades()`: Fetch historical trades
- `get_balance()`: Get account balances
- `get_tickers()`: Fetch current prices
- `get_fiat_deposits()`: Retrieve fiat deposit history

### Configuration

- Environment variables configured via `.env` file (copy from `example.env`)
- Database can be SQLite (development) or PostgreSQL (production)
- Exchange API keys configured per exchange in settings
- Logging level configurable via `LOGGING_LEVEL`

## Development Notes

- Uses Poetry for dependency management with Python 3.13
- Ruff for linting and formatting with 80 character line length
- Django admin interface available for data management
- Management commands in each app's `management/commands/` directory
- Double-entry accounting automatically creates legs when trades are saved
- Currency mapping handled per exchange in `CURRENCY_MAPPING` dictionaries
- CHANGELOG.md follows [Keep a Changelog](https://keepachangelog.com) format
- Semantic versioning used for releases
- **IMPORTANT**: Always run these commands after making changes:
  - `make fix-trailing-whitespace` - Fix trailing whitespaces
  - `make format-md` - Format markdown files to 80-character wrapping
  - Run both commands at the end of each task

### Changelog Management

```bash
# Check changelog format
make changelog-check

# Release a new version (moves unreleased entries to version)
make changelog-release VERSION=1.0.0
```

## Commit Guidelines

**NEVER** add Claude as a co-author in commit messages. Do not include:

- `Co-Authored-By: Claude <noreply@anthropic.com>`
- Any other co-author attribution for Claude

**NEVER** use emojis in commit messages.

**Always** wrap commit message titles at 80 characters and body text at 80
characters.

Always verify commit messages before committing and remove any co-author lines
referencing Claude.

## CI Testing

**IMPORTANT**: When making changes to GitHub Actions workflows, always test them
locally using `act` before committing:

```bash
# Test specific workflow
act -j lint-and-format
act -j test
act -j build

# List all available jobs
act --list

# Dry run to check syntax
act --dryrun
```

This ensures CI configurations work correctly before pushing changes.

## Dockerfile Guidelines

**IMPORTANT**: Always run `make lint-dockerfiles` after modifying any
Dockerfile:

```bash
# After editing infrastructure/Dockerfile or any other Dockerfile
make lint-dockerfiles

# Fix any hadolint warnings or errors before committing
```

This ensures Dockerfiles follow best practices and security guidelines.

## Shell Script Guidelines

**IMPORTANT**: Always run `make lint-bash` after modifying any shell script:

```bash
# After editing any .sh file
make lint-bash

# Fix any shellcheck warnings or errors before committing
```

This ensures shell scripts follow best practices and avoid common issues.

## Dependency Management

The project uses Dependabot for automated dependency updates:

- **Python dependencies**: Weekly updates on Monday at 09:00
- **GitHub Actions**: Weekly updates on Monday at 10:00
- **Docker base images**: Weekly updates on Monday at 11:00

Dependabot will create pull requests with dependency updates that need to be
reviewed and merged. The CI pipeline will automatically test all dependency
updates.
