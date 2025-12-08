"""
Simple executor for running strategies periodically.

Features:
- Loads `config_us30.json` and starts a background thread
- Fetches M5/H1 candles from MetaTrader5 (if available)
- Runs `SMCStrategy.analyze()` and logs results to console/log file
- Will only place orders if environment variable `ALLOW_PLACE_ORDERS=1` is set
"""

import os
import json
import time
import threading
import logging
from pathlib import Path
from datetime import datetime

from src.strategies import SMCStrategy


LOG_PATH = Path('./logs/us30_bot.log')
LOG_PATH.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH, encoding='utf-8'),
        logging.StreamHandler()
    ]
)


def load_config():
    path = os.getenv('CONFIG_PATH', './config_us30.json')
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load config {path}: {e}")
        return {}


def start(poll_seconds: int = 30):
    """Start executor thread (daemon)."""
    thread = threading.Thread(target=_run, args=(poll_seconds,), daemon=True)
    thread.start()
    logging.info("Executor thread started")


def _run(poll_seconds: int):
    config = load_config()
    execution_cfg = config.get('execution', {})
    strategies_cfg = config.get('strategies', {})

    active = strategies_cfg.get('active', [])

    # Only run SMC by default here
    if 'smc' not in active or not strategies_cfg.get('smc', {}).get('enabled', False):
        logging.info("SMC strategy not active or enabled in config; executor will remain idle.")
        return

    smc = SMCStrategy(strategies_cfg.get('smc', {}))

    # Try to import MT5 but fail gracefully
    try:
        import MetaTrader5 as mt5
        mt5_available = True
    except Exception:
        mt5_available = False
        logging.warning("MetaTrader5 not available; executor will only run in offline/demo mode.")

    symbol = config.get('broker', {}).get('symbol', 'US30m')

    allow_place = os.getenv('ALLOW_PLACE_ORDERS', '0') == '1'
    if allow_place:
        logging.warning("ALLOW_PLACE_ORDERS=1 detected: executor MAY attempt to place orders (demo).")

    while True:
        try:
            entry_data = None
            bias_data = None

            if mt5_available:
                if not mt5.initialize():
                    logging.debug("MT5 initialize() returned False")
                else:
                    # Fetch M5 and H1
                    try:
                        rates_m5 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, smc.min_candles)
                        rates_h1 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 20)
                        import pandas as pd
                        if rates_m5 is not None and len(rates_m5) > 0:
                            entry_data = pd.DataFrame(rates_m5)[['open', 'high', 'low', 'close', 'tick_volume']]
                        if rates_h1 is not None and len(rates_h1) > 0:
                            bias_data = pd.DataFrame(rates_h1)[['open', 'high', 'low', 'close', 'tick_volume']]
                    except Exception as e:
                        logging.error(f"Error fetching rates from MT5: {e}")
                        entry_data = None
                        bias_data = None
            else:
                # No MT5: do nothing but log that executor is idle
                logging.debug("MT5 not available; skipping data fetch")

            if entry_data is None or bias_data is None:
                logging.info("Insufficient live data for analysis (MT5 missing or not enough candles).")
            else:
                signal = smc.analyze(entry_data, bias_data)
                now = datetime.utcnow().isoformat()
                logging.info(f"SMC analyze result at {now}: signal={signal['signal']} strength={signal['strength']} details={signal.get('details')} ")

                if signal['signal'] != 'NONE' and execution_cfg.get('enabled', False):
                    logging.info(f"Valid signal detected: {signal['signal']} — entry {signal['entry_price']} SL {signal['stop_loss']} TP {signal['take_profit']}")

                    if allow_place and mt5_available:
                        # Attempt to place a market order (demo). Use small volume and the mt5 API.
                        try:
                            tick = mt5.symbol_info_tick(symbol)
                            price = tick.ask if signal['signal'] == 'BUY' else tick.bid
                            volume = 0.01
                            order_type = mt5.ORDER_TYPE_BUY if signal['signal'] == 'BUY' else mt5.ORDER_TYPE_SELL
                            request = {
                                "action": mt5.TRADE_ACTION_DEAL,
                                "symbol": symbol,
                                "volume": volume,
                                "type": order_type,
                                "price": price,
                                "sl": float(signal['stop_loss']) if signal.get('stop_loss') else 0.0,
                                "tp": float(signal['take_profit']) if signal.get('take_profit') else 0.0,
                                "deviation": execution_cfg.get('deviation_points', 50),
                                "magic": execution_cfg.get('magic_number', 0),
                                "comment": execution_cfg.get('comment', 'US30_BOT'),
                            }
                            result = mt5.order_send(request)
                            logging.info(f"Order send result: {result}")
                        except Exception as e:
                            logging.error(f"Failed to place order: {e}")
                    else:
                        logging.info("Order placement skipped (ALLOW_PLACE_ORDERS not set or MT5 not available).")

            time.sleep(poll_seconds)

        except Exception as exc:
            logging.exception(f"Executor loop error: {exc}")
            time.sleep(poll_seconds)
