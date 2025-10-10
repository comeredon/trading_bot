# Trading Algorithm Bot

A Python-based trading algorithm bot that analyzes historical data from Asian and London stock markets (past 3 days) and executes user-defined trading rules on NYSE. Enhanced with 7 NQ Stats patterns based on 10-20 years of historical data and full MetaTrader 5 integration.

## Features

- **Multi-Market Analysis**: Fetches and analyzes data from Asian markets (Tokyo, Shanghai, Hong Kong, Singapore) and London (FTSE)
- **NQ Futures Focus**: Optimized for NQ futures (NQ=F) trading
- **Historical Data**: Analyzes past 3 days of market data by default (configurable)
- **Technical Indicators**: Calculates RSI, MACD, Bollinger Bands, SMA, and more
- **NQ Stats Patterns**: 7 proven patterns with 59%-98% success rates:
  - ALN Sessions (Asia-London-NY) - 73%-98% accuracy
  - Initial Balance (IB) - 96% break by 4pm
  - 1-Hour Continuation - 70% accuracy
  - Noon Curve - 74.3% opposite sides
  - Net Change SDEVs - Rubber Band Theory
  - RTH Breaks - 83.29% continuation
  - Morning Judas - Myth-busting (64-70% continuation)
- **Cross-Market Correlations**: Identifies relationships between markets
- **Rule-Based Trading**: Execute custom trading rules on NYSE based on analysis
- **MetaTrader 5 Integration**: 5 export formats (CSV, JSON, MQ5, Comment, Indicator)
- **Automated Execution**: Python script for MT5 signal automation
- **Configurable Rules**: Easy-to-edit JSON format for defining trading strategies

## Installation

1. Clone this repository:
```powershell
git clone https://github.com/comeredon/trading_bot.git
cd trading_bot
```

2. Create a virtual environment (recommended):
```powershell
python -m venv .venv
.venv\Scripts\activate
```

3. Install required dependencies:
```powershell
pip install -r requirements.txt
```

4. (Optional) For MT5 integration, install MT5 Python API:
```powershell
pip install MetaTrader5
```

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

### MetaTrader 5 Integration

For automated signal execution in MT5:
```powershell
python execute_mt5_signals.py
```

See [MT5_INTEGRATION_GUIDE.md](MT5_INTEGRATION_GUIDE.md) for detailed instructions.

## Configuration

### config.json

Configure data sources, API settings, and analysis parameters:

```json
{
    "data_sources": {
        "asia": {
            "indices": ["NQ=F", "^N225", "000001.SS", "^HSI"]
        },
        "london": {
            "indices": ["NQ=F", "^FTSE"]
        },
        "nyse": {
            "indices": ["NQ=F", "^GSPC"]
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

## NQ Stats Patterns

This bot integrates 7 proven statistical patterns from nqstats.com:

1. **ALN Sessions** - Analyzes Asia-London-NY session relationships
2. **Initial Balance** - 96% IB break by 4pm ET
3. **1-Hour Continuation** - 9am hour predicts NY session (70% accuracy)
4. **Noon Curve** - AM/PM opposite extremes (74.3%)
5. **Net Change SDEVs** - Rubber band mean reversion theory
6. **RTH Breaks** - Regular Trading Hours position analysis (83%)
7. **Morning Judas** - Continuation > Reversal (64-70%)

## Output Files

The bot generates multiple output formats:

### JSON Results
- `results/trading_signals_[timestamp].json` - Complete analysis and signals

### MT5 Export Files
- `mt5_signals/mt5_signals_[timestamp].csv` - For Expert Advisors
- `mt5_signals/mt5_signals_[timestamp].json` - Enhanced JSON with metadata
- `mt5_signals/mt5_script_[timestamp].mq5` - Ready-to-compile MQL5 script
- `mt5_signals/mt5_comment_[timestamp].txt` - Chart comment format
- `mt5_signals/mt5_indicator_data_[timestamp].txt` - Custom indicator data

## Example Output

```
============================================================
Trading Algorithm Bot - Starting Analysis
============================================================

[1/4] Fetching Asian market data...
  Fetching 4 indices from asia...
    ✓ NQ=F: 3 data points
    ✓ ^N225: 3 data points
    ...

[2/4] Fetching London market data...
  ...

[3/4] Analyzing market trends...

[4/4] Executing trading rules on NYSE...
  ✓✓ High-confidence NQ Stats signal: london_partial_down

============================================================
NQ Stats Pattern Analysis (10-Year Historical Data)
============================================================

ALN Session Pattern: LONDON_PARTIAL_DOWN
  Description: London broke Asia low but not high
  Confidence: 73%
  Trading Bias: bearish

Initial Balance (9:30-10:30am ET):
  Break by 4pm probability: 96%
  Strategy: Look for short positions targeting IB low break

...

============================================================
Trading Signals for NYSE
============================================================

Signal #1: NQ Stats Pattern Signal
  Action: SHORT
  Confidence: 73.0%
  Entry Strategy: Enter short on London low break
  ...
```

## Disclaimer

**IMPORTANT**: This software is for educational and research purposes only. Always test on a demo account before live trading. The bot provides analysis and recommendations but does not guarantee profits. Use proper risk management and never risk more than you can afford to lose. The creators are not responsible for any financial losses.

## License

MIT License
