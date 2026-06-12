from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

from bot.logging_config import get_logger

logger = get_logger(__name__)


def place_market_order(client, symbol, side, quantity):
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": Client.FUTURE_ORDER_TYPE_MARKET,
        "quantity": quantity,
    }

    logger.info("REQUEST [MARKET] %s", params)

    try:
        resp = client.futures_create_order(**params)
    except BinanceAPIException as e:
        logger.error("API error: code=%s msg=%s", e.code, e.message)
        raise RuntimeError(f"Binance API error [{e.code}]: {e.message}") from e
    except BinanceRequestException as e:
        logger.error("Network error: %s", e.message)
        raise RuntimeError(f"Network error: {e.message}") from e
    except Exception as e:
        logger.exception("Unexpected error placing market order: %s", e)
        raise

    logger.info("RESPONSE [MARKET] %s", resp)
    return resp


def place_limit_order(client, symbol, side, quantity, price, time_in_force="GTC"):
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": Client.FUTURE_ORDER_TYPE_LIMIT,
        "quantity": quantity,
        "price": price,
        "timeInForce": time_in_force,
    }

    logger.info("REQUEST [LIMIT] %s", params)

    try:
        resp = client.futures_create_order(**params)
    except BinanceAPIException as e:
        logger.error("API error: code=%s msg=%s", e.code, e.message)
        raise RuntimeError(f"Binance API error [{e.code}]: {e.message}") from e
    except BinanceRequestException as e:
        logger.error("Network error: %s", e.message)
        raise RuntimeError(f"Network error: {e.message}") from e
    except Exception as e:
        logger.exception("Unexpected error placing limit order: %s", e)
        raise

    logger.info("RESPONSE [LIMIT] %s", resp)
    return resp


def place_stop_limit_order(client, symbol, side, quantity, price, stop_price, time_in_force="GTC"):
    # STOP type on USDT-M futures triggers a limit order when stop_price is hit
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": Client.FUTURE_ORDER_TYPE_STOP,
        "quantity": quantity,
        "price": price,
        "stopPrice": stop_price,
        "timeInForce": time_in_force,
    }

    logger.info("REQUEST [STOP_LIMIT] %s", params)

    try:
        resp = client.futures_create_order(**params)
    except BinanceAPIException as e:
        logger.error("API error: code=%s msg=%s", e.code, e.message)
        raise RuntimeError(f"Binance API error [{e.code}]: {e.message}") from e
    except BinanceRequestException as e:
        logger.error("Network error: %s", e.message)
        raise RuntimeError(f"Network error: {e.message}") from e
    except Exception as e:
        logger.exception("Unexpected error placing stop-limit order: %s", e)
        raise

    logger.info("RESPONSE [STOP_LIMIT] %s", resp)
    return resp
