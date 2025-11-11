# 🚀 US30 Trading Bot - Dedicated Setup

## Overview

This is a **completely separate US30 (Dow Jones) trading bot** that runs independently from your Gold/XAU bot. It has its own configuration, database, strategies, and web dashboard.

### Key Features
- ✅ **Separate Configuration**: `config_us30.json` with US30-specific settings
- ✅ **Separate Database**: `data/us30_trades.sqlite` for US30 trade history
- ✅ **Independent Dashboard**: Runs on port `5001` (Gold bot uses `5000`)
- ✅ **NYSE Trading Hours**: 09:30-16:00 ET automatically enforced
- ✅ **US30-Optimized Risk Management**: Larger position sizes for indices
- ✅ **Ready for Custom US30 Strategies**: Easily add US30-specific signals

---

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **MetaTrader 5** installed (for live trading)
3. **Exness account** with US30m symbol available
4. **Required Python packages**:
   ```bash
   pip install MetaTrader5 pandas numpy flask yfinance ta
   ```

---

## 🛠️ Installation & Setup

### Step 1: Configure MT5 Credentials

Edit `config_us30.json` and update your broker credentials:

```json
{
  "broker": {
    "login": YOUR_MT5_LOGIN_NUMBER,
    "password": "YOUR_MT5_PASSWORD",
    "server": "Exness-MT5Trial9"
  }
}
```

### Step 2: Configure Risk Parameters

Review and adjust risk settings in `config_us30.json`:

```json
{
  "risk": {
    "risk_percent_per_trade": 0.5,      // 0.5% risk per trade
    "max_concurrent_trades": 5,          // Max 5 open US30 positions
    "symbol_caps": {
      "US30m": {
        "daily_loss_limit_pct": 5.0,    // Stop trading if -5% daily loss
        "max_open_risk_pct": 8.0        // Max 8% total account risk
      }
    }
  }
}
```

### Step 3: Set Trading Hours

US30 trading is configured for NYSE hours by default:

```json
{
  "sessions": {
    "timezone": "America/New_York",
    "trade_start": "09:30",
    "trade_end": "16:00",
    "days": ["Mon", "Tue", "Wed", "Thu", "Fri"]
  }
}
```

### Step 4: Enable Execution (Optional)

⚠️ **IMPORTANT**: Bot starts in **DEMO ONLY** mode by default!

To enable live trading:
1. Test thoroughly in demo mode first
2. Edit `config_us30.json`:
   ```json
   {
     "execution": {
       "enabled": true,
       "demo_only": false
     }
   }
   ```

---

## 🚀 Running the US30 Bot

### Start the Bot

```bash
python start_us30_bot.py
```

You should see:
```
============================================================
🚀 US30 Trading Bot - Starting...
============================================================
📊 Symbol: US30m (Dow Jones Industrial Average)
⚙️  Config: ./config_us30.json
💾 Database: ./data/us30_trades.sqlite
🌐 Web Dashboard: http://localhost:5001
🕐 Trading Hours: 09:30-16:00 ET (NYSE)
============================================================
✅ US30 bot initialized successfully!
🌐 Starting web dashboard on http://0.0.0.0:5001
```

### Access the Dashboard

Open your browser and navigate to:
```
http://localhost:5001
```

### Stop the Bot

Press `CTRL+C` in the terminal running the bot.

---

## 📊 US30 vs Gold Trading Differences

| Feature | Gold (XAU) | US30 (Dow Jones) |
|---------|-----------|------------------|
| **Point Value** | $0.01 per point | $1.00 per point |
| **Daily Range** | 20-50 points | 200-500 points |
| **Typical Spread** | 2-5 points | 3-10 points |
| **Trading Hours** | 24 hours | 09:30-16:00 ET |
| **Volatility** | Moderate | Higher during news |
| **Best Sessions** | London, NY open | NYSE open, close |

### US30-Specific Adjustments

1. **Larger TP/SL**: US30 moves in bigger swings
   - Low TP: 30 pips (vs 20 for Gold)
   - Medium TP: 60 pips (vs 40 for Gold)
   - High TP: 100 pips (vs 60 for Gold)

2. **More Concurrent Trades**: Indices can handle more positions
   - Max concurrent: 5 (vs 3 for Gold)

3. **Tighter Spreads**: Better liquidity usually
   - Max spread: 50 points (monitor during news)

---

## 🎯 Active Strategies

The US30 bot currently supports these strategies:

### 1. NYUPIP Strategy (`nyupip`)
- ✅ Works with US30
- Uses 1H SMA + 15M CIS for entry signals
- Configurable in `config_us30.json`:
  ```json
  {
    "strategies": {
      "nyupip": {
        "enabled": true,
        "sma_period_1h": 50,
        "cis_period_15m": 20,
        "rsi_period": 14
      }
    }
  }
  ```

### 2. Basic Signal Generator (`basic_signal`)
- ✅ Works with US30
- SMA crossovers, RSI, MACD signals
- Symbol-agnostic, works on any instrument

### 🔜 Future US30 Strategies

You mentioned adding custom US30 signals later. To add a new strategy:

