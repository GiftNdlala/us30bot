# 🚀 SMC Strategy - Quick Start Guide

## 5-Minute Setup

### 1. Verify Installation ✓
```bash
# Check SMC strategy is accessible
python3 -c "from src.strategies import SMCStrategy; print('✓ SMC imported successfully')"
```

### 2. Test the Strategy ✓
```bash
# Run the example to see it working
python3 smc_strategy_example.py
```

### 3. Check Configuration ✓
The strategy is already configured in `config_us30.json`:
```json
{
  "strategies": {
    "active": ["smc", "nyupip", "basic_signal"],
    "smc": {
      "enabled": true,
      "entry_timeframe": "M5",
      "bias_timeframe": "H1",
      "ema_period": 50,
      "rr_ratio": 3
    }
  }
}
```

### 4. Start the Bot ✓
```bash
python3 start_us30_bot.py
```

The bot will automatically:
- Load the SMC strategy
- Analyze M5 candles with H1 bias
- Generate BUY/SELL signals
- Create orders based on signals

---

## What SMC Does

**Detects 5 Smart Money Components:**

1. **BOS** (Break of Structure)
   - Price breaks last 2 swing highs or lows

2. **MSS** (Market Structure Shift)
   - Last 3 candles each progressively higher/lower

3. **OB** (Order Block)
   - Previous candle imbalance level

4. **FVG** (Fair Value Gap)
   - 3-candle imbalance gap

5. **LS** (Liquidity Sweep)
   - Wick extends beyond previous swing

**Plus:**
- 🎯 **EMA Bias**: H1 EMA 50 for trend confirmation
- 📊 **Confluence Scoring**: 0-100 strength metric
- 💰 **Risk Management**: 1:3 R:R ratio

---

## Signal Example

### BUY Signal
```
Signal: BUY ✓
Strength: 80/100 (strong)

Entry: 16,850
Stop Loss: 16,810
Take Profit: 16,970

Confluence:
  ✓ Break of Structure (yes)
  ✓ Market Structure Shift (yes)
  ✓ Liquidity Sweep (yes)
  ✗ Order Block (no)
  ✗ Fair Value Gap (no)
```

### No Signal
```
Signal: NONE
Reason: Insufficient data or no SMC confluence
```

---

## File Structure

```
/workspaces/us30bot/
├── config_us30.json              ← SMC configured here
├── start_us30_bot.py             ← Start bot (loads SMC)
├── smc_strategy_example.py       ← Test & examples
├── SMC_STRATEGY_GUIDE.md         ← Full documentation
├── SMC_INTEGRATION_SUMMARY.md    ← This integration summary
├── src/
│   ├── __init__.py
│   └── strategies/
│       ├── __init__.py           ← Exports SMCStrategy
│       └── smc_strategy.py       ← Core strategy logic
```

---

## Common Tasks

### Change EMA Period (Default: 50)
Edit `config_us30.json`:
```json
"smc": {
  "ema_period": 20  // or 200 for longer trends
}
```

### Change Risk-Reward Ratio (Default: 3)
Edit `config_us30.json`:
```json
"smc": {
  "rr_ratio": 2.5  // 1:2.5 instead of 1:3
}
```

### Disable SMC Strategy
Edit `config_us30.json`:
```json
"strategies": {
  "active": ["nyupip", "basic_signal"]  // Remove "smc"
}
```

### Enable Only SMC Strategy
Edit `config_us30.json`:
```json
"strategies": {
  "active": ["smc"]  // Only SMC
}
```

---

## Troubleshooting

### "No signals generated"
- ✓ Check: Do you have 100+ M5 candles?
- ✓ Check: Is price clearly above/below EMA on H1?
- ✓ Check: Are BOS + MSS aligned?

### "ImportError: Cannot import SMCStrategy"
- ✓ Run: `python3 -c "from src.strategies import SMCStrategy"`
- ✓ Check: Are you in `/workspaces/us30bot/` directory?
- ✓ Check: Do files exist in `src/strategies/`?

### "Signals are too frequent/infrequent"
- ✓ Adjust: Increase EMA period for fewer signals
- ✓ Adjust: Decrease EMA period for more signals
- ✓ Adjust: Increase min_candles requirement

---

## Understanding Signal Strength

| Strength | Confluences | Interpretation |
|----------|-------------|-----------------|
| 30-40 | 2 (BOS + MSS only) | Weak signal |
| 60-70 | 3 (+ OB/FVG/LS) | Moderate signal |
| 80-90 | 4 (multiple confluences) | Strong signal |
| 95-100 | 5 (all components) | Maximum confidence |

**Tip:** Only trade signals with 70+ strength for best results.

---

## Next Steps

1. **Review**: Read `SMC_STRATEGY_GUIDE.md` for full documentation
2. **Test**: Run `python3 smc_strategy_example.py`
3. **Configure**: Adjust parameters in `config_us30.json` if needed
4. **Run**: Start bot with `python3 start_us30_bot.py`
5. **Monitor**: Check dashboard at `http://localhost:5001`
6. **Backtest**: Test strategy with historical data
7. **Paper Trade**: Practice in demo mode first
8. **Live Trade**: When confident, enable live trading

---

## Performance Tips

✅ **Do:**
- Trade during high activity hours (09:30-16:00 ET)
- Use 1:3+ risk-reward ratio
- Wait for 70+ strength signals
- Combine with other indicators
- Keep logs and analyze results

❌ **Don't:**
- Trade signals with <60 strength
- Trade outside NYSE hours
- Over-leverage positions
- Skip stop-loss orders
- Trade immediately after news events

---

## Getting Help

1. **Read**: `SMC_STRATEGY_GUIDE.md` (comprehensive guide)
2. **Examples**: `smc_strategy_example.py` (working code)
3. **Code**: `src/strategies/smc_strategy.py` (detailed comments)
4. **Config**: `config_us30.json` (all parameters)

---

## Status

✅ **Strategy**: Ready to use
✅ **Configuration**: Done
✅ **Testing**: Verified
✅ **Integration**: Complete
✅ **Documentation**: Comprehensive

**Start trading with SMC now!** 🚀

---

**Quick Links:**
- Strategy Code: `src/strategies/smc_strategy.py`
- Full Guide: `SMC_STRATEGY_GUIDE.md`
- Examples: `smc_strategy_example.py`
- Config: `config_us30.json` (line 72)
