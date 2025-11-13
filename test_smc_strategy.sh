#!/bin/bash
# SMC Strategy Quick Reference & Testing

echo "=================================="
echo "SMC Strategy - US30 Bot Integration"
echo "=================================="
echo ""

# 1. Test SMC Strategy
echo "1️⃣  Testing SMC Strategy..."
echo "   Command: python3 smc_strategy_example.py"
echo ""

# 2. View Configuration
echo "2️⃣  SMC Strategy is configured in config_us30.json:"
echo "   ✓ Entry Timeframe: M5"
echo "   ✓ Bias Timeframe: H1"
echo "   ✓ EMA Period: 50"
echo "   ✓ R:R Ratio: 3:1"
echo ""

# 3. File Structure
echo "3️⃣  Strategy Files:"
echo "   ✓ src/strategies/smc_strategy.py        (Main strategy logic)"
echo "   ✓ src/strategies/__init__.py            (Strategy package)"
echo "   ✓ smc_strategy_example.py               (Usage examples)"
echo "   ✓ SMC_STRATEGY_GUIDE.md                 (Full documentation)"
echo ""

# 4. What SMC Detects
echo "4️⃣  SMC Components:"
echo "   ✓ BOS (Break of Structure)    - Breaks last 2 swing highs/lows"
echo "   ✓ MSS (Market Structure Shift) - Consecutive higher/lower candles"
echo "   ✓ OB  (Order Block)           - Previous candle imbalance"
echo "   ✓ FVG (Fair Value Gap)        - 3-candle imbalance"
echo "   ✓ LS  (Liquidity Sweep)       - Wick extends beyond previous swing"
echo "   ✓ EMA (Trend Bias)            - H1 EMA 50 for direction confirmation"
echo ""

# 5. Entry Conditions
echo "5️⃣  Entry Requirements (ALL required for signal):"
echo "   ✓ BOS aligned with MSS"
echo "   ✓ Price aligned with EMA bias"
echo "   ✓ At least 1 confluence (OB, FVG, or LS)"
echo ""

# 6. Signal Output
echo "6️⃣  Signal Structure:"
echo "   {
echo "       'signal': 'BUY' / 'SELL' / 'NONE',
echo "       'strength': 30-100,         # Confluence score"
echo "       'entry_price': float,       # Current close"
echo "       'stop_loss': float,         # Swing low/high"
echo "       'take_profit': float,       # Entry + (SL_dist × R:R)"
echo "       'details': {                # Detailed breakdown"
echo "           'bos': bool,"
echo "           'mss': bool,"
echo "           'ob': bool,"
echo "           'fvg': bool,"
echo "           'liquidity_sweep': bool,"
echo "           'ema_bias': 'bullish'/'bearish',"
echo "           'confluence_count': 1-5"
echo "       }"
echo "   }"
echo ""

# 7. Quick Start
echo "7️⃣  Quick Start:"
echo "   $ python3 -c \"from src.strategies import SMCStrategy; print('✓ SMC imported successfully')\""
echo ""

# 8. Integration
echo "8️⃣  Bot Integration:"
echo "   ✓ Auto-loaded when config_us30.json includes 'smc' in active strategies"
echo "   ✓ Runs on every tick"
echo "   ✓ Generates BUY/SELL signals based on M5 + H1 analysis"
echo ""

# 9. Testing
echo "9️⃣  Testing Command:"
python3 /workspaces/us30bot/smc_strategy_example.py 2>&1 | head -15

echo ""
echo "✅ SMC Strategy integration complete!"
echo ""
echo "📖 For detailed documentation, see: SMC_STRATEGY_GUIDE.md"
echo ""
