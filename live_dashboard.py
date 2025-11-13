"""
Live Dashboard for US30 Trading Bot
====================================
Flask web dashboard to display:
- Live US30 price
- Open tickets/positions
- Account balance
- Strategy signals
- Trade history
"""

import os
import json
import threading
from datetime import datetime
from flask import Flask, render_template, jsonify, send_from_directory
from pathlib import Path
import pandas as pd
import sqlite3

# Create Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['JSON_SORT_KEYS'] = False

# Global state
dashboard_data = {
    'symbol': 'US30m',
    'current_price': 0.0,
    'price_change': 0.0,
    'price_change_pct': 0.0,
    'open_tickets': [],
    'account_balance': 0.0,
    'equity': 0.0,
    'free_margin': 0.0,
    'used_margin': 0.0,
    'margin_level': 0.0,
    'last_updated': datetime.now().isoformat(),
    'bot_status': 'initializing',
    'active_strategies': [],
    'total_profit_loss': 0.0,
    'trades_today': 0,
    'win_rate': 0.0,
}

# Load configuration
def load_config():
    """Load bot configuration."""
    config_path = os.getenv('CONFIG_PATH', './config_us30.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except:
        return {}

# Initialize data
CONFIG = load_config()


def get_open_tickets():
    """Fetch open tickets from MT5 or database."""
    try:
        import MetaTrader5 as mt5
        
        if not mt5.initialize():
            return []
        
        symbol = CONFIG.get('broker', {}).get('symbol', 'US30m')
        positions = mt5.positions_get(symbol=symbol)
        
        if positions is None:
            return []
        
        tickets = []
        for pos in positions:
            ticket = {
                'ticket': pos.ticket,
                'symbol': pos.symbol,
                'type': 'BUY' if pos.type == 0 else 'SELL',
                'volume': pos.volume,
                'entry_price': pos.price_open,
                'current_price': pos.price_current,
                'profit_loss': pos.profit,
                'profit_loss_pct': (pos.profit / (pos.volume * pos.price_open) * 100) if pos.price_open > 0 else 0,
                'open_time': datetime.fromtimestamp(pos.time).isoformat() if pos.time > 0 else '',
                'comment': pos.comment if pos.comment else '',
            }
            tickets.append(ticket)
        
        return tickets
    except Exception as e:
        print(f"Error fetching tickets: {e}")
        return []


def get_account_info():
    """Get account information from MT5."""
    try:
        import MetaTrader5 as mt5
        
        if not mt5.initialize():
            return {
                'balance': 0,
                'equity': 0,
                'free_margin': 0,
                'used_margin': 0,
                'margin_level': 0,
            }
        
        account_info = mt5.account_info()
        if account_info is None:
            return {
                'balance': 0,
                'equity': 0,
                'free_margin': 0,
                'used_margin': 0,
                'margin_level': 0,
            }
        
        return {
            'balance': account_info.balance,
            'equity': account_info.equity,
            'free_margin': account_info.margin_free,
            'used_margin': account_info.margin,
            'margin_level': account_info.margin_level if account_info.margin > 0 else 0,
        }
    except Exception as e:
        print(f"Error fetching account info: {e}")
        return {
            'balance': 0,
            'equity': 0,
            'free_margin': 0,
            'used_margin': 0,
            'margin_level': 0,
        }


def get_current_price():
    """Get current US30 price from MT5."""
    try:
        import MetaTrader5 as mt5
        
        if not mt5.initialize():
            return 0.0, 0.0, 0.0
        
        symbol = CONFIG.get('broker', {}).get('symbol', 'US30m')
        tick = mt5.symbol_info_tick(symbol)
        
        if tick is None:
            return 0.0, 0.0, 0.0
        
        # Get previous close (from yesterday or 1 day ago)
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 1, 2)
        if rates is not None and len(rates) >= 2:
            prev_close = rates[0]['close']
            current_price = tick.bid
            change = current_price - prev_close
            change_pct = (change / prev_close * 100) if prev_close > 0 else 0
        else:
            current_price = tick.bid
            change = 0.0
            change_pct = 0.0
        
        return current_price, change, change_pct
    except Exception as e:
        print(f"Error fetching price: {e}")
        return 0.0, 0.0, 0.0


def update_dashboard_data():
    """Update dashboard data continuously."""
    global dashboard_data
    
    while True:
        try:
            # Get current price
            price, change, change_pct = get_current_price()
            dashboard_data['current_price'] = price
            dashboard_data['price_change'] = change
            dashboard_data['price_change_pct'] = change_pct
            
            # Get account info
            account_info = get_account_info()
            dashboard_data['account_balance'] = account_info['balance']
            dashboard_data['equity'] = account_info['equity']
            dashboard_data['free_margin'] = account_info['free_margin']
            dashboard_data['used_margin'] = account_info['used_margin']
            dashboard_data['margin_level'] = account_info['margin_level']
            
            # Get open tickets
            tickets = get_open_tickets()
            dashboard_data['open_tickets'] = tickets
            
            # Calculate metrics
            total_pl = sum([t['profit_loss'] for t in tickets])
            dashboard_data['total_profit_loss'] = total_pl
            
            # Get active strategies
            dashboard_data['active_strategies'] = CONFIG.get('strategies', {}).get('active', [])
            
            # Update timestamp
            dashboard_data['last_updated'] = datetime.now().isoformat()
            dashboard_data['bot_status'] = 'running'
            
        except Exception as e:
            print(f"Error updating dashboard: {e}")
            dashboard_data['bot_status'] = 'error'
        
        # Update every 2 seconds
        import time
        time.sleep(2)


def init_live_stream():
    """Initialize live data streaming."""
    # Start background thread for data updates
    update_thread = threading.Thread(target=update_dashboard_data, daemon=True)
    update_thread.start()


@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('dashboard.html')


@app.route('/api/dashboard')
def api_dashboard():
    """API endpoint for dashboard data."""
    return jsonify(dashboard_data)


@app.route('/api/price')
def api_price():
    """API endpoint for current price."""
    return jsonify({
        'symbol': dashboard_data['symbol'],
        'price': dashboard_data['current_price'],
        'change': dashboard_data['price_change'],
        'change_pct': dashboard_data['price_change_pct'],
        'timestamp': dashboard_data['last_updated'],
    })


@app.route('/api/tickets')
def api_tickets():
    """API endpoint for open tickets."""
    return jsonify({
        'tickets': dashboard_data['open_tickets'],
        'count': len(dashboard_data['open_tickets']),
        'total_pl': dashboard_data['total_profit_loss'],
        'timestamp': dashboard_data['last_updated'],
    })


@app.route('/api/account')
def api_account():
    """API endpoint for account info."""
    return jsonify({
        'balance': dashboard_data['account_balance'],
        'equity': dashboard_data['equity'],
        'free_margin': dashboard_data['free_margin'],
        'used_margin': dashboard_data['used_margin'],
        'margin_level': dashboard_data['margin_level'],
        'timestamp': dashboard_data['last_updated'],
    })


@app.route('/api/status')
def api_status():
    """API endpoint for bot status."""
    return jsonify({
        'status': dashboard_data['bot_status'],
        'active_strategies': dashboard_data['active_strategies'],
        'symbol': dashboard_data['symbol'],
        'timestamp': dashboard_data['last_updated'],
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    init_live_stream()
    app.run(host='0.0.0.0', port=5001, debug=False)
