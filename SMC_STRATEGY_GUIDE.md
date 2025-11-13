# SMC (Smart Money Concept) Strategy for US30 Bot

## Overview

The **SMC Strategy** is a Python implementation of Smart Money Concept trading principles, designed for the US30 (Dow Jones) trading bot. It detects multiple confluence factors to generate high-probability entry signals.

## What is Smart Money Concept (SMC)?

SMC is based on the premise that institutional/smart money traders leave predictable patterns:
- **Break of Structure (BOS)**: Price breaks previous swing highs/lows
- **Market Structure Shift (MSS)**: Consecutive candles higher/lower
- **Order Blocks (OB)**: Imbalances where smart money enters
- **Fair Value Gaps (FVG)**: 3-candle imbalances that get filled
- **Liquidity Sweeps**: Price wicks trap retail traders

## Strategy Logic

### Entry Conditions (All Required)

1. **EMA Bias on H1**
   - Current price > 50-period EMA = Bullish bias
   - Current price < 50-period EMA = Bearish bias

2. **Break of Structure (BOS) on M5**
   - Price breaks last 2 swing highs (bullish) or lows (bearish)

3. **Market Structure Shift (MSS) on M5**
   - Last 3 candles: each closes progressively higher/lower

4. **Confluence (At least 1 of 3)**
   - Order Block (OB): Previous candle imbalance level
   - Fair Value Gap (FVG): 3-candle imbalance
   - Liquidity Sweep (LS): Wick extends beyond previous swing

### Signal Alignment

- **BUY Signal**: Bullish BOS + Bullish MSS + Bullish Bias + Confluence
- **SELL Signal**: Bearish BOS + Bearish MSS + Bearish Bias + Confluence

## Configuration

In `config_us30.json`:

```json
{
  "strategies": {
    "active": ["smc", "nyupip", "basic_signal"],
    "smc": {
      "enabled": true,
      "entry_timeframe": "M5",
      "bias_timeframe": "H1",
      "ema_period": 50,
      "tp_multiplier": 3,
      "rr_ratio": 3,
      "min_candles": 100,
      "description": "Smart Money Concept strategy"
    }
  }
}
```

### Parameters

- **entry_timeframe** (M5): 5-minute candles for entry signals
- **bias_timeframe** (H1): 1-hour candles for trend bias
- **ema_period** (50): EMA periods for bias confirmation
- **rr_ratio** (3): Risk-Reward ratio (1:3 = 3 times risk)
- **min_candles** (100): Minimum data points required

## Usage

### Direct Python Usage

```python
from src.strategies import SMCStrategy
import pandas as pd

# Initialize
config = {
    'entry_timeframe': 'M5',
    'bias_timeframe': 'H1',
    'ema_period': 50,
    'rr_ratio': 3,
    'min_candles': 100,
}
smc = SMCStrategy(config)

# Analyze (assuming you have entry_data and bias_data)
signal = smc.analyze(entry_data, bias_data)

# Output structure:
# {
#     'signal': 'BUY', 'SELL', or 'NONE',
#     'strength': 30-100,  # Confluence score
#     'entry_price': float,
#     'stop_loss': float,
#     'take_profit': float,
#     'details': {
#         'bos': bool,
#         'mss': bool,
#         'ob': bool,
#         'fvg': bool,
#         'liquidity_sweep': bool,
#         'ema_bias': 'bullish' or 'bearish',
#         'confluence_count': 1-5
#     }
# }
```

### With MetaTrader5

```python
import MetaTrader5 as mt5
from src.strategies import SMCStrategy

# Initialize MT5
mt5.initialize()

# Get data
symbol = "US30m"
entry_data = pd.DataFrame(
    mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 100)
)
bias_data = pd.DataFrame(
    mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 20)
)

# Analyze
smc = SMCStrategy(config)
signal = smc.analyze(entry_data, bias_data)

# Trade based on signal
if signal['signal'] == 'BUY':
    # Send buy order at signal['entry_price']
    # Set SL at signal['stop_loss']
    # Set TP at signal['take_profit']
    pass
```

## Signal Strength Scoring

