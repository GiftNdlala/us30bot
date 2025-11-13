# 🌐 US30 Trading Bot - Web Dashboard Guide

## Overview

A professional **real-time web dashboard** displaying live US30 price, open positions, account information, and bot status. Built with **Flask + HTML5 + CSS3 + JavaScript**.

## Features

✅ **Real-time Price Updates** - Live US30 price with change tracking
✅ **Open Positions Display** - All active trades with P/L
✅ **Account Information** - Balance, equity, margin, and levels
✅ **Active Strategies** - Shows currently running strategies
✅ **Live Statistics** - Total P/L, open orders, bot status
✅ **Responsive Design** - Works on desktop, tablet, and mobile
✅ **Dark Theme** - Professional trading interface
✅ **Auto-refresh** - Updates every 2 seconds

## File Structure

```
/workspaces/us30bot/
├── live_dashboard.py           # Flask app & API endpoints
├── templates/
│   └── dashboard.html          # Main HTML template
└── static/
    ├── styles.css              # Dashboard styling
    └── dashboard.js            # Real-time updates & interactivity
```

## Getting Started

### 1. Ensure Flask is Installed
```bash
pip install flask
```

The bot launcher (`start_us30_bot.py`) will automatically start the dashboard.

### 2. Start the Bot
```bash
cd /workspaces/us30bot
python3 start_us30_bot.py
```

### 3. Open Dashboard
Open your browser and navigate to:
```
http://localhost:5001
```

## Dashboard Components

### 📊 Price Card
- **Current US30 Price** in large, easy-to-read format
- **Change** - points and percentage change from previous close
- **Mini Chart** - visual representation of price history (last 100 candles)

### 💰 Account Card
- **Balance** - total account balance
- **Equity** - current equity (balance + profit/loss)
- **Free Margin** - available margin for new positions
- **Used Margin** - margin tied up in open positions
- **Margin Level** - percentage (100%+ safe, <20% warning)

### 📈 Open Positions
Two views of open trades:

**Card View** (Summary)
- Trade type (BUY/SELL)
- Ticket number
- Symbol and volume
- Profit/Loss amount and percentage

**Table View** (Detailed)
- Ticket number
- Trade type
- Volume
- Entry price
- Current price
- Profit/Loss
- Profit/Loss percentage
- Open time

### 🤖 Active Strategies
- Lists all currently enabled strategies
- Shows real-time status
- Updated every 2 seconds

### 📊 Statistics
- **Total P/L** - combined profit/loss from all open positions
- **Open Orders** - number of open positions
- **Bot Status** - current bot state (running, initializing, error)

## API Endpoints

The dashboard provides RESTful API endpoints for data access:

### GET /api/dashboard
Returns all dashboard data:
```json
{
    "symbol": "US30m",
    "current_price": 16850.50,
    "price_change": 25.00,
    "price_change_pct": 0.15,
    "open_tickets": [...],
    "account_balance": 50000.00,
    "equity": 50150.25,
    "free_margin": 45000.00,
    "used_margin": 5000.00,
    "margin_level": 1002.5,
    "last_updated": "2025-11-13T14:35:22.123456",
    "bot_status": "running",
    "active_strategies": ["smc", "nyupip"],
    "total_profit_loss": 150.25
}
```

### GET /api/price
Current price only:
```json
{
    "symbol": "US30m",
    "price": 16850.50,
    "change": 25.00,
    "change_pct": 0.15,
    "timestamp": "2025-11-13T14:35:22.123456"
}
```

### GET /api/tickets
Open positions:
```json
{
    "tickets": [
        {
            "ticket": 123456,
            "symbol": "US30m",
            "type": "BUY",
            "volume": 0.1,
            "entry_price": 16825.00,
            "current_price": 16850.50,
            "profit_loss": 25.50,
            "profit_loss_pct": 0.15,
            "open_time": "2025-11-13T14:30:00",
            "comment": "SMC Entry"
        }
    ],
    "count": 1,
    "total_pl": 25.50,
    "timestamp": "2025-11-13T14:35:22.123456"
}
```

### GET /api/account
Account information:
```json
{
    "balance": 50000.00,
    "equity": 50150.25,
    "free_margin": 45000.00,
    "used_margin": 5000.00,
    "margin_level": 1002.5,
    "timestamp": "2025-11-13T14:35:22.123456"
}
```

