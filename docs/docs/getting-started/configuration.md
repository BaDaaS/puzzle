---
sidebar_position: 2
---

# Configuration

Learn how to configure Puzzle for your specific needs, including exchange
integrations and system settings.

## Environment Configuration

Puzzle uses environment variables for configuration. All settings are defined in
your `.env` file (copied from `example.env` during installation).

### Database Settings

Configure your database connection:

```bash
# For development (SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# For production (PostgreSQL)
DATABASE_URL=postgresql://username:password@localhost:5432/puzzle
```

### Exchange API Configuration

Set up your cryptocurrency exchange API credentials:

```bash
# Kraken
CRYPTO_EXCHANGE_KRAKEN_API_KEY=your_kraken_api_key
CRYPTO_EXCHANGE_KRAKEN_SECRET_KEY=your_kraken_secret_key

# Add other exchanges as needed
```

### Infrastructure Services

Configure connection details for supporting services:

```bash
# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# InfluxDB
INFLUXDB_URL=http://localhost:8086
INFLUXDB_TOKEN=your_influxdb_token
INFLUXDB_ORG=your_organization
INFLUXDB_BUCKET=puzzle_data
```

### Logging Configuration

Set your preferred logging level:

```bash
LOGGING_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

## Exchange Setup

### Supported Exchanges

Puzzle currently supports the following exchanges:

- **Kraken**: Full integration with trading and balance fetching
- **Coinbase**: Basic integration (extensible)

### Adding Exchange API Keys

1. **Create API Keys**: Log into your exchange and create API keys with
   appropriate permissions:

   - **Read permissions**: For balance and trade history
   - **Trade permissions**: Only if you plan to execute trades through Puzzle

2. **Configure in Environment**: Add your API keys to the `.env` file:

   ```bash
   CRYPTO_EXCHANGE_KRAKEN_API_KEY=your_api_key_here
   CRYPTO_EXCHANGE_KRAKEN_SECRET_KEY=your_secret_key_here
   ```

3. **Populate Exchange Data**: Run the management command to populate exchange
   information:

   ```bash
   make populate-exchanges
   ```

### Testing Exchange Connections

Verify your exchange connections:

```bash
# Test balance fetching
make get-balance

# Test trade history
make get-trades

# Test price fetching
make get-price
```

## Currency Configuration

### Populate Supported Currencies

Puzzle supports both FIAT and cryptocurrency. Populate the currency database:

```bash
make populate-currencies
```

This command adds support for major currencies including:

- **FIAT**: USD, EUR, GBP, etc.
- **Cryptocurrencies**: BTC, ETH, USDT, etc.

### Custom Currency Mapping

Each exchange may use different symbol representations. Puzzle handles this
through currency mapping in each exchange's implementation. See
`trading/exchange_api/kraken.py` for examples.

## Security Configuration

### API Key Security

- **Never commit API keys**: Ensure `.env` is in your `.gitignore`
- **Use read-only keys**: When possible, create API keys with minimal
  permissions
- **Rotate regularly**: Update your API keys periodically

### Database Security

For production deployments:

- Use strong database passwords
- Enable SSL connections
- Restrict database access to necessary IPs only

## Advanced Configuration

### Custom Settings

Puzzle uses Django settings which can be customized in `puzzle/settings.py`.
Common customizations include:

- **Time zones**: Set your local timezone
- **Admin interface**: Customize the Django admin
- **CORS settings**: For API access from web frontends

### Performance Tuning

For production deployments:

- **Database connection pooling**: Configure appropriate pool sizes
- **Redis optimization**: Tune Redis memory usage
- **InfluxDB retention**: Set appropriate data retention policies

## Validation

After configuration, validate your setup:

```bash
# Run all checks
make check

# Test specific components
make test
```

## Next Steps

With Puzzle configured, you're ready to start using Puzzle for asset management.

## Configuration Reference

### Environment Variables

| Variable                            | Description                | Default    |
| ----------------------------------- | -------------------------- | ---------- |
| `DATABASE_URL`                      | Database connection string | SQLite     |
| `REDIS_HOST`                        | Redis hostname             | localhost  |
| `REDIS_PORT`                        | Redis port                 | 6379       |
| `LOGGING_LEVEL`                     | Application logging level  | INFO       |
| `CRYPTO_EXCHANGE_KRAKEN_API_KEY`    | Kraken API key             | (required) |
| `CRYPTO_EXCHANGE_KRAKEN_SECRET_KEY` | Kraken secret key          | (required) |
| `INFLUXDB_URL`                      | InfluxDB connection URL    | (required) |
| `INFLUXDB_TOKEN`                    | InfluxDB authentication    | (required) |

For a complete list, see `example.env` in the repository.
