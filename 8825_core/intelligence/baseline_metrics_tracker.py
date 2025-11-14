#!/usr/bin/env python3
"""
Baseline Metrics Tracker
Analyzes current LLM usage across the 8825 system to establish baseline before LLOM Router
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict

class BaselineMetricsTracker:
    """
    Tracks current LLM usage to establish baseline metrics
    """
    
    def __init__(self):
        self.system_root = Path(__file__).parent.parent.parent
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'systems_analyzed': [],
            'llm_calls_found': [],
            'estimated_usage': {},
            'cost_projections': {},
            'baseline_summary': {}
        }
    
    def analyze_codebase(self):
        """Scan codebase for LLM usage"""
        
        print("🔍 Scanning codebase for LLM usage...\n")
        
        # Systems to analyze
        systems = {
            'content_index': self.system_root / '8825_core' / 'content_index',
            'brain': self.system_root / '8825_core' / 'brain',
            'workflows': self.system_root / '8825_core' / 'workflows',
            'integrations': self.system_root / '8825_core' / 'integrations',
        }
        
        for system_name, system_path in systems.items():
            if system_path.exists():
                print(f"📂 Analyzing {system_name}...")
                self._analyze_system(system_name, system_path)
        
        # Calculate totals
        self._calculate_baseline()
        
        return self.results
    
    def _analyze_system(self, system_name: str, system_path: Path):
        """Analyze a specific system for LLM calls"""
        
        # Find Python files
        py_files = list(system_path.glob('**/*.py'))
        
        for py_file in py_files:
            try:
                content = py_file.read_text()
                
                # Look for OpenAI calls
                openai_calls = self._find_openai_calls(content, py_file)
                if openai_calls:
                    self.results['llm_calls_found'].extend(openai_calls)
                
                # Look for Anthropic calls
                anthropic_calls = self._find_anthropic_calls(content, py_file)
                if anthropic_calls:
                    self.results['llm_calls_found'].extend(anthropic_calls)
                    
            except Exception as e:
                print(f"  ⚠️  Error reading {py_file.name}: {e}")
        
        self.results['systems_analyzed'].append(system_name)
    
    def _find_openai_calls(self, content: str, file_path: Path) -> List[Dict]:
        """Find OpenAI API calls in code"""
        
        calls = []
        
        # Pattern: client.chat.completions.create
        pattern = r'client\.chat\.completions\.create\s*\('
        matches = re.finditer(pattern, content)
        
        for match in matches:
            # Extract context around the call
            start = max(0, match.start() - 200)
            end = min(len(content), match.end() + 500)
            context = content[start:end]
            
            # Try to extract model
            model_match = re.search(r'model\s*=\s*["\']([^"\']+)["\']', context)
            model = model_match.group(1) if model_match else 'unknown'
            
            # Try to extract max_tokens
            tokens_match = re.search(r'max_tokens\s*=\s*(\d+)', context)
            max_tokens = int(tokens_match.group(1)) if tokens_match else 4096
            
            calls.append({
                'file': str(file_path.relative_to(self.system_root)),
                'provider': 'openai',
                'model': model,
                'max_tokens': max_tokens,
                'line': content[:match.start()].count('\n') + 1
            })
        
        return calls
    
    def _find_anthropic_calls(self, content: str, file_path: Path) -> List[Dict]:
        """Find Anthropic API calls in code"""
        
        calls = []
        
        # Pattern: anthropic.messages.create
        pattern = r'anthropic\.messages\.create\s*\('
        matches = re.finditer(pattern, content)
        
        for match in matches:
            # Extract context
            start = max(0, match.start() - 200)
            end = min(len(content), match.end() + 500)
            context = content[start:end]
            
            # Try to extract model
            model_match = re.search(r'model\s*=\s*["\']([^"\']+)["\']', context)
            model = model_match.group(1) if model_match else 'unknown'
            
            # Try to extract max_tokens
            tokens_match = re.search(r'max_tokens\s*=\s*(\d+)', context)
            max_tokens = int(tokens_match.group(1)) if tokens_match else 4096
            
            calls.append({
                'file': str(file_path.relative_to(self.system_root)),
                'provider': 'anthropic',
                'model': model,
                'max_tokens': max_tokens,
                'line': content[:match.start()].count('\n') + 1
            })
        
        return calls
    
    def _calculate_baseline(self):
        """Calculate baseline usage and costs"""
        
        # Group by system
        by_system = defaultdict(list)
        for call in self.results['llm_calls_found']:
            system = call['file'].split('/')[0]
            by_system[system].append(call)
        
        # Estimate usage per system
        usage_estimates = {
            'content_index': {
                'files_per_month': 10000,  # 10k files processed
                'calls_per_file': 2,  # naming + similarity check
                'model': 'gpt-4o-mini',
                'avg_tokens_per_call': 500
            },
            'brain': {
                'calls_per_month': 50,  # weekly + ad-hoc
                'model': 'gpt-4o',
                'avg_tokens_per_call': 2000
            },
            'workflows': {
                'calls_per_month': 500,  # various workflows
                'model': 'gpt-4o-mini',
                'avg_tokens_per_call': 1000
            }
        }
        
        # Cost per million tokens
        costs = {
            'gpt-4o-mini': 0.15,
            'gpt-4o': 2.50,
            'claude-sonnet-4': 3.00
        }
        
        # Calculate costs
        total_monthly_cost = 0
        
        for system, estimates in usage_estimates.items():
            if 'files_per_month' in estimates:
                total_calls = estimates['files_per_month'] * estimates['calls_per_file']
            else:
                total_calls = estimates['calls_per_month']
            
            total_tokens = total_calls * estimates['avg_tokens_per_call']
            cost_per_million = costs.get(estimates['model'], 2.50)
            monthly_cost = (total_tokens / 1_000_000) * cost_per_million
            
            self.results['estimated_usage'][system] = {
                'calls_per_month': total_calls,
                'tokens_per_month': total_tokens,
                'model': estimates['model'],
                'monthly_cost': round(monthly_cost, 2)
            }
            
            total_monthly_cost += monthly_cost
        
        # Summary
        self.results['baseline_summary'] = {
            'total_monthly_cost': round(total_monthly_cost, 2),
            'total_annual_cost': round(total_monthly_cost * 12, 2),
            'llm_calls_found': len(self.results['llm_calls_found']),
            'systems_with_llm': len(by_system),
            'primary_model': 'gpt-4o-mini',
            'expensive_model_usage': sum(1 for c in self.results['llm_calls_found'] if 'gpt-4o' in c['model'] and 'mini' not in c['model'])
        }
        
        # Projected savings with LLOM Router
        self.results['cost_projections'] = {
            'current_monthly': round(total_monthly_cost, 2),
            'with_llom_router': round(total_monthly_cost * 0.13, 2),  # 87% reduction
            'monthly_savings': round(total_monthly_cost * 0.87, 2),
            'annual_savings': round(total_monthly_cost * 0.87 * 12, 2),
            'savings_percent': 87
        }
    
    def print_report(self):
        """Print baseline metrics report"""
        
        print("\n" + "="*70)
        print("📊 BASELINE METRICS REPORT")
        print("="*70 + "\n")
        
        # LLM Calls Found
        print(f"🔍 LLM Calls Found: {len(self.results['llm_calls_found'])}\n")
        
        by_file = defaultdict(list)
        for call in self.results['llm_calls_found']:
            by_file[call['file']].append(call)
        
        for file, calls in sorted(by_file.items()):
            print(f"  📄 {file}")
            for call in calls:
                print(f"     Line {call['line']}: {call['provider']} - {call['model']} (max {call['max_tokens']} tokens)")
        
        print("\n" + "-"*70 + "\n")
        
        # Estimated Usage
        print("📈 ESTIMATED MONTHLY USAGE:\n")
        
        for system, usage in self.results['estimated_usage'].items():
            print(f"  {system}:")
            print(f"    Calls: {usage['calls_per_month']:,}")
            print(f"    Tokens: {usage['tokens_per_month']:,}")
            print(f"    Model: {usage['model']}")
            print(f"    Cost: ${usage['monthly_cost']:.2f}/month")
            print()
        
        print("-"*70 + "\n")
        
        # Baseline Summary
        summary = self.results['baseline_summary']
        print("💰 BASELINE SUMMARY:\n")
        print(f"  Total Monthly Cost: ${summary['total_monthly_cost']:.2f}")
        print(f"  Total Annual Cost: ${summary['total_annual_cost']:.2f}")
        print(f"  LLM Calls Found: {summary['llm_calls_found']}")
        print(f"  Systems with LLM: {summary['systems_with_llm']}")
        print(f"  Primary Model: {summary['primary_model']}")
        print(f"  Expensive Model Usage: {summary['expensive_model_usage']} calls")
        
        print("\n" + "-"*70 + "\n")
        
        # Projections
        proj = self.results['cost_projections']
        print("🎯 PROJECTED SAVINGS WITH LLOM ROUTER:\n")
        print(f"  Current Monthly: ${proj['current_monthly']:.2f}")
        print(f"  With LLOM Router: ${proj['with_llom_router']:.2f}")
        print(f"  Monthly Savings: ${proj['monthly_savings']:.2f} ({proj['savings_percent']}%)")
        print(f"  Annual Savings: ${proj['annual_savings']:.2f}")
        
        print("\n" + "="*70 + "\n")
    
    def save_report(self, output_path: Path = None):
        """Save report to JSON"""
        
        if output_path is None:
            output_path = Path(__file__).parent / 'baseline_metrics.json'
        
        output_path.write_text(json.dumps(self.results, indent=2))
        print(f"💾 Report saved to: {output_path}")


def main():
    """Run baseline metrics analysis"""
    
    tracker = BaselineMetricsTracker()
    tracker.analyze_codebase()
    tracker.print_report()
    tracker.save_report()
    
    return tracker.results


if __name__ == '__main__':
    main()
