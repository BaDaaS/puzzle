# For developers

## Pre-requisites

- Use [pyenv](https://github.com/pyenv/pyenv/) to install the require Python version.
- [Poetry](https://python-poetry.org/docs/) to manage Python dependencies.

## Setup

```
pyenv install 3.13
poetry install
cp -f example.env .env
# Create a superuser
poetry run python manage.py createsuperuser
```


## Infrastructure

You will need Redis and InfluxDB to keep data.

To start containers using docker, you can use:
```shell
./infrastructure/influxdb.sh
./infrastructure/redis.sh
```

Check the files to change the port and configuration to meet your needs.
