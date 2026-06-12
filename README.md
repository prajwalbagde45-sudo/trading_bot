# Binance Futures Testnet Trading Bot 🤖

A production-quality Python CLI application for placing **MARKET**, **LIMIT**,
and **STOP-LIMIT** orders on the **Binance USDT-M Futures Testnet**.

Built with clean architecture, modular design, full input validation,
structured logging, and robust error handling.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Folder Structure](#2-folder-structure)
3. [Installation Steps](#3-installation-steps)
4. [Testnet Account Setup](#4-testnet-account-setup)
5. [API Key Generation](#5-api-key-generation)
6. [Configuration](#6-configuration)
7. [Running the Bot](#7-running-the-bot)
8. [CLI Reference](#8-cli-reference)
9. [Usage Examples](#9-usage-examples)
10. [Sample Output](#10-sample-output)
11. [Logging](#11-logging)
12. [Assumptions](#12-assumptions)
13. [Bonus Feature — STOP-LIMIT Orders](#13-bonus-feature--stop-limit-orders)

---

## 1. Project Overview

This bot connects to the [Binance Futures Testnet](https://testnet.binancefuture.com)
and exposes a simple CLI to place orders programmatically — ideal for learning,
strategy testing, or as a skeleton for a production trading system.

### Key capabilities

| Feature | Details |
|---|---|
| Order types | MARKET, LIMIT, STOP-LIMIT (bonus) |
| Order sides | BUY, SELL |
| Input validation | All parameters validated before any API call |
| Structured logging | Rotating log file + console warnings |
| Error handling | Binance ClientError, ServerError, network errors |
| Clean architecture | Single-responsibility modules, type hints, docstrings |

---

## 2. Folder Structure

```
trading_bot/
│
├── bot/
│   ├── __init__.py          # Package metadata
│   ├── client.py            # Binance Testnet client factory
│   ├── orders.py            # place_market_order / place_limit_order / place_stop_limit_order
│   ├── validators.py        # Input validation helpers
│   ├── logging_config.py    # Rotating file + console logging setup
│   └── cli.py               # argparse CLI, output formatting, orchestration
│
├── logs/
│   ├── .gitkeep             # Keeps the directory in git
│   └── trading.log          # Created automatically at runtime
│
├── .env.example             # Credential template — copy to .env
├── .env                     # Your real credentials (gitignored)
├── .gitignore
├── requirements.txt
├── README.md
└── main.py                  # Entry point
```

---

## 3. Installation Steps

### Prerequisites

- Python **3.11** or newer
- `pip` (comes with Python)
- A Binance Testnet account (see §4)

### Steps

```bash
# 1 — Clone or download the project
git clone <your-repo-url>
cd trading_bot

# 2 — Create and activate a virtual environment (recommended)
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

# 3 — Install dependencies
pip install -r requirements.txt

# 4 — Set up credentials
copy .env.example .env        # Windows
# cp .env.example .env        # macOS / Linux

# Open .env in your editor and fill in the API key and secret
```

---

## 4. Testnet Account Setup

1. Visit **[https://testnet.binancefuture.com](https://testnet.binancefuture.com)**
2. Click **"Sign Up"** (or log in with GitHub OAuth — the easiest option)
3. After signing in, you will land on the Futures Testnet trading interface
4. The testnet automatically credits your account with **test USDT** for trading
5. To get more test funds, click **"Asset"** → **"Get"** on the testnet portal

> **Important:** The Futures Testnet is completely separate from your real
> Binance account. Credentials created here only work on the testnet.

---

## 5. API Key Generation

1. Once logged in to [https://testnet.binancefuture.com](https://testnet.binancefuture.com),
   navigate to the **API key** section (usually top-right menu → "API Management")
2. Click **"Generate Key"**
3. Copy the **API Key** and **Secret Key** — the secret is shown only once
4. Open your `.env` file and paste the values:

```dotenv
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

---

## 6. Configuration

The bot reads credentials from a `.env` file in the project root.

| Variable | Required | Description |
|---|---|---|
| `BINANCE_API_KEY` | ✅ Yes | Your Testnet API key |
| `BINANCE_API_SECRET` | ✅ Yes | Your Testnet API secret |

All other settings (log level, max file size, backup count) are constants
in [`bot/logging_config.py`](bot/logging_config.py).

---

## 7. Running the Bot

```bash
# From the trading_bot/ directory with your virtual environment active
python main.py [OPTIONS]
```

Use `--help` to see all options:

```bash
python main.py --help
```

---

## 8. CLI Reference

| Argument | Type | Required | Description |
|---|---|---|---|
| `--symbol` | `str` | ✅ | Trading pair e.g. `BTCUSDT`, `ETHUSDT` |
| `--side` | `BUY\|SELL` | ✅ | Order direction |
| `--type` | `MARKET\|LIMIT\|STOP` | ✅ | Order type |
| `--quantity` | `float` | ✅ | Contract quantity e.g. `0.001` |
| `--price` | `float` | For LIMIT/STOP | Limit price |
| `--stop_price` | `float` | For STOP only | Stop trigger price |
| `--tif` | `GTC\|IOC\|FOK` | No | Time-in-force (default: `GTC`) |
| `--version` | — | No | Print version and exit |

---

## 9. Usage Examples

### Example 1 — MARKET BUY Order

```bash
python main.py \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.001
```

### Example 2 — LIMIT SELL Order

```bash
python main.py \
  --symbol BTCUSDT \
  --side SELL \
  --type LIMIT \
  --quantity 0.002 \
  --price 50000
```

### Example 3 — LIMIT BUY with IOC (Immediate Or Cancel)

```bash
python main.py \
  --symbol ETHUSDT \
  --side BUY \
  --type LIMIT \
  --quantity 0.01 \
  --price 2800 \
  --tif IOC
```

### Example 4 — STOP-LIMIT BUY (Bonus Feature)

```bash
python main.py \
  --symbol BTCUSDT \
  --side BUY \
  --type STOP \
  --quantity 0.001 \
  --price 49000 \
  --stop_price 49500
```

---

## 10. Sample Output

### MARKET BUY

```
============================================================
          ORDER REQUEST SUMMARY
============================================================
  Symbol        : BTCUSDT
  Side          : BUY
  Order Type    : MARKET
  Quantity      : 0.001
============================================================

============================================================
          ORDER RESPONSE DETAILS
============================================================
  Order ID      : 4291748302
  Client OID    : web_5Xk2mQpR9vNt3hFj
  Symbol        : BTCUSDT
  Side          : BUY
  Type          : MARKET
  Status        : FILLED
  Orig Qty      : 0.001
  Executed Qty  : 0.001
  Avg Price     : 67423.10
  Time-in-Force : GTC
  Update Time   : 1749543262412
============================================================

  ✅  MARKET order placed SUCCESSFULLY!
```

### LIMIT SELL

```
============================================================
          ORDER REQUEST SUMMARY
============================================================
  Symbol        : BTCUSDT
  Side          : SELL
  Order Type    : LIMIT
  Quantity      : 0.002
  Price         : 70000.0
  Time-in-Force : GTC
============================================================

============================================================
          ORDER RESPONSE DETAILS
============================================================
  Order ID      : 4291748567
  Client OID    : web_9Lm7nRqS2wBx4cGk
  Symbol        : BTCUSDT
  Side          : SELL
  Type          : LIMIT
  Status        : NEW
  Orig Qty      : 0.002
  Executed Qty  : 0.000
  Avg Price     : 70000.00
  Time-in-Force : GTC
  Update Time   : 1749543425339
============================================================

  ✅  LIMIT order placed SUCCESSFULLY!
```

---

## 11. Logging

All activity is recorded in **`logs/trading.log`** using a rotating file handler:

- **Max file size:** 5 MB per file
- **Backup count:** 3 (i.e., `trading.log`, `trading.log.1`, `trading.log.2`, `trading.log.3`)
- **Encoding:** UTF-8

**Log format:**
```
2025-01-15 10:23:45,123 | INFO     | bot.orders    | REQUEST  [MARKET_ORDER] params={...}
2025-01-15 10:23:45,387 | INFO     | bot.orders    | RESPONSE [MARKET_ORDER] data={...}
```

Every log entry contains:

| Field | Content |
|---|---|
| Timestamp | `YYYY-MM-DD HH:MM:SS,ms` |
| Level | `DEBUG / INFO / WARNING / ERROR` |
| Module | e.g. `bot.orders`, `bot.validators` |
| Message | Human-readable description + structured data |

A full example session is provided in [`logs/trading.log.sample`](logs/trading.log.sample).

---

## 12. Assumptions

1. **Testnet only** — The base URL is hard-coded to `https://testnet.binancefuture.com`.
   Do **not** use live API keys with this bot as-is.

2. **USDT-M Futures** — Only USD-margined perpetual contracts are supported
   (`UMFutures`). Coin-margined (`CMFutures`) pairs are not tested.

3. **Quantity precision** — The bot sends the quantity exactly as provided by
   the user. Binance may reject orders that don't respect the symbol's
   `stepSize` filter. Consult the exchange info endpoint for exact precision.

4. **No position management** — The bot places new orders only. It does not
   query open positions, cancel orders, or manage leverage/margin mode.

5. **Single order per invocation** — Each `python main.py` call places exactly
   one order. Batch or scheduled execution is out of scope.

6. **Default leverage** — Leverage is whatever the testnet account is currently
   set to (default: 20×). The bot does not change leverage automatically.

7. **Python 3.11+** — Uses `X | Y` union type hints (PEP 604) which require
   Python 3.10 or newer.

---

## 13. Bonus Feature — STOP-LIMIT Orders

A **STOP-LIMIT** order becomes a live limit order once the market reaches the
`stop_price`.

```
Example: BUY STOP-LIMIT
  stop_price = 49,500   ← triggers when market drops to this price
  price      = 49,000   ← the actual limit order placed when triggered
  quantity   = 0.001 BTC
```

```bash
python main.py \
  --symbol BTCUSDT \
  --side BUY \
  --type STOP \
  --quantity 0.001 \
  --price 49000 \
  --stop_price 49500
```

The Binance type value sent to the API is `STOP` (for USDT-M Futures).
`STOP_MARKET` is a separate type not covered here but follows the same pattern
in `orders.py`.

---

## License

This project is provided for educational purposes on the Binance Futures
Testnet. **Never run it with real funds without thorough testing and risk
management controls.**
