# Infrastructure

## Pre-requisites

On a new Debian/Ubuntu machine, the following commands should be enough to run the project:

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
pyenv install 3.13.0
```

You will need Redis and InfluxDB to keep data.

To start containers using docker, you can use:
```shell
./infrastructure/influxdb.sh
./infrastructure/redis.sh
```

Check the files to change the port and configuration to meet your needs.
