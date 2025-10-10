#!/usr/bin/env python3
"""
Trading Algorithm Bot - Main Entry Point
Analyzes Asian and London stock market data to generate NYSE trading signals
"""

import argparse
import json
import os
from datetime import datetime

from trading_bot.config import Config
from trading_bot.data_fetcher import DataFetcher
from trading_bot.analyzer import MarketAnalyzer
from trading_bot.rule_engine import RuleEngine
from trading_bot.mt5_exporter import MT5Exporter


def print_header():
    """Print application header"""
    print("=" * 60)
    print("Trading Algorithm Bot - Starting Analysis")
    print("=" * 60)
    print()


def main():
    """Main execution function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Trading Algorithm Bot')
    parser.add_argument('--config', default='config.json',
                       help='Path to configuration file')
    parser.add_argument('--rules', default='rules.json',
                       help='Path to rules file')
    parser.add_argument('--days', type=int, default=3,
                       help='Number of historical days to analyze')
    
    args = parser.parse_args()
    
    print_header()
    
    # Initialize components
    config = Config(args.config)
    fetcher = DataFetcher(config)
    analyzer = MarketAnalyzer()
    rule_engine = RuleEngine(args.rules)
    mt5_exporter = MT5Exporter()
    
    # Step 1: Fetch Asian market data
    print("[1/4] Fetching Asian market data...")
    asia_data = fetcher.fetch_market_data('asia', days=args.days)
    
    # Step 2: Fetch London market data
    print("\n[2/4] Fetching London market data...")
    london_data = fetcher.fetch_market_data('london', days=args.days)
    
    # Step 3: Analyze market trends
    print("\n[3/4] Analyzing market trends...")
    analysis = analyzer.analyze(asia_data, london_data)
    
    # Step 4: Execute trading rules
    print("\n[4/4] Executing trading rules on NYSE...")
    signals = rule_engine.execute_rules(analysis)
    
    # Display results
    print("\n" + "=" * 60)
    print("Analysis Results")
    print("=" * 60)
    analyzer.display_summary(analysis)
    
    print("\n" + "=" * 60)
    print("Trading Signals for NYSE")
    print("=" * 60)
    rule_engine.display_signals(signals)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = 'results'
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f'trading_signals_{timestamp}.json')
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'analysis': analysis,
        'signals': signals
    }
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nResults saved to: {output_file}")
    
    # Export for MT5
    print("\n" + "=" * 60)
    print("Exporting Signals for MetaTrader 5")
    print("=" * 60)
    
    mt5_files = mt5_exporter.export_signals(signals, analysis)
    
    print("\nMT5-compatible files generated:")
    for file_type, file_path in mt5_files.items():
        print(f"  {file_type.upper()}: {file_path}")
    
    # Create indicator data file
    indicator_file = mt5_exporter.create_mt5_indicator_data(analysis)
    print(f"  INDICATOR: {indicator_file}")
    
    print("\n" + "=" * 60)
    print("To use with MT5:")
    print("  1. Copy files from mt5_signals/ to MT5 data folder")
    print("  2. See MT5_INTEGRATION_GUIDE.md for detailed instructions")
    print("  3. Run execute_mt5_signals.py for automated execution")
    print("=" * 60)
    print("\nBot execution completed successfully!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExecution interrupted by user.")
    except Exception as e:
        print(f"\n\nError: {str(e)}")
        import traceback
        traceback.print_exc()
