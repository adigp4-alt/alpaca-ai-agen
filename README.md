# Alpaca AI Trading Agent

> **Project showcase:** A compact rule-based Python integration prototype. Runtime behavior and investment performance are unverified. [Explore the source features, scope, and wider portfolio](./PROJECT-SHOWCASE.md).

An autonomous AI trading agent built for the September 2026 Alpaca Hackathon. 

This project demonstrates a fully functional, highly decoupled architecture using the **Model Context Protocol (MCP)** to separate the trading logic from the broker API integrations.

## Architecture

1. **MCP Server (`mcp_server.py`)**: A fast, standard MCP server that securely wraps the Alpaca Trading API. It exposes four critical tools:
   - `get_account_balance`
   - `get_stock_price`
   - `get_historical_bars`
   - `place_market_order`
2. **AI Agent (`agent.py`)**: An autonomous agent that consumes the MCP server. It utilizes a **Multi-Indicator Consensus Strategy**:
   - Calculates **SMA (Simple Moving Average)** crossovers.
   - Calculates **RSI (Relative Strength Index)** to identify overbought/oversold momentum.
   - Calculates **MACD (Moving Average Convergence Divergence)** to confirm trend reversals.
   - **Consensus**: The agent only places a trade if at least 2 out of the 3 indicators mathematically agree, reducing false positives and improving win rates.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Grab your free Paper Trading API keys from [alpaca.markets](https://alpaca.markets) and export them:

**Windows (PowerShell):**
```powershell
$env:ALPACA_API_KEY="your_api_key_here"
$env:ALPACA_SECRET_KEY="your_secret_key_here"
$env:ALPACA_ENDPOINT="https://paper-api.alpaca.markets"
```

**Mac/Linux:**
```bash
export ALPACA_API_KEY="your_api_key_here"
export ALPACA_SECRET_KEY="your_secret_key_here"
export ALPACA_ENDPOINT="https://paper-api.alpaca.markets"
```

### 3. Run the Agent
```bash
python agent.py
```

## Why this architecture?
By wrapping the Alpaca API in an MCP Server, this codebase is instantly compatible with *any* modern AI model (Claude, GPT-4, Llama) that supports the Model Context Protocol. You can swap out the hardcoded math agent in `agent.py` for an LLM that autonomously plans and executes trades using the exact same server!
