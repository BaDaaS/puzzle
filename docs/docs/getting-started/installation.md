---
sidebar_position: 1
---

# Installation

This guide will help you install and set up Puzzle on your development machine.

## Prerequisites

Before installing Puzzle, ensure you have the following tools installed:

### Python Environment

- **Python 3.13**: Use [pyenv](https://github.com/pyenv/pyenv/) to install the
  required Python version
- **Poetry**: For Python dependency management

### Infrastructure Services

You'll need the following services running:

- **Redis 8.0**: For real-time communication middleware
- **InfluxDB 2.7.10**: For time-series data storage
- **PostgreSQL** (optional): For production deployments

### System Dependencies

On Ubuntu/Debian systems, install the required build dependencies:

```bash
sudo apt install build-essential \
  libssl-dev \
  zlib1g-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev \
  curl \
  git \
  libpq-dev \
  libffi-dev \
  liblzma-dev
```

## Installation Steps

### 1. Install Python and Poetry

Install Python 3.13 using pyenv:

```bash
# Install pyenv
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
export PATH="$HOME/.pyenv/bin:$PATH"

# Install Python 3.13
pyenv install 3.13.5
pyenv global 3.13.5
```

Install Poetry:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Clone the Repository

```bash
git clone https://github.com/BaDaaS/puzzle.git
cd puzzle
```

### 3. Install Dependencies

```bash
# Install Python dependencies
poetry install

# Set up environment configuration
cp example.env .env
```

### 4. Database Setup

Run the database migrations:

```bash
poetry run python manage.py migrate
```

Create a superuser account:

```bash
poetry run python manage.py createsuperuser
```

### 5. Start Infrastructure Services

Start Redis and InfluxDB using the provided scripts:

```bash
./infrastructure/redis.sh
./infrastructure/influxdb.sh
```

Alternatively, use the Makefile:

```bash
make infrastructure
```

## Verification

Verify your installation by running the development server:

```bash
make dev
```

Visit http://localhost:8000 to see the Puzzle interface.

## Docker Installation

For a containerized setup, use Docker Compose:

```bash
# Start all services (Redis, InfluxDB, PostgreSQL, and Puzzle)
make docker-compose-up

# View logs
make docker-compose-logs

# Stop all services
make docker-compose-down
```

## Next Steps

Now that Puzzle is installed, proceed to:

1. **[Configuration](./configuration)**: Configure your exchanges and settings

## Troubleshooting

### Common Issues

**Poetry installation fails**:

- Ensure Python 3.13 is properly installed and active
- Try updating pip: `pip install --upgrade pip`

**Database connection errors**:

- Verify PostgreSQL is running (if using production setup)
- Check your `.env` file configuration

**Redis/InfluxDB connection issues**:

- Ensure Docker is running
- Check that ports 6379 (Redis) and 8086 (InfluxDB) are available

For more help, check our
[GitHub Issues](https://github.com/BaDaaS/puzzle/issues) or start a
[Discussion](https://github.com/BaDaaS/puzzle/discussions).
