import os
from typing import Any
import alpaca_trade_api as tradeapi
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("AlpacaTradingServer")

# Initialize Alpaca API client
# Requires environment variables: ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_ENDPOINT
api_key = os.environ.get("ALPACA_API_KEY", "dummy_key")
secret_key = os.environ.get("ALPACA_SECRET_KEY", "dummy_secret")
base_url = os.environ.get("ALPACA_ENDPOINT", "https://paper-api.alpaca.markets")

api = tradeapi.REST(api_key, secret_key, base_url, api_version='v2')

@mcp.tool()
def get_account_balance() -> dict[str, Any]:
    """Get the current account balance and buying power."""
    try:
        account = api.get_account()
        return {
            "cash": float(account.cash),
            "buying_power": float(account.buying_power),
            "portfolio_value": float(account.portfolio_value),
            "status": account.status
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_stock_price(symbol: str) -> dict[str, Any]:
    """Get the latest quote and trade price for a stock symbol."""
    try:
        quote = api.get_latest_quote(symbol)
        trade = api.get_latest_trade(symbol)
        return {
            "symbol": symbol,
            "latest_trade_price": trade.price,
            "bid_price": quote.bid_price,
            "ask_price": quote.ask_price,
            "timestamp": str(trade.timestamp)
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_historical_bars(symbol: str, timeframe: str = "1Day", limit: int = 100) -> dict[str, Any]:
    """
    Get historical price bars for a stock symbol.
    Timeframe options: '1Min', '1Hour', '1Day', etc.
    """
    try:
        bars = api.get_bars(symbol, timeframe, limit=limit).df
        if bars.empty:
            return {"error": "No data found"}
        
        # Convert to records format for easy JSON serialization
        records = bars.reset_index().to_dict(orient="records")
        # Ensure timestamps are strings
        for row in records:
            if 'timestamp' in row:
                row['timestamp'] = str(row['timestamp'])
        
        return {
            "symbol": symbol,
            "bars": records
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def place_market_order(symbol: str, qty: float, side: str) -> dict[str, Any]:
    """
    Place a market order to buy or sell a stock.
    Side must be 'buy' or 'sell'.
    """
    if side not in ['buy', 'sell']:
        return {"error": "Side must be 'buy' or 'sell'"}
        
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='market',
            time_in_force='gtc' # Good till cancelled
        )
        return {
            "id": order.id,
            "symbol": order.symbol,
            "qty": order.qty,
            "side": order.side,
            "status": order.status
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("Starting Alpaca MCP Server...")
    mcp.run()
