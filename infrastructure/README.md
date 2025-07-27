# Infrastructure

## Docker Setup

### Complete Stack with Docker Compose

The easiest way to run the complete Puzzle infrastructure:

```shell
# Start all services (Redis, InfluxDB, PostgreSQL, and Puzzle app)
make docker-compose-up

# View logs
make docker-compose-logs

# Stop all services
make docker-compose-down
```

### Individual Docker Build

To build just the Puzzle application Docker image:

```shell
# Build the Docker image
make docker-build

# Run with custom tag
DOCKER_TAG=dev make docker-build
```

## Manual Setup

### Pre-requisites

On a new Debian/Ubuntu machine, install system dependencies:

```shell
# Install pyenv + python + poetry
sudo apt install build-essential \
  libssl-dev \
  zlib1g-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev \
  curl \
  git \
  libncursesw5-dev \
  xz-utils \
  tk-dev \
  libxml2-dev \
  libxmlsec1-dev \
  libffi-dev \
  liblzma-dev
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
export PATH="$HOME/.pyenv/bin:$PATH"
pyenv install 3.13.5
```

### Individual Services

Start Redis and InfluxDB containers separately:

```shell
./infrastructure/influxdb.sh
./infrastructure/redis.sh
```

## Configuration

- **Redis**: Version 8.0, port 6379
- **InfluxDB**: Version 2.7.10, port 8086
- **PostgreSQL**: Version 16, port 5432 (docker-compose only)
- **Python**: Version 3.13.5

Check the respective files to modify ports and configuration.
