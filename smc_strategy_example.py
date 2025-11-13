"""
SMC Strategy Integration Example
=================================

This module shows how to integrate the SMC strategy with the US30 bot.
"""

import pandas as pd
from src.strategies import SMCStrategy


def example_usage():
    """
    Example showing how to use the SMC strategy.
    """
    
    # Configuration matching config_us30.json
    smc_config = {
        'entry_timeframe': 'M5',
        'bias_timeframe': 'H1',
        'ema_period': 50,
        'tp_multiplier': 3,
        'rr_ratio': 3,
        'min_candles': 100,
    }
    
    # Initialize strategy
    smc = SMCStrategy(smc_config)
    
    # Example: Simulated OHLCV data (M5)
    entry_data = pd.DataFrame({
        'open': [16000 + i*2 for i in range(100)],
        'high': [16020 + i*2 for i in range(100)],
        'low': [15980 + i*2 for i in range(100)],
        'close': [16010 + i*2 for i in range(100)],
        'volume': [1000000] * 100,
    })
    
    # Example: Simulated OHLCV data (H1) - Bias data
    bias_data = pd.DataFrame({
        'open': [16000 + i*10 for i in range(20)],
        'high': [16050 + i*10 for i in range(20)],
        'low': [15950 + i*10 for i in range(20)],
        'close': [16020 + i*10 for i in range(20)],
        'volume': [10000000] * 20,
    })
    
    # Analyze for SMC signals
    signal = smc.analyze(entry_data, bias_data)
    
    print("\n=== SMC Strategy Signal ===")
    print(f"Signal: {signal['signal']}")
    print(f"Strength: {signal['strength']}/100")
    
    if signal['signal'] != 'NONE':
        print(f"\nEntry Price: {signal['entry_price']:.2f}")
        print(f"Stop Loss: {signal['stop_loss']:.2f}")
        print(f"Take Profit: {signal['take_profit']:.2f}")
        print(f"SL Distance: {signal['sl_distance']:.2f}")
        print(f"R:R Ratio: 1:{signal['rr_ratio']}")
        
        print(f"\nConfluence Details:")
        for key, value in signal['details'].items():
            print(f"  {key}: {value}")
    else:
        print(f"No signal. Reason: {signal['details'].get('reason', 'Unknown')}")
    
    # Get strategy status
    status = smc.get_status()
    print(f"\nStrategy Status: {status}")


def integrate_with_mt5_data():
    """
    Example showing how to fetch real MT5 data and use SMC strategy.
    
    This would be integrated into the main bot framework.
    """
    
    try:
        import MetaTrader5 as mt5
    except ImportError:
        print("MetaTrader5 not installed. Install with: pip install MetaTrader5")
        return
    
    # Initialize MT5 (would normally be done by bot framework)
    if not mt5.initialize():
        print("Failed to initialize MT5")
        return
    
    symbol = "US30m"
    smc_config = {
        'entry_timeframe': 'M5',
        'bias_timeframe': 'H1',
        'ema_period': 50,
        'rr_ratio': 3,
        'min_candles': 100,
    }
    
    smc = SMCStrategy(smc_config)
    
    # Fetch M5 data (last 100 candles)
    rates_m5 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 100)
    entry_data = pd.DataFrame(rates_m5)[['open', 'high', 'low', 'close', 'tick_volume']]
    
    # Fetch H1 data (last 20 candles for bias)
    rates_h1 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 20)
    bias_data = pd.DataFrame(rates_h1)[['open', 'high', 'low', 'close', 'tick_volume']]
    
    # Get signal
    signal = smc.analyze(entry_data, bias_data)
    
    print(f"SMC Signal on {symbol}: {signal['signal']}")
    print(f"Strength: {signal['strength']}/100")
    
    if signal['signal'] != 'NONE':
        print(f"Entry: {signal['entry_price']}, SL: {signal['stop_loss']}, TP: {signal['take_profit']}")
    
    mt5.shutdown()


if __name__ == '__main__':
    print("SMC Strategy Examples")
    print("=" * 50)
    example_usage()
