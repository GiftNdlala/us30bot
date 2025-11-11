# ⚡ US30 Bot - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Install Dependencies (1 min)
```bash
pip install -r requirements_us30.txt
```

### Step 2: Configure MT5 Credentials (2 min)
Edit `config_us30.json` lines 7-9:
```json
"login": 12345678,           # Your MT5 login
"password": "your_password",  # Your MT5 password
"server": "Exness-MT5Trial9"  # Your broker server
```

### Step 3: Start the Bot (1 min)
```bash
python start_us30_bot.py
```

### Step 4: Open Dashboard (30 sec)
Open browser: **http://localhost:5001**

---

## ✅ Pre-Flight Checklist

Before running the bot:

- [ ] Python 3.8+ installed
- [ ] MT5 installed and running
- [ ] `requirements_us30.txt` packages installed
- [ ] `config_us30.json` credentials configured
- [ ] US30m symbol available in your MT5 account
- [ ] Sufficient account balance for US30 trading

---

## 🎯 First-Time Configuration

### Risk Settings (IMPORTANT!)

The bot defaults to **demo mode** with conservative settings:

| Setting | Default | Adjust To |
|---------|---------|-----------|
| **Risk per trade** | 0.5% | Your preference |
| **Max concurrent trades** | 5 | 3-8 recommended |
| **Daily loss limit** | 5% | 3-10% recommended |
| **Execution enabled** | ❌ False | ✅ True (when ready) |
| **Demo only** | ✅ True | ❌ False (when ready) |

Edit these in `config_us30.json`:

```json
{
  "risk": {
    "risk_percent_per_trade": 0.5,
    "max_concurrent_trades": 5,
    "symbol_caps": {
      "US30m": {
        "daily_loss_limit_pct": 5.0
      }
    }
  },
  "execution": {
    "enabled": false,  // ⚠️ Change to true when ready
    "demo_only": true  // ⚠️ Change to false for live trading
  }
}
```

---

## 🕐 Trading Hours

**US30 trading is active during NYSE hours:**

- **Start**: 09:30 AM ET
- **End**: 04:00 PM ET
- **Days**: Monday - Friday

The bot automatically:
- ✅ Starts trading at 09:30 ET
- ✅ Stops new entries at 16:00 ET
- ✅ Closes positions at end of session (optional)
- ✅ Respects US market holidays

---

## 📊 Dashboard Features

Access at **http://localhost:5001**

### Main Controls
- **Start/Stop Trading** - Enable/disable trade execution
- **Live Price Feed** - Real-time US30 price updates
- **Open Positions** - View all active trades
- **Trade History** - Recent trade performance
- **Risk Monitor** - Current exposure and daily P&L

### Key Metrics Displayed
- Current US30 price (^DJI from Yahoo Finance)
- Open positions count
- Today's P&L
- Daily loss limit remaining
- Active signals (NYUPIP, Basic Signal)

---

## 🧪 Testing Workflow

### Phase 1: Demo Testing (1 week minimum)
1. ✅ Start bot in demo mode
2. ✅ Verify strategies generate signals
3. ✅ Check trade execution in MT5
4. ✅ Monitor win rate and drawdown
5. ✅ Review logs daily

### Phase 2: Paper Trading Review
1. ✅ Analyze trade history database
2. ✅ Calculate profit factor
3. ✅ Identify best trading hours
4. ✅ Optimize TP/SL levels
5. ✅ Adjust risk parameters if needed

### Phase 3: Live Trading (when ready)
1. ⚠️ Change `"demo_only": false` in config
2. ⚠️ Change `"enabled": true` in execution section
3. ⚠️ Start with minimum position sizes
4. ⚠️ Monitor closely for first few days
5. ⚠️ Scale up gradually

---

## 🛡️ Safety Features

The bot includes multiple safety mechanisms:

