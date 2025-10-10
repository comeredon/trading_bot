"""
Trading Algorithm Bot - Main Entry Point
Analyzes historical data from Asian and London markets to execute rules on NYSE
"""

import argparse
from datetime import datetime, timedelta
from trading_bot.data_fetcher import DataFetcher
from trading_bot.rule_engine import RuleEngine
from trading_bot.analyzer import MarketAnalyzer
from trading_bot.config import Config


def main():
    parser = argparse.ArgumentParser(description='Trading Algorithm Bot')
    parser.add_argument('--config', type=str, default='config.json',
                        help='Path to configuration file')
    parser.add_argument('--rules', type=str, default='rules.json',
                        help='Path to trading rules file')
    parser.add_argument('--days', type=int, default=3,
                        help='Number of historical days to analyze')
    
    args = parser.parse_args()
    
    # Load configuration
    config = Config(args.config)
    
    # Initialize components
    data_fetcher = DataFetcher(config)
    rule_engine = RuleEngine(args.rules)
    analyzer = MarketAnalyzer()
    
    print("=" * 60)
    print("Trading Algorithm Bot - Starting Analysis")
    print("=" * 60)
    
    # Fetch historical data from Asian markets
    print("\n[1/4] Fetching Asian market data...")
    asia_data = data_fetcher.fetch_market_data(
        market='asia',
        days=args.days
    )
    
    # Fetch historical data from London market
    print("[2/4] Fetching London market data...")
    london_data = data_fetcher.fetch_market_data(
        market='london',
        days=args.days
    )
    
    # Analyze combined market data
    print("[3/4] Analyzing market trends...")
    analysis_results = analyzer.analyze(asia_data, london_data)
    
    # Execute rules on NYSE
    print("[4/4] Executing trading rules on NYSE...")
    trading_signals = rule_engine.execute_rules(analysis_results)
    
    # Display results
    print("\n" + "=" * 60)
    print("Analysis Results")
    print("=" * 60)
    analyzer.display_summary(analysis_results)
    
    print("\n" + "=" * 60)
    print("Trading Signals for NYSE")
    print("=" * 60)
    rule_engine.display_signals(trading_signals)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"results/trading_signals_{timestamp}.json"
    rule_engine.save_signals(trading_signals, results_file)
    print(f"\n✓ Results saved to: {results_file}")
    
    # Export to MetaTrader 5 format
    print("\n" + "=" * 60)
    print("Exporting to MetaTrader 5 Format")
    print("=" * 60)
    
    from trading_bot.mt5_exporter import MT5Exporter
    mt5_exporter = MT5Exporter()
    
    mt5_files = mt5_exporter.export_signals(trading_signals, analysis_results)
    
    print("\n✓ MT5 Files Generated:")
    for file_type, file_path in mt5_files.items():
        print(f"  - {file_type.upper()}: {file_path}")
    
    # Create indicator data
    indicator_file = mt5_exporter.create_mt5_indicator_data(analysis_results)
    print(f"  - INDICATOR DATA: {indicator_file}")
    
    print("\n" + "=" * 60)
    print("MT5 Integration Instructions")
    print("=" * 60)
    print("1. Copy files from 'mt5_signals/' folder to MT5 'Files' directory")
    print("2. CSV file: Import into EA or custom indicator")
    print("3. JSON file: Use with MT5 Python integration")
    print("4. MQ5 file: Compile in MetaEditor and run as script")
    print("5. Comment file: Copy content to chart comment")
    print("=" * 60)


if __name__ == "__main__":
    main()
