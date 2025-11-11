#!/usr/bin/env python3
"""
US30 Trading Bot Launcher
==========================
Dedicated launcher for US30 (Dow Jones) trading bot.
Runs independently from the XAU/Gold bot on a separate port.

Features:
- Separate configuration (config_us30.json)
- Separate database (data/us30_trades.sqlite)
- Runs on port 5001 (default Gold bot uses 5000)
- US30-specific strategies and risk management
- NYSE trading hours (09:30-16:00 ET)
"""

import os
import sys
from pathlib import Path

# Set environment variables BEFORE importing any bot modules
os.environ['CONFIG_PATH'] = './config_us30.json'
os.environ['US30_SYMBOL'] = 'US30m'
os.environ['DB_PATH'] = './data/us30_trades.sqlite'
os.environ['BOT_NAME'] = 'US30_BOT'
os.environ['LOG_PREFIX'] = '[US30]'

def check_prerequisites():
    """Check if all required files and directories exist."""
    print("🔍 Checking US30 bot prerequisites...")
    
    # Check config file
    config_path = Path('./config_us30.json')
    if not config_path.exists():
        print("❌ Error: config_us30.json not found!")
        return False
    print("✅ Config file found: config_us30.json")
    
    # Create data directory if it doesn't exist
    data_dir = Path('./data')
    data_dir.mkdir(exist_ok=True)
    print(f"✅ Data directory ready: {data_dir}")
    
    # Create logs directory if it doesn't exist
    logs_dir = Path('./logs')
    logs_dir.mkdir(exist_ok=True)
    print(f"✅ Logs directory ready: {logs_dir}")
    
    return True

def main():
    """Main entry point for US30 bot."""
    print("=" * 60)
    print("🚀 US30 Trading Bot - Starting...")
    print("=" * 60)
    print(f"📊 Symbol: US30m (Dow Jones Industrial Average)")
    print(f"⚙️  Config: {os.getenv('CONFIG_PATH')}")
    print(f"💾 Database: {os.getenv('DB_PATH')}")
    print(f"🌐 Web Dashboard: http://localhost:5001")
    print(f"🕐 Trading Hours: 09:30-16:00 ET (NYSE)")
    print("=" * 60)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed. Please fix the issues above.")
        sys.exit(1)
    
    try:
        # Import bot modules AFTER setting environment variables
        from live_dashboard import app, init_live_stream
        
        print("\n🔄 Initializing US30 live data stream...")
        init_live_stream()
        
        print("\n✅ US30 bot initialized successfully!")
        print("🌐 Starting web dashboard on http://0.0.0.0:5001")
        print("📊 Open your browser to access the dashboard")
        print("⚠️  Press CTRL+C to stop the bot\n")
        
        # Start Flask dashboard on port 5001 (different from Gold bot)
        app.run(
            host='0.0.0.0',
            port=5001,
            debug=False,
            use_reloader=False  # Prevent double initialization
        )
        
    except ImportError as e:
        print(f"\n❌ Error importing bot modules: {e}")
        print("💡 Make sure all required Python packages are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Error starting US30 bot: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  US30 bot stopped by user (CTRL+C)")
        print("👋 Goodbye!")
        sys.exit(0)
