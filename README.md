# Puzzle - Take control back of your assets in real-time. Crypto, stocks, real estates, T-bills, cash.

Managing assets of a business or as a sole-trader is cumbersome and requires to be meticulous.
Even though some platforms like [Finary](https://finary.com/en) do exist, these
platforms are centralized, and might not be respecting your privacy.

Puzzle is the software to manage all of your assets, in one-app, in real-time,
including your invoices and clients.

Features that Puzzle provides:
- (real-time and automated) invoicing system
- integration with Stripe
- financial market interface, crypto and FIAT
- basic double-entry accounting system
  - does not include VAT or tax system

The enterprise version is actively used by different successful companies in
different areas:
- BaDaaS - a cryptography laboratory based in Belgium
- LeakIX - a cybersecurity company providing an overview of business vulnerable
  assets on the Internet.

## Cypherpunk movement

At [BaDaaS](https://badaas.be), we do believe the cypherpunks must build free
and open source softwares that help people to keep their privacy.

Manifesto's:
- [PrivAcc - 2024](https://privacc.org/)

## Enterprise

If you want to reach out to us for an enterprise version or enterprise
features, send us an email 

## Technological stack

The software is built on different components:
- a relational database, PostgreSQL, to keep track of relational data, like the
  ledgers, the trades, etc. It aims to be long term data. Not necessarily
  time-based.
- a time series database. Also for long term data, but mostly to keep track of
  data evolving every seconds, at least. It might be stricter on time later.
- a middleware, Redis, to communicate in real time between processes and
  exchange information.
- a web interface, to visualize and interact with the
  PostgreSQL database.

## Where does the development of the software happen?

On this public repository, we do commit changes that have been tested in our
enterprise version for at least 2 months. The development of the enterprise
version is happening on a private repository, and we do backport changes from
time to time, when we know they are stable.

For now, the development happens on a private repository as the development is
not linear, and experimentation happens with breaking changes. In the near
future, when the public version will be stabilized, we will start releasing the
development of the private components.

## License

GPL 3.0

## Why Puzzle?

That's the puzzle!
Reference: [How I met your mother](https://how-i-met-your-mother.fandom.com/wiki/Puzzles)
