# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Comprehensive Makefile with development, testing, and CI/CD targets
- Docker infrastructure setup with multi-stage Dockerfile
- Docker Compose configuration for complete development stack
- GitHub Container Registry integration with automated image builds
- Hadolint integration for Dockerfile linting
- Trailing whitespace detection and fixing
- Markdown formatting with Prettier (80-character line wrapping)
- Split CI workflows: lint → test → build pipeline
- CLAUDE.md documentation for AI assistant guidance
- Infrastructure documentation and setup scripts

### Changed

- Updated Python version to 3.13.5 (latest stable)
- Updated Redis version to 8.0 (latest stable)
- CI workflows now use same Makefile targets as local development
- Improved help system in Makefile following openmina pattern

### Infrastructure

- **Redis**: Version 8.0, port 6379
- **InfluxDB**: Version 2.7.10, port 8086
- **PostgreSQL**: Version 16, port 5432 (docker-compose)
- **Python**: Version 3.13.5

### Development Tools

- Poetry for dependency management
- Ruff for linting and formatting
- Pytest for testing
- Hadolint for Dockerfile linting
- Prettier for markdown formatting
- Docker for containerization

## [0.1.0] - 2025-01-XX

### Added

- Django-based asset management application
- Trading module with cryptocurrency exchange integrations (Kraken, Coinbase)
- Double-entry accounting system
- Support for multiple currencies (FIAT and cryptocurrency)
- InfluxDB integration for time-series data
- Redis middleware for real-time communication
- Management commands for data population and price fetching
- Basic web interface for data visualization

### Core Features

- Real-time and automated invoicing system
- Stripe integration for payments
- Financial market interface for crypto and FIAT
- Basic double-entry accounting (no VAT/tax system)
- Multi-exchange trading support via CCXT library

### Architecture

- **Apps**: trading, accounting, common
- **Database**: PostgreSQL (primary), InfluxDB (time-series), Redis (cache)
- **Exchange APIs**: Abstract base class for consistent integrations
- **Models**: Trade, Account, Entity, Currency, Exchange with relationships
