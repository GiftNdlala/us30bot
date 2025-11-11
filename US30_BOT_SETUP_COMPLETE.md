# ✅ US30 Bot Setup - COMPLETE

## 🎉 Your Dedicated US30 Trading Bot is Ready!

All files have been created successfully. You now have a **completely separate US30 bot** that runs independently from your Gold/XAU bot.

---

## 📁 Files Created

### Core Files
1. ✅ **`config_us30.json`** (2.7 KB)
   - US30-specific configuration
   - NYSE trading hours (09:30-16:00 ET)
   - Risk management: 0.5% per trade, max 5 positions
   - Daily loss limit: 5%
   - Starts in DEMO mode (safe!)

2. ✅ **`start_us30_bot.py`** (3.4 KB, executable)
   - Dedicated US30 bot launcher
   - Runs on port 5001 (separate from Gold bot's 5000)
   - Sets environment variables automatically
   - Includes prerequisite checks

3. ✅ **`requirements_us30.txt`**
   - All Python dependencies
   - MT5, Flask, pandas, yfinance, ta, etc.
   - Install with: `pip install -r requirements_us30.txt`

### Documentation
4. ✅ **`README_US30.md`** (9.4 KB)
   - Comprehensive documentation
   - Installation & setup guide
   - US30 vs Gold differences
   - Strategy configuration
   - Troubleshooting guide
   - Security best practices

5. ✅ **`QUICKSTART_US30.md`** (6.8 KB)
   - 5-minute quick start guide
   - Essential commands
   - Testing workflow
   - Common troubleshooting
   - Pro tips for US30 trading

### Configuration Templates
6. ✅ **`.env.us30.example`**
   - Environment variable template
   - Credentials management
   - Copy to `.env.us30` and fill in values

7. ✅ **`.gitignore_us30`**
   - Git ignore rules for US30 bot
   - Protects sensitive credentials
   - Add to your main `.gitignore`

### Directories
8. ✅ **`data/`** - For US30 trade database (`us30_trades.sqlite`)
9. ✅ **`logs/`** - For US30 bot logs (`us30_bot.log`)

---

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies
```bash
pip install -r requirements_us30.txt
```

### 2. Configure MT5 Credentials
Edit `config_us30.json`:
```json
{
  "broker": {
    "login": YOUR_MT5_LOGIN,      // ← Add your MT5 login
    "password": "YOUR_PASSWORD",   // ← Add your password
    "server": "Exness-MT5Trial9"   // ← Your broker server
  }
}
```

### 3. Start the Bot
```bash
python start_us30_bot.py
```

Then open: **http://localhost:5001**

---

## 🎯 What's Configured Out of the Box

### ✅ Trading Parameters
- **Symbol**: US30m (Dow Jones Industrial Average)
- **Timeframe**: M15 (15-minute charts)
- **Risk per trade**: 0.5% of account
- **Max concurrent trades**: 5 positions
- **Daily loss limit**: 5% (auto-stops trading)
- **Max open risk**: 8% total account exposure

### ✅ Trading Hours (NYSE)
- **Active**: Monday-Friday, 09:30-16:00 ET
- **Automatic**: Bot respects these hours
- **Configurable**: Edit in `config_us30.json`

### ✅ Active Strategies
1. **NYUPIP Strategy**
   - 1H SMA + 15M CIS entries
   - RSI confirmation
   - Works with US30 out of the box

2. **Basic Signal Generator**
   - SMA crossovers
   - RSI signals
   - MACD signals

### ✅ Safety Features
- Starts in **DEMO mode** by default
- Execution **disabled** by default
- Daily loss limit protection
- Max open risk protection
- Campaign-based trade management
- Position timeout mechanism

---

## 🔄 Running Both Bots Together

Your setup now supports **dual-bot operation**:

| Bot | Port | Config | Database | Symbol |
|-----|------|--------|----------|--------|
| **Gold Bot** | 5000 | `config.json` | `data/trades.sqlite` | XAUUSDm |
| **US30 Bot** | 5001 | `config_us30.json` | `data/us30_trades.sqlite` | US30m |

### Start Both:
```bash
# Terminal 1 - Gold Bot
python live_dashboard.py

# Terminal 2 - US30 Bot  
python start_us30_bot.py
```

### Access Dashboards:
- Gold: http://localhost:5000
- US30: http://localhost:5001

Each operates **completely independently**:
- ✅ Separate configurations
- ✅ Separate databases
- ✅ Separate risk management  
- ✅ Different trading hours
- ✅ Independent strategies

---

## 📊 US30-Specific Optimizations

The bot is pre-configured with US30-optimized settings:

### Position Sizing
```json
{
  "execution": {
    "low_tp_pips": 30,        // US30: 30 pips (Gold: 20)
    "medium_tp_pips": 60,     // US30: 60 pips (Gold: 40)
    "high_tp_pips": 100       // US30: 100 pips (Gold: 60)
  }
}
```

### Trading Rules
- **Spread filter**: Max 50 points (tighter than Gold)
- **More positions**: 5 concurrent (vs 3 for Gold)
- **Slippage**: 20 points (good liquidity)
- **Campaign trades**: 10-20 per cycle (higher volume)

### US30 Characteristics Built-In
- Point value: $1.00 per point
- Typical daily range: 200-500 points
- Best hours: 09:30 open, 15:30-16:00 close
- News events: Automatically cautious during volatility

---

## 🎨 Next Steps (Your Custom Strategies)

You mentioned adding **custom US30 signals** later. Here's how:

### Adding a New Strategy

1. **Create strategy file**: `src/strategies/my_us30_strategy.py`

2. **Implement logic**:
   ```python
   def generate_signals(symbol, timeframe, data):
       # Your US30-specific logic here
       signals = []
       
       # Example: US30 opening range breakout
       if is_nyse_open() and price_breaks_opening_range():
           signals.append({
               'type': 'BUY',
               'confidence': 'HIGH',
               'reason': 'Opening range breakout'
           })
       
       return signals
   ```

3. **Add to config**:
   ```json
   {
     "strategies": {
       "active": ["nyupip", "basic_signal", "my_us30_strategy"],
       "my_us30_strategy": {
         "enabled": true,
         "param1": "value1"
       }
     }
   }
   ```

4. **Test in demo mode!**

### Strategy Ideas for US30
- 📈 Opening range breakouts (first 30 min)
- 📈 Closing auction strategies (last 30 min)
- 📈 Market structure breaks (ICT concepts)
- 📈 Correlation with SPX/NDX
- 📈 News-driven momentum
- 📈 Gap trading strategies

---

## 🛡️ Security Checklist

Before going live:

- [ ] ⚠️ Never commit `config_us30.json` with real credentials to git
- [ ] ⚠️ Add US30 files to `.gitignore` (use `.gitignore_us30` as reference)
- [ ] ⚠️ Test in demo mode for at least 1-2 weeks
- [ ] ⚠️ Monitor logs daily: `tail -f logs/us30_bot.log`
- [ ] ⚠️ Set up database backups (enabled in config)
- [ ] ⚠️ Start with minimum position sizes
- [ ] ⚠️ Review trades daily in database
- [ ] ⚠️ Only enable live trading when confident

---

## 📈 Monitoring & Maintenance

### View Trade History
```bash
# Last 24 hours (US30 trades)
python get_trade_history.py 24 json | jq '.trades[] | select(.symbol == "US30m")'
```

### Check Bot Status
```bash
# Is bot running?
ps aux | grep start_us30_bot

# API status check
curl http://localhost:5001/api/status
```

### View Logs
```bash
# Live log monitoring
tail -f logs/us30_bot.log

# Last 50 entries
tail -50 logs/us30_bot.log

# Search for errors
grep ERROR logs/us30_bot.log
```

### Database Queries
```bash
# Open database
sqlite3 data/us30_trades.sqlite

# Example queries:
SELECT COUNT(*) FROM trades WHERE symbol = 'US30m';
SELECT AVG(profit_pips) FROM trades WHERE symbol = 'US30m' AND profit_pips > 0;
```

---

## 📚 Documentation Reference

| File | Purpose | Size |
|------|---------|------|
| `README_US30.md` | Full documentation | 9.4 KB |
| `QUICKSTART_US30.md` | Quick start guide | 6.8 KB |
| `config_us30.json` | Bot configuration | 2.7 KB |
| `start_us30_bot.py` | Launcher script | 3.4 KB |

**Read these files for detailed information!**

---

## 🎯 Key Differences from Gold Bot

| Feature | Gold Bot | US30 Bot |
|---------|----------|----------|
| **Port** | 5000 | **5001** |
| **Config** | `config.json` | **`config_us30.json`** |
| **Database** | `data/trades.sqlite` | **`data/us30_trades.sqlite`** |
| **Symbol** | XAUUSDm | **US30m** |
| **Hours** | 24/5 | **09:30-16:00 ET** |
| **Point Value** | $0.01 | **$1.00** |
| **Daily Range** | 20-50 pips | **200-500 points** |
| **Max Positions** | 3 | **5** |
| **TP Levels** | 20/40/60 | **30/60/100** |

---

## ✅ Setup Status: COMPLETE

### What's Done ✅
- [x] Configuration file created (`config_us30.json`)
- [x] Launcher script created (`start_us30_bot.py`)
- [x] Directory structure created (`data/`, `logs/`)
- [x] Documentation written (README, Quick Start)
- [x] Requirements file created
- [x] Environment template created
- [x] Git ignore template created
- [x] US30-specific optimizations applied
- [x] Safety features enabled (demo mode, limits)

### What You Need to Do 🎯
1. Install dependencies: `pip install -r requirements_us30.txt`
2. Add MT5 credentials to `config_us30.json`
3. Run the bot: `python start_us30_bot.py`
4. Test in demo mode (1-2 weeks minimum)
5. Add your custom US30 strategies when ready
6. Enable live trading once confident

---

## 🚀 You're Ready to Go!

Your **dedicated US30 trading bot** is fully set up and ready to run. The bot is configured with:

✅ Conservative risk management  
✅ NYSE trading hours  
✅ Demo mode enabled (safe to start)  
✅ Separate from Gold bot (no conflicts)  
✅ Ready for your custom US30 strategies  

### First Command:
```bash
pip install -r requirements_us30.txt && python start_us30_bot.py
```

### First URL:
```
http://localhost:5001
```

---

**Happy US30 Trading! 📊🚀**

For questions or issues, review:
1. `QUICKSTART_US30.md` - Quick troubleshooting
2. `README_US30.md` - Full documentation
3. `logs/us30_bot.log` - Runtime logs
