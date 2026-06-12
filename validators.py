from bot.logging_config import get_logger

logger = get_logger(__name__)

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP"}

MIN_QTY = 0.0
MAX_QTY = 1_000_000.0
MIN_PRICE = 0.0
MAX_PRICE = 10_000_000.0


def validate_symbol(symbol):
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol can't be empty (e.g. BTCUSDT).")
    if not symbol.isalnum():
        raise ValueError(f"'{symbol}' looks wrong — use letters and digits only (e.g. BTCUSDT).")
    logger.debug("Symbol ok: %s", symbol.upper())


def validate_side(side):
    if side.upper() not in VALID_SIDES:
        raise ValueError(f"Side must be BUY or SELL, got '{side}'.")
    logger.debug("Side ok: %s", side.upper())


def validate_order_type(order_type):
    if order_type.upper() not in VALID_ORDER_TYPES:
        raise ValueError(f"Order type must be MARKET, LIMIT, or STOP — got '{order_type}'.")
    logger.debug("Order type ok: %s", order_type.upper())


def validate_quantity(quantity):
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValueError(f"Quantity '{quantity}' isn't a valid number.")

    if qty <= MIN_QTY:
        raise ValueError(f"Quantity must be positive, got {qty}.")
    if qty > MAX_QTY:
        raise ValueError(f"Quantity {qty} is too large (max {MAX_QTY}).")

    logger.debug("Quantity ok: %s", qty)


def validate_price(price, order_type):
    if order_type.upper() == "MARKET":
        logger.debug("Skipping price check for MARKET order")
        return

    if price is None:
        raise ValueError(f"--price is required for {order_type.upper()} orders.")

    try:
        p = float(price)
    except (TypeError, ValueError):
        raise ValueError(f"Price '{price}' isn't a valid number.")

    if p <= MIN_PRICE:
        raise ValueError(f"Price must be positive, got {p}.")
    if p > MAX_PRICE:
        raise ValueError(f"Price {p} is too large (max {MAX_PRICE}).")

    logger.debug("Price ok: %s", p)


def validate_stop_price(stop_price, order_type):
    if order_type.upper() != "STOP":
        return

    if stop_price is None:
        raise ValueError("--stop_price is required for STOP orders.")

    try:
        sp = float(stop_price)
    except (TypeError, ValueError):
        raise ValueError(f"Stop price '{stop_price}' isn't a valid number.")

    if sp <= MIN_PRICE:
        raise ValueError(f"Stop price must be positive, got {sp}.")

    logger.debug("Stop price ok: %s", sp)


def validate_all(*, symbol, side, order_type, quantity, price=None, stop_price=None):
    """Run all checks and collect every error before raising so the user sees them all at once."""
    errors = []

    checks = [
        (validate_symbol,     {"symbol": symbol}),
        (validate_side,       {"side": side}),
        (validate_order_type, {"order_type": order_type}),
        (validate_quantity,   {"quantity": quantity}),
        (validate_price,      {"price": price, "order_type": order_type}),
        (validate_stop_price, {"stop_price": stop_price, "order_type": order_type}),
    ]

    for fn, kwargs in checks:
        try:
            fn(**kwargs)
        except ValueError as e:
            errors.append(str(e))

    if errors:
        raise ValueError("Validation failed:\n  • " + "\n  • ".join(errors))

    logger.info("All inputs valid — %s %s %s qty=%s", order_type.upper(), side.upper(), symbol.upper(), quantity)