### GET /api/status
Bot status:
```json
{
    "status": "running",
    "active_strategies": ["smc", "nyupip"],
    "symbol": "US30m",
    "timestamp": "2025-11-13T14:35:22.123456"
}
```

## Customization

### Change Update Frequency
In `static/dashboard.js`, modify:
```javascript
dashboardState.updateInterval = 2000; // milliseconds
```

Lower values = more frequent updates (increases CPU usage)

### Change Port
In `start_us30_bot.py`, modify:
```python
app.run(
    host='0.0.0.0',
    port=5002,  # Change 5001 to your desired port
    debug=False,
    use_reloader=False
)
```

### Customize Colors
In `static/styles.css`, modify the CSS variables:
```css
:root {
    --primary-color: #1e3a8a;
    --secondary-color: #3b82f6;
    --success-color: #10b981;
    --danger-color: #ef4444;
    /* ... more colors ... */
}
```

### Add More Dashboard Cards
Edit `templates/dashboard.html` to add new card sections, then update `static/dashboard.js` to populate them with data from the API.

## Performance Tips

1. **Reduce Update Frequency** - Change from 2s to 5s for less CPU usage
2. **Disable Animations** - Remove or disable CSS animations for better performance
3. **Use API Selectively** - Only fetch data you need
4. **Cache Data** - Implement browser caching for static assets

## Troubleshooting

### Dashboard won't open
- **Check port**: Make sure port 5001 is not in use
- **Check firewall**: Allow port 5001 through firewall
- **Check logs**: Look for errors in bot logs

### No price showing
- **Check MT5**: Ensure MetaTrader5 is running and connected
- **Check symbol**: Verify 'US30m' is available in your account
- **Check configuration**: Review `config_us30.json` for correct broker settings

### Positions not showing
- **Check MT5**: Verify you have open positions in MT5
- **Check symbol**: Make sure positions are on US30m
- **Check permissions**: Verify account can access position info

### Dashboard slow/not updating
- **Check internet**: Verify connection is stable
- **Check browser**: Try refreshing or opening in incognito mode
- **Check CPU**: Monitor system resources for bottlenecks
- **Increase update interval**: Change from 2s to 5s in `dashboard.js`

## Mobile Access

Access the dashboard from any device on your network:
```
http://<your-computer-ip>:5001
```

Example:
```
http://192.168.1.100:5001
```

## Security Notes

⚠️ **Important**: The dashboard is not password-protected by default.

For production use, add authentication:
1. Use a reverse proxy (nginx, Apache)
2. Add IP whitelisting
3. Implement login/authentication
4. Use HTTPS

## Browser Compatibility

✅ Chrome/Chromium (recommended)
✅ Firefox
✅ Safari
✅ Edge
✅ Mobile browsers (responsive design)

## Features in Development

- 📊 Advanced charts with TradingView
- 📝 Trade history and analytics
- 🔔 Alerts and notifications
- 💾 Data export (CSV, PDF)
- ⚙️ Dashboard customization
- 🔐 User authentication

## Support & Debugging

### Enable Debug Mode
In `start_us30_bot.py`, modify:
```python
app.run(
    host='0.0.0.0',
    port=5001,
    debug=True,  # Enable debug mode
    use_reloader=False
)
```

### Check Console for Errors
Open browser DevTools (F12) → Console tab to see JavaScript errors

### Check Server Logs
Look at terminal output where you started the bot for Flask errors

## Quick Links

- **Dashboard**: `http://localhost:5001`
- **API**: `http://localhost:5001/api/dashboard`
- **Code**: `live_dashboard.py`
- **Templates**: `templates/dashboard.html`
- **Styles**: `static/styles.css`
- **Scripts**: `static/dashboard.js`

## Integration with Bot

The dashboard is **automatically integrated** with the bot:

1. **Auto-starts** when you run `python3 start_us30_bot.py`
2. **Live data** updates from MT5 every 2 seconds
3. **Real-time** price and position tracking
4. **Responsive** to bot events and signals

No additional configuration needed - just start the bot!

---

**Status**: ✅ Ready to use
**Created**: November 13, 2025
**Version**: 1.0

Enjoy your trading dashboard! 🚀
