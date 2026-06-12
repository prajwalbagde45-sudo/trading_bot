import os

from binance.client import Client
from dotenv import load_dotenv

from bot.logging_config import get_logger

logger = get_logger(__name__)

TESTNET_BASE_URL = "https://testnet.binancefuture.com"


def get_futures_client():
    # load .env from project root
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key:
        logger.error("BINANCE_API_KEY missing from environment")
        raise EnvironmentError(
            "BINANCE_API_KEY not set. Copy .env.example to .env and add your testnet credentials."
        )

    if not api_secret:
        logger.error("BINANCE_API_SECRET missing from environment")
        raise EnvironmentError(
            "BINANCE_API_SECRET not set. Copy .env.example to .env and add your testnet credentials."
        )

    logger.debug("Creating Binance Futures Testnet client")
    client = Client(api_key=api_key, api_secret=api_secret, testnet=True)
    logger.info("Client ready — connected to testnet")
    return client
