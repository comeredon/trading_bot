"""
Rule Engine - Executes user-defined trading rules
"""

import json
import os
from typing import Dict, List
from datetime import datetime


class RuleEngine:
    """Executes trading rules based on market analysis"""
    
    def __init__(self, rules_file='rules.json'):
        self.rules_file = rules_file
        self.rules = self._load_rules()
    
    def _load_rules(self) -> List[Dict]:
        """Load trading rules from JSON file"""
        if os.path.exists(self.rules_file):
            with open(self.rules_file, 'r') as f:
                return json.load(f)
        else:
            # Return default rules
            return self._default_rules()
    
    def _default_rules(self) -> List[Dict]:
        """Default trading rules"""
        return [
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
            },
            {
                "id": 2,
                "name": "Bearish Consensus Rule",
                "description": "Enter SHORT when both markets are bearish",
                "conditions": {
                    "overall_sentiment": "bearish",
                    "confidence_min": 0.6
                },
                "action": {
                    "type": "SHORT",
                    "position_size": "moderate",
                    "stop_loss": 2.0,
                    "take_profit": 5.0
                }
            },
            {
                "id": 3,
                "name": "High Momentum Long",
                "description": "Strong upward momentum detected",
                "conditions": {
                    "overall_sentiment": "bullish",
                    "signal_strength_min": 60
                },
                "action": {
                    "type": "LONG",
                    "position_size": "aggressive",
                    "stop_loss": 1.5,
                    "take_profit": 7.0
                }
            },
            {
                "id": 4,
                "name": "Defensive Position",
                "description": "Mixed signals - reduce exposure",
                "conditions": {
                    "overall_sentiment": "mixed"
                },
                "action": {
                    "type": "HOLD",
                    "position_size": "conservative",
                    "stop_loss": 3.0,
                    "take_profit": 3.0
                }
            },
            {
                "id": 5,
                "name": "Strong Correlation Play",
                "description": "High correlation between markets",
                "conditions": {
                    "correlation_strength": "strong",
                    "overall_sentiment": ["bullish", "bearish"]
                },
                "action": {
                    "type": "FOLLOW_TREND",
                    "position_size": "moderate",
                    "stop_loss": 2.5,
                    "take_profit": 6.0
                }
            }
        ]
    
    def execute_rules(self, analysis: Dict) -> List[Dict]:
        """
        Execute trading rules based on analysis results
        
        Args:
            analysis: Market analysis results
        
        Returns:
            List of triggered trading signals
        """
        signals = []
        combined = analysis['combined_signals']
        correlations = analysis['correlations']
        
        # Check if NQ Stats provides a high-confidence signal
        if 'nq_stats' in analysis:
            nq_decision = analysis['nq_stats'].get('trading_decision', {})
            if nq_decision.get('confidence', 0) >= 0.65:
                # NQ Stats has high confidence - create priority signal
                nq_signal = self._create_nq_stats_signal(nq_decision, analysis)
                signals.append(nq_signal)
                print(f"  ✓✓ High-confidence NQ Stats signal: {nq_decision['primary_signal']}")
        
        # Execute traditional rules
        for rule in self.rules:
            if self._evaluate_rule(rule, combined, correlations):
                signal = self._create_signal(rule, analysis)
                signals.append(signal)
                print(f"  ✓ Rule triggered: {rule['name']}")
        
        if not signals:
            print("  ℹ No rules triggered - no trading signals generated")
        
        return signals
    
    def _evaluate_rule(self, rule: Dict, combined_signals: Dict, 
                       correlations: Dict) -> bool:
        """Evaluate if a rule's conditions are met"""
        conditions = rule['conditions']
        
        # Check sentiment condition
        if 'overall_sentiment' in conditions:
            required_sentiment = conditions['overall_sentiment']
            actual_sentiment = combined_signals['overall_sentiment']
            
            if isinstance(required_sentiment, list):
                if actual_sentiment not in required_sentiment:
                    return False
            else:
                if actual_sentiment != required_sentiment:
                    return False
        
        # Check confidence condition
        if 'confidence_min' in conditions:
            if combined_signals['confidence'] < conditions['confidence_min']:
                return False
        
        # Check signal strength condition
        if 'signal_strength_min' in conditions:
            if combined_signals['signal_strength'] < conditions['signal_strength_min']:
                return False
        
        # Check correlation condition
        if 'correlation_strength' in conditions:
            if correlations['strength'] != conditions['correlation_strength']:
                return False
        
        return True
    
    def _create_signal(self, rule: Dict, analysis: Dict) -> Dict:
        """Create a trading signal from a triggered rule"""
        action = rule['action']
        combined = analysis['combined_signals']
        
        signal = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'rule_id': rule['id'],
            'rule_name': rule['name'],
            'description': rule['description'],
            'action_type': action['type'],
            'position_size': action['position_size'],
            'stop_loss_pct': action.get('stop_loss', 0),
            'take_profit_pct': action.get('take_profit', 0),
            'confidence': combined['confidence'],
            'signal_strength': combined['signal_strength'],
            'factors': combined['factors'],
            'recommendations': analysis['recommendations']
        }
        
        return signal
    
    def _create_nq_stats_signal(self, nq_decision: Dict, analysis: Dict) -> Dict:
        """Create a trading signal from NQ Stats analysis"""
        signal = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'rule_id': 999,
            'rule_name': 'NQ Stats Pattern Signal',
            'description': 'High-confidence signal based on 10-year NQ statistical patterns',
            'action_type': nq_decision['primary_signal'],
            'position_size': 'moderate' if nq_decision['confidence'] < 0.75 else 'aggressive',
            'stop_loss_pct': 2.0,
            'take_profit_pct': 6.0,
            'confidence': nq_decision['confidence'],
            'signal_strength': nq_decision['confidence'] * 100,
            'entry_strategy': nq_decision['entry_strategy'],
            'risk_management': nq_decision['risk_management'],
            'factors': nq_decision['supporting_factors'],
            'source': 'nqstats.com patterns'
        }
        
        return signal
    
    def display_signals(self, signals: List[Dict]):
        """Display trading signals"""
        if not signals:
            print("\nNo trading signals generated.")
            return
        
        for i, signal in enumerate(signals, 1):
            print(f"\nSignal #{i}: {signal['rule_name']}")
            print(f"  Action: {signal['action_type']}")
            print(f"  Position Size: {signal['position_size']}")
            print(f"  Stop Loss: {signal['stop_loss_pct']}%")
            print(f"  Take Profit: {signal['take_profit_pct']}%")
            print(f"  Confidence: {signal['confidence']:.1%}")
            print(f"  Signal Strength: {signal['signal_strength']:.1f}/100")
            print(f"  Description: {signal['description']}")
            
            # Display NQ Stats specific information
            if 'entry_strategy' in signal and signal.get('source') == 'nqstats.com patterns':
                print(f"  Entry Strategy: {signal['entry_strategy']}")
                if 'risk_management' in signal:
                    print("  Risk Management:")
                    for key, value in signal['risk_management'].items():
                        print(f"    - {key.replace('_', ' ').title()}: {value}")
    
    def save_signals(self, signals: List[Dict], output_file: str):
        """Save trading signals to JSON file"""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(signals, f, indent=4)
    
    def add_custom_rule(self, rule: Dict):
        """Add a custom trading rule"""
        self.rules.append(rule)
        self._save_rules()
    
    def _save_rules(self):
        """Save current rules to file"""
        with open(self.rules_file, 'w') as f:
            json.dump(self.rules, f, indent=4)
