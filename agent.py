import time
import pandas as pd
from mcp_server import get_historical_bars, place_market_order, get_account_balance

def calculate_sma(df, period):
    """Calculate Simple Moving Average."""
    return df['close'].rolling(window=period).mean()

def calculate_rsi(df, period=14):
    """Calculate Relative Strength Index."""
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(df, short_period=12, long_period=26, signal_period=9):
    """Calculate MACD and Signal Line."""
    short_ema = df['close'].ewm(span=short_period, adjust=False).mean()
    long_ema = df['close'].ewm(span=long_period, adjust=False).mean()
    macd = short_ema - long_ema
    signal_line = macd.ewm(span=signal_period, adjust=False).mean()
    return macd, signal_line

def check_trading_signal(symbol: str) -> str:
    """
    Checks if a stock should be bought or sold based on a multi-indicator consensus strategy (SMA, RSI, MACD).
    """
    print(f"[{symbol}] Analyzing historical data...")
    # Simulate calling the MCP tool to get data
    response = get_historical_bars(symbol, timeframe='1Day', limit=100)
    
    if "error" in response:
        print(f"[{symbol}] Error fetching data: {response['error']}")
        return "hold"
        
    bars = response['bars']
    if len(bars) < 30:
        print(f"[{symbol}] Not enough data to calculate indicators.")
        return "hold"
        
    df = pd.DataFrame(bars)
    
    # Calculate Indicators
    df['SMA_5'] = calculate_sma(df, 5)
    df['SMA_20'] = calculate_sma(df, 20)
    df['RSI'] = calculate_rsi(df, 14)
    df['MACD'], df['MACD_Signal'] = calculate_macd(df)
    
    # Get the latest two rows
    latest = df.iloc[-1]
    previous = df.iloc[-2]
    
    # SMA Signal
    sma_buy = previous['SMA_5'] <= previous['SMA_20'] and latest['SMA_5'] > latest['SMA_20']
    sma_sell = previous['SMA_5'] >= previous['SMA_20'] and latest['SMA_5'] < latest['SMA_20']
    
    # RSI Signal (Overbought > 70 = sell, Oversold < 30 = buy)
    rsi_buy = latest['RSI'] < 30
    rsi_sell = latest['RSI'] > 70
    
    # MACD Signal
    macd_buy = previous['MACD'] <= previous['MACD_Signal'] and latest['MACD'] > latest['MACD_Signal']
    macd_sell = previous['MACD'] >= previous['MACD_Signal'] and latest['MACD'] < latest['MACD_Signal']
    
    # Consensus Logic (Requires 2 out of 3 indicators to agree)
    buy_signals = sum([sma_buy, rsi_buy, macd_buy])
    sell_signals = sum([sma_sell, rsi_sell, macd_sell])
    
    if buy_signals >= 2:
        return "buy"
    elif sell_signals >= 2:
        return "sell"
        
    return "hold"

def run_trading_bot():
    """Main trading loop for the AI agent."""
    print("=== AI Trading Agent Started ===")
    
    # Simulate getting account balance
    balance = get_account_balance()
    if "error" in balance:
        print(f"Failed to connect to Alpaca: {balance['error']}")
        print("Note: You need to set ALPACA_API_KEY and ALPACA_SECRET_KEY environment variables.")
        return
        
    print(f"Initial Portfolio Value: ${balance.get('portfolio_value', 0):.2f}")
    print(f"Available Cash: ${balance.get('cash', 0):.2f}")
    
    tickers_to_watch = ["AAPL", "MSFT", "GOOGL", "NVDA"]
    
    for symbol in tickers_to_watch:
        signal = check_trading_signal(symbol)
        
        if signal == "buy":
            print(f"[{symbol}] SIGNAL: BUY! Executing order...")
            # Simulate placing order (buying 1 share for simplicity)
            result = place_market_order(symbol, 1.0, "buy")
            print(f"[{symbol}] Order Result: {result}")
            
        elif signal == "sell":
            print(f"[{symbol}] SIGNAL: SELL! Executing order...")
            result = place_market_order(symbol, 1.0, "sell")
            print(f"[{symbol}] Order Result: {result}")
            
        else:
            print(f"[{symbol}] SIGNAL: HOLD. No action taken.")
            
        time.sleep(1) # Rate limiting prevention

if __name__ == "__main__":
    # Note: To run this for real, you must set your Alpaca API keys as environment variables
    # e.g., export ALPACA_API_KEY='your_key'
    #       export ALPACA_SECRET_KEY='your_secret'
    run_trading_bot()
