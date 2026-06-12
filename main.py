import sys
import warnings

warnings.filterwarnings("ignore", category=Warning, module="requests")

from bot.logging_config import setup_logging
from bot.cli import run

if __name__ == "__main__":
    setup_logging()
    sys.exit(run())