### Auto-Stop Conditions
- ❌ Daily loss limit reached (-5% by default)
- ❌ Max open risk exceeded (8% default)
- ❌ Outside trading hours
- ❌ MT5 connection lost
- ❌ Excessive spread detected

### Risk Controls
- ✅ Per-trade risk capped at 0.5%
- ✅ Max 5 concurrent positions
- ✅ Stop-loss on every trade
- ✅ Position timeout (closes stale trades)
- ✅ Campaign-based entry management

---

## 📈 Performance Monitoring

### View Recent Trades
```bash
# Last 24 hours
python get_trade_history.py 24 json

# Last 7 days
python get_trade_history.py 168 json

# Filter US30 trades only
python get_trade_history.py 24 json | jq '.trades[] | select(.symbol == "US30m")'
```

### Check Bot Logs
```bash
# View live logs
tail -f logs/us30_bot.log

# Search for errors
grep ERROR logs/us30_bot.log

# View last 50 lines
tail -50 logs/us30_bot.log
```

### Database Location
- **Path**: `data/us30_trades.sqlite`
- **Backup**: Enable in config (`"backup_enabled": true`)
- **Query**: Use SQLite browser or Python scripts

---

## 🔧 Common Commands

### Start Bot
```bash
python start_us30_bot.py
```

### Stop Bot
Press `CTRL+C` in terminal

### Restart Bot
```bash
# Stop with CTRL+C, then:
python start_us30_bot.py
```

### Check if Running
```bash
ps aux | grep start_us30_bot
```

### View Dashboard Status
```bash
curl http://localhost:5001/api/status
```

---

## 🐛 Quick Troubleshooting

### Bot won't start
```bash
# Check if port 5001 is available
lsof -i :5001

# Verify config exists
ls -la config_us30.json

# Test Python packages
python -c "import MetaTrader5, flask, pandas; print('OK')"
```

### No trades executing
1. Check if execution is enabled in config
2. Verify trading hours (09:30-16:00 ET)
3. Confirm MT5 connection is active
4. Review logs for error messages

### Dashboard not loading
1. Ensure bot is running (`ps aux | grep start_us30_bot`)
2. Check firewall (if accessing remotely)
3. Try accessing from `http://127.0.0.1:5001`

---

## 📞 Need Help?

### Debug Mode
Enable detailed logging in `config_us30.json`:
```json
{
  "monitoring": {
    "log_level": "DEBUG"
  }
}
```

### Check Configuration
```bash
# Validate JSON syntax
python -m json.tool config_us30.json
```

### Review Strategy Status
Check dashboard → Strategy section → Active strategies

---

## 🎯 Next Steps After Setup

1. **Run in demo mode for 1-2 weeks**
2. **Add custom US30 strategies** (you mentioned this is coming)
3. **Optimize parameters** based on results
4. **Enable live trading** when confident
5. **Monitor and adjust** continuously

---

## ⚡ Pro Tips

- 💡 US30 is most active at NYSE open (09:30 ET) and close (15:30-16:00 ET)
- 💡 Avoid trading during major news events (FOMC, NFP, etc.)
- 💡 Watch for correlation with S&P 500 (^GSPC) and Nasdaq (^IXIC)
- 💡 US30 respects technical levels better than Gold
- 💡 Consider wider stops during first 30 minutes of trading
- 💡 Close all positions before weekends (gap risk)

---

## 🚀 Run Both Bots Simultaneously

You can run **BOTH Gold and US30 bots** at the same time:

**Terminal 1 (Gold Bot):**
```bash
python live_dashboard.py  # Port 5000
```

**Terminal 2 (US30 Bot):**
```bash
python start_us30_bot.py  # Port 5001
```

Access dashboards:
- Gold: http://localhost:5000
- US30: http://localhost:5001

Each bot operates independently with separate:
- ✅ Configs
- ✅ Databases  
- ✅ Risk management
- ✅ Trading sessions

---

**Ready to trade US30! 📊🚀**

For detailed documentation, see `README_US30.md`