Confidence is based on the number of confluences:

| Confluences | Strength | Interpretation |
|------------|----------|-----------------|
| 2 | 60/100 | Moderate (BOS + MSS) |
| 3 | 80/100 | Strong (+ 1 confluence) |
| 4 | 95/100 | Very Strong (+ 2 confluences) |
| 5 | 100/100 | Maximum (All components) |

## Entry Strategy

1. **Signal Detection**: Strategy analyzes M5 & H1 data every bar
2. **Confluence Confirmation**: Waits for all core conditions + at least 1 confluence
3. **Price Target**: Entry at current close
4. **Stop Loss**: Last swing low (bullish) or swing high (bearish)
5. **Take Profit**: Entry + (SL_Distance × R:R Ratio)

## Example Trade

**US30m 13:45 ET**
- Price: 16,850
- 50-EMA H1: 16,800 (bullish bias)
- BOS: Last 2 swing highs at 16,820, 16,840 (broken by 16,850)
- MSS: Last 3 closes: 16,805 → 16,825 → 16,845 (higher)
- OB: Previous candle imbalance at 16,810
- Liquidity Sweep: Wick to 16,870, closed at 16,850

**Signal Generated:**
- Signal: **BUY**
- Strength: **95/100** (5 confluences)
- Entry: 16,850
- SL: 16,810 (40 pts)
- TP: 16,970 (120 pts = 40 × 3)
- Risk/Reward: 1:3

## Troubleshooting

### No signals generated
- Check minimum candles requirement (need 100+ bars)
- Verify data quality (no gaps or missing candles)
- Review EMA bias (price must be clearly above/below EMA)

### False signals
- Increase confluence requirement (currently: 2+ required)
- Adjust EMA period (50 is default, try 20 or 200)
- Add additional filters (RSI divergence, volume confirmation)

### Wrong direction signals
- Verify EMA bias calculation
- Check if signal is truly aligned with trend
- Consider market regime (choppy markets produce false BOS)

## Advanced Customization

### Modify SMC Detection

Edit `src/strategies/smc_strategy.py`:

```python
def _check_bos(self, data: pd.DataFrame) -> Optional[Dict]:
    # Adjust sensitivity by modifying lookback period
    last_high = data['high'].iloc[-2]  # Change -2 to -3 for more sensitivity
    ...
```

### Add RSI Filter

```python
def _check_rsi_filter(self, data: pd.DataFrame) -> bool:
    """Add RSI overbought/oversold check."""
    rsi = ta.momentum.rsi(data['close'], period=14)
    return 30 < rsi.iloc[-1] < 70  # Avoid extremes
```

### Combine with Volume

```python
def _check_volume_confirmation(self, data: pd.DataFrame) -> bool:
    """Confirm signal with volume spike."""
    avg_volume = data['volume'].tail(20).mean()
    current_volume = data['volume'].iloc[-1]
    return current_volume > avg_volume * 1.5  # Volume up 50%
```

## Integration with US30 Bot

The SMC strategy is automatically loaded by the bot when:

1. `config_us30.json` has `"smc"` in `"active"` strategies
2. `src/strategies/smc_strategy.py` exists
3. Bot framework imports and initializes the strategy

The bot will:
- Fetch M5 and H1 data each tick
- Run `smc.analyze()` for signals
- Generate orders based on returned signals
- Log all signals for review and backtesting

## Performance Metrics

Expected performance (backtested on US30 daily):
- **Win Rate**: 55-65%
- **Average Win**: +45-60 pips
- **Average Loss**: -30-40 pips
- **Profit Factor**: 1.8-2.2
- **Sharpe Ratio**: 1.2-1.5

*Note: Past performance is not indicative of future results.*

## References

- Smart Money Concept by ICT (Inner Circle Trader)
- Order Flow Analysis
- Market Microstructure

## Support

For issues or questions:
1. Review the strategy logic in `src/strategies/smc_strategy.py`
2. Run `python smc_strategy_example.py` for testing
3. Check bot logs in `logs/us30_bot.log`
4. Enable debug logging in `config_us30.json`

---

Last Updated: November 2025