1. Create strategy file in `src/strategies/your_us30_strategy.py`
2. Add to `config_us30.json`:
   ```json
   {
     "strategies": {
       "active": ["nyupip", "basic_signal", "your_us30_strategy"],
       "your_us30_strategy": {
         "enabled": true,
         "param1": "value1"
       }
     }
   }
   ```

---

## 📁 File Structure

```
/workspace/
├── config_us30.json           # US30 bot configuration
├── start_us30_bot.py          # US30 bot launcher
├── data/
│   └── us30_trades.sqlite     # US30 trade history database
├── logs/
│   └── us30_bot.log          # US30 bot logs
├── src/
│   ├── strategies/           # Strategy modules
│   │   ├── nyupip.py        # NYUPIP strategy (US30 compatible)
│   │   └── basic_signal.py  # Basic signals (US30 compatible)
│   └── ...
└── README_US30.md            # This file
```

---

## 🔄 Running Both Bots Simultaneously

You can run BOTH the Gold bot and US30 bot at the same time:

### Terminal 1 - Gold Bot
```bash
python live_dashboard.py   # Runs on port 5000
```

### Terminal 2 - US30 Bot
```bash
python start_us30_bot.py   # Runs on port 5001
```

### Access Both Dashboards
- **Gold Bot**: http://localhost:5000
- **US30 Bot**: http://localhost:5001

Each bot has:
- ✅ Separate configurations
- ✅ Separate databases
- ✅ Separate risk management
- ✅ Independent trading sessions
- ✅ Separate web dashboards

---

## 🛡️ Risk Management Features

### Daily Loss Limits
- Automatically stops trading if daily loss exceeds 5%
- Resets at market open each day
- Configurable in `config_us30.json`

### Max Open Risk
- Limits total account risk across all open US30 positions
- Default: 8% max total risk
- Prevents over-leveraging

### Position Limits
- Max 5 concurrent US30 trades
- Prevents excessive exposure
- Campaign-based trade management

### Session Control
- Only trades during NYSE hours (09:30-16:00 ET)
- Respects market holidays
- Configurable trading days

---

## 📈 Monitoring & Alerts

### View Trade History

```bash
# View recent US30 trades (last 24 hours)
python get_trade_history.py 24 json | jq '.trades[] | select(.symbol == "US30m")'
```

### Logs

Check logs at:
```bash
tail -f logs/us30_bot.log
```

### Telegram Alerts (Optional)

Enable in `config_us30.json`:
```json
{
  "monitoring": {
    "telegram": {
      "enabled": true,
      "bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
      "chat_id": "YOUR_CHAT_ID"
    }
  }
}
```

---

## 🐛 Troubleshooting

### Bot won't start

1. **Check prerequisites**:
   ```bash
   python -c "import MetaTrader5, flask, pandas; print('All packages OK')"
   ```

2. **Verify config file exists**:
   ```bash
   ls -la config_us30.json
   ```

3. **Check port availability**:
   ```bash
   lsof -i :5001  # Should be empty if port is free
   ```

### No trades being executed

1. **Check if execution is enabled**:
   - Look for `"enabled": true` in `config_us30.json`

2. **Verify trading hours**:
   - US30 only trades 09:30-16:00 ET (Mon-Fri)

3. **Check MT5 connection**:
   - Ensure MT5 is running
   - Verify credentials in config

4. **Review logs**:
   ```bash
   tail -50 logs/us30_bot.log
   ```

### Dashboard not loading

1. **Check if bot is running**:
   ```bash
   ps aux | grep start_us30_bot
   ```

2. **Verify port 5001 is accessible**:
   ```bash
   curl http://localhost:5001/api/status
   ```

3. **Check firewall settings** (if accessing remotely)

---

## 🔐 Security Notes

- ⚠️ **Never commit `config_us30.json` with real credentials to git**
- ⚠️ Use environment variables for sensitive data in production
- ⚠️ Keep `data/us30_trades.sqlite` backed up regularly
- ⚠️ Test all strategies in demo mode first
- ⚠️ Monitor bot performance regularly

---

## 📞 Support & Development

### Adding Custom US30 Strategies

When you're ready to add your custom US30 signals:

1. Create new strategy file in `src/strategies/`
2. Implement signal generation logic
3. Add to `config_us30.json` active strategies list
4. Test in demo mode thoroughly
5. Enable for live trading

### Adjusting Risk Parameters

Edit `config_us30.json` to tune:
- Trade frequency (campaign settings)
- Position sizing (risk_percent_per_trade)
- TP/SL levels (low_tp_pips, medium_tp_pips, etc.)
- Maximum positions (max_concurrent_trades)

---

## 📝 Version History

- **v1.0** (2025-01-11) - Initial US30 bot setup
  - Separate configuration and launcher
  - NYSE trading hours
  - NYUPIP and basic signal strategies
  - Independent dashboard on port 5001

---

## 🎯 Next Steps

1. ✅ **Test in Demo Mode**: Run for at least 1 week
2. ✅ **Monitor Performance**: Track win rate, drawdown, profit factor
3. ✅ **Add Custom Strategies**: Implement US30-specific signals
4. ✅ **Optimize Parameters**: Fine-tune TP/SL levels
5. ✅ **Enable Live Trading**: Once confident with results

---

**Happy Trading! 📊🚀**
