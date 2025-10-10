# Trading Algorithm Bot

A Python-based trading algorithm bot that analyzes historical data from Asian and London stock markets (past 3 days) and executes user-defined trading rules on NYSE.

## Features

- **Multi-Market Analysis**: Fetches and analyzes data from Asian markets (Tokyo, Shanghai, Hong Kong, Singapore) and London (FTSE)
- **Historical Data**: Analyzes past 3 days of market data by default (configurable)
- **Technical Indicators**: Calculates RSI, MACD, Bollinger Bands, SMA, and more
- **Cross-Market Correlations**: Identifies relationships between markets
- **Rule-Based Trading**: Execute custom trading rules on NYSE based on analysis
- **Configurable Rules**: Easy-to-edit JSON format for defining trading strategies

## Installation

1. Install required dependencies:
```powershell
pip install -r requirements.txt
```

2. Configure your settings in `config.json` (optional - defaults are provided)

## Usage

### Basic Usage

Run the bot with default settings:
```powershell
python main.py
```

### Custom Configuration

Specify custom configuration and rules files:
```powershell
python main.py --config custom_config.json --rules custom_rules.json
```

Specify number of historical days to analyze:
```powershell
python main.py --days 5
```

## Configuration

### config.json

Configure data sources, API settings, and analysis parameters:

```json
{
    "data_sources": {
        "asia": {
            "indices": ["^N225", "000001.SS", "^HSI", "^STI"]
        },
        "london": {
            "indices": ["^FTSE"]
        }
    }
}
```

### rules.json

Define your trading rules with conditions and actions:

```json
[
    {
        "id": 1,
        "name": "Bullish Consensus Rule",
        "description": "Enter LONG when both markets are bullish",
        "conditions": {
            "overall_sentiment": "bullish",
            "confidence_min": 0.6
        },
        "action": {
            "type": "LONG",
            "position_size": "moderate",
            "stop_loss": 2.0,
            "take_profit": 5.0
        }
    }
]
```

## Rule Conditions

You can define rules based on:

- `overall_sentiment`: "bullish", "bearish", "neutral", or "mixed"
- `confidence_min`: Minimum confidence level (0.0 to 1.0)
- `signal_strength_min`: Minimum signal strength (0 to 100)
- `correlation_strength`: "strong", "moderate", or "weak"

## Action Types

- `LONG`: Buy/long position
- `SHORT`: Sell/short position
- `HOLD`: Hold current position
- `FOLLOW_TREND`: Follow the detected trend

## Position Sizes

- `conservative`: Small position size
- `moderate`: Medium position size
- `aggressive`: Large position size

## Output

The bot generates:

1. **Console Output**: Real-time analysis and trading signals
2. **JSON Results**: Saved in `results/trading_signals_[timestamp].json`

## Example Output

```
============================================================
Trading Algorithm Bot - Starting Analysis
============================================================

[1/4] Fetching Asian market data...
  Fetching 4 indices from asia...
    ✓ ^N225: 3 data points
    ✓ 000001.SS: 3 data points
    ...

[2/4] Fetching London market data...
  ...

[3/4] Analyzing market trends...

[4/4] Executing trading rules on NYSE...
  ✓ Rule triggered: Bullish Consensus Rule

============================================================
Analysis Results
============================================================
...

============================================================
Trading Signals for NYSE
============================================================

Signal #1: Bullish Consensus Rule
  Action: LONG
  Position Size: moderate
  Stop Loss: 2.0%
  Take Profit: 5.0%
  Confidence: 75.0%
  ...
```

## Customizing Rules

To add your own custom rules:

1. Edit `rules.json` or create a new rules file
2. Define conditions based on market analysis
3. Specify actions to take when conditions are met
4. Run the bot with your custom rules file

Example custom rule:
```json
{
    "id": 10,
    "name": "My Custom Rule",
    "description": "Custom trading strategy",
    "conditions": {
        "overall_sentiment": "bullish",
        "confidence_min": 0.8,
        "signal_strength_min": 70
    },
    "action": {
        "type": "LONG",
        "position_size": "aggressive",
        "stop_loss": 1.0,
        "take_profit": 10.0
    }
}
```

## Limitations

- This bot is for educational and backtesting purposes only
- Does not execute actual trades (paper trading only)
- Requires internet connection to fetch market data
- Historical data limited to yfinance availability

## Disclaimer

This software is for educational purposes only. Do not use it for actual trading without proper testing and risk management. The creators are not responsible for any financial losses.

## License

MIT License
