import argparse
import sys
import warnings

warnings.filterwarnings("ignore", category=Warning, module="requests")

from bot import __version__
from bot.client import get_futures_client
from bot.logging_config import get_logger, setup_logging
from bot.orders import place_limit_order, place_market_order, place_stop_limit_order
from bot.validators import validate_all

logger = get_logger(__name__)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet bot — place MARKET, LIMIT, or STOP-LIMIT orders.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
  python main.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 50000
  python main.py --symbol BTCUSDT --side BUY --type STOP --quantity 0.001 --price 49000 --stop_price 49500
        """,
    )

    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--symbol", type=str, required=True, metavar="SYMBOL",
                        help="Trading pair e.g. BTCUSDT, ETHUSDT")
    parser.add_argument("--side", type=str, required=True, choices=["BUY", "SELL"],
                        metavar="SIDE", help="BUY or SELL")
    parser.add_argument("--type", dest="order_type", type=str, required=True,
                        choices=["MARKET", "LIMIT", "STOP"], metavar="TYPE",
                        help="MARKET, LIMIT, or STOP (stop-limit)")
    parser.add_argument("--quantity", type=float, required=True, metavar="QTY",
                        help="Quantity in base asset units e.g. 0.001 BTC")
    parser.add_argument("--price", type=float, default=None, metavar="PRICE",
                        help="Limit price — required for LIMIT and STOP orders")
    parser.add_argument("--stop_price", type=float, default=None, metavar="STOP_PRICE",
                        help="Stop trigger price — required for STOP orders")
    parser.add_argument("--tif", dest="time_in_force", type=str, default="GTC",
                        choices=["GTC", "IOC", "FOK"], metavar="TIF",
                        help="Time-in-force for LIMIT/STOP orders (default: GTC)")

    return parser


def print_request_summary(args):
    print("\n" + "=" * 60)
    print("          ORDER REQUEST SUMMARY")
    print("=" * 60)
    print(f"  Symbol        : {args.symbol}")
    print(f"  Side          : {args.side}")
    print(f"  Order Type    : {args.order_type}")
    print(f"  Quantity      : {args.quantity}")
    if args.order_type in ("LIMIT", "STOP"):
        print(f"  Price         : {args.price}")
    if args.order_type == "STOP":
        print(f"  Stop Price    : {args.stop_price}")
    if args.order_type != "MARKET":
        print(f"  Time-in-Force : {args.time_in_force}")
    print("=" * 60)


def print_order_response(result):
    # avgPrice is 0 for orders not yet filled, fall back to price in that case
    avg_price = result.get("avgPrice") or result.get("price", "N/A")

    print("\n" + "=" * 60)
    print("          ORDER RESPONSE DETAILS")
    print("=" * 60)
    print(f"  Order ID      : {result.get('orderId', 'N/A')}")
    print(f"  Client OID    : {result.get('clientOrderId', 'N/A')}")
    print(f"  Symbol        : {result.get('symbol', 'N/A')}")
    print(f"  Side          : {result.get('side', 'N/A')}")
    print(f"  Type          : {result.get('type', 'N/A')}")
    print(f"  Status        : {result.get('status', 'N/A')}")
    print(f"  Orig Qty      : {result.get('origQty', 'N/A')}")
    print(f"  Executed Qty  : {result.get('executedQty', 'N/A')}")
    print(f"  Avg Price     : {avg_price}")
    stop = result.get("stopPrice")
    if stop and stop != "0":
        print(f"  Stop Price    : {stop}")
    print(f"  Time-in-Force : {result.get('timeInForce', 'N/A')}")
    print(f"  Update Time   : {result.get('updateTime', 'N/A')}")
    print("=" * 60)


def run(argv=None):
    # make sure unicode output works on windows too
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    setup_logging()

    parser = build_parser()
    args = parser.parse_args(argv)

    # normalise to uppercase throughout
    args.symbol = args.symbol.upper()
    args.side = args.side.upper()
    args.order_type = args.order_type.upper()

    logger.info(
        "CLI invoked: symbol=%s side=%s type=%s qty=%s price=%s stop=%s",
        args.symbol, args.side, args.order_type, args.quantity, args.price, args.stop_price,
    )

    # validate first — no point hitting the API with bad inputs
    try:
        validate_all(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
        )
    except ValueError as e:
        logger.error("Validation failed: %s", e)
        print(f"\n  ❌  {e}\n", file=sys.stderr)
        return 1

    print_request_summary(args)

    try:
        client = get_futures_client()
    except EnvironmentError as e:
        logger.error("Could not init client: %s", e)
        print(f"\n  ❌  {e}\n", file=sys.stderr)
        return 1

    try:
        if args.order_type == "MARKET":
            result = place_market_order(client, args.symbol, args.side, args.quantity)

        elif args.order_type == "LIMIT":
            result = place_limit_order(
                client, args.symbol, args.side, args.quantity, args.price, args.time_in_force
            )

        else:  # STOP
            result = place_stop_limit_order(
                client, args.symbol, args.side, args.quantity,
                args.price, args.stop_price, args.time_in_force
            )

    except Exception as e:
        logger.error("Order failed: %s", e)
        print(f"\n  ❌  Order failed: {e}\n", file=sys.stderr)
        return 1

    print_order_response(result)
    print(f"\n  ✅  {args.order_type} order placed successfully!\n")
    logger.info("Done — orderId=%s status=%s", result.get("orderId"), result.get("status"))

    return 0
