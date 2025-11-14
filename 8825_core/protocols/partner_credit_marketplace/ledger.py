#!/usr/bin/env python3
"""
Partner Credit Marketplace - Multi-Partner Ledger
Tracks credit balances across multiple partner pairs
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Configuration
LEDGER_DIR = Path(__file__).parent / "data"
LEDGER_FILE = LEDGER_DIR / "multi_partner_ledger.json"

# Ensure data directory exists
LEDGER_DIR.mkdir(parents=True, exist_ok=True)


class CreditLedger:
    """Multi-partner credit ledger system"""
    
    def __init__(self):
        self.ledger = self._load_ledger()
    
    def _load_ledger(self) -> dict:
        """Load ledger from disk"""
        if LEDGER_FILE.exists():
            with open(LEDGER_FILE, 'r') as f:
                return json.load(f)
        
        # Initialize new ledger
        return {
            "version": "3.0.0",
            "created": datetime.now().isoformat(),
            "partners": {},
            "transactions": [],
            "balances": {}
        }
    
    def _save_ledger(self):
        """Save ledger to disk"""
        with open(LEDGER_FILE, 'w') as f:
            json.dump(self.ledger, f, indent=2)
    
    def add_partner(self, partner_id: str, name: str, contact: str):
        """Register a new partner"""
        if partner_id in self.ledger["partners"]:
            raise ValueError(f"Partner {partner_id} already exists")
        
        self.ledger["partners"][partner_id] = {
            "name": name,
            "contact": contact,
            "joined": datetime.now().isoformat(),
            "active": True
        }
        self._save_ledger()
    
    def get_partner_pair_key(self, partner_a: str, partner_b: str) -> str:
        """Get consistent key for partner pair"""
        return f"{min(partner_a, partner_b)}:{max(partner_a, partner_b)}"
    
    def record_transaction(
        self,
        from_partner: str,
        to_partner: str,
        credits: float,
        work_order_id: str,
        description: str,
        skill_multiplier: float = 1.0
    ):
        """Record a credit transaction"""
        # Validate partners exist
        if from_partner not in self.ledger["partners"]:
            raise ValueError(f"Partner {from_partner} not found")
        if to_partner not in self.ledger["partners"]:
            raise ValueError(f"Partner {to_partner} not found")
        
        # Calculate adjusted credits
        adjusted_credits = credits * skill_multiplier
        
        # Create transaction
        transaction = {
            "id": f"TXN-{len(self.ledger['transactions']) + 1:04d}",
            "timestamp": datetime.now().isoformat(),
            "from": from_partner,
            "to": to_partner,
            "credits": credits,
            "skill_multiplier": skill_multiplier,
            "adjusted_credits": adjusted_credits,
            "work_order_id": work_order_id,
            "description": description,
            "expiry": (datetime.now() + timedelta(days=18*30)).isoformat()
        }
        
        self.ledger["transactions"].append(transaction)
        
        # Update balances
        pair_key = self.get_partner_pair_key(from_partner, to_partner)
        if pair_key not in self.ledger["balances"]:
            self.ledger["balances"][pair_key] = {
                "partner_a": min(from_partner, to_partner),
                "partner_b": max(from_partner, to_partner),
                "net_balance": 0.0,
                "total_volume": 0.0
            }
        
        balance = self.ledger["balances"][pair_key]
        
        # Update net balance (positive = partner_a owes partner_b)
        if from_partner == balance["partner_a"]:
            balance["net_balance"] += adjusted_credits
        else:
            balance["net_balance"] -= adjusted_credits
        
        balance["total_volume"] += adjusted_credits
        
        self._save_ledger()
        return transaction
    
    def get_balance(self, partner_a: str, partner_b: str) -> dict:
        """Get balance between two partners"""
        pair_key = self.get_partner_pair_key(partner_a, partner_b)
        
        if pair_key not in self.ledger["balances"]:
            return {
                "partner_a": partner_a,
                "partner_b": partner_b,
                "net_balance": 0.0,
                "total_volume": 0.0,
                "status": "balanced"
            }
        
        balance = self.ledger["balances"][pair_key].copy()
        
        # Determine status
        net = abs(balance["net_balance"])
        if net == 0:
            balance["status"] = "balanced"
        elif net / balance["total_volume"] > 0.15:
            balance["status"] = "needs_trueup"
        else:
            balance["status"] = "normal"
        
        return balance
    
    def get_all_balances(self) -> List[dict]:
        """Get all partner pair balances"""
        balances = []
        for pair_key, balance in self.ledger["balances"].items():
            balance_copy = balance.copy()
            
            # Add status
            net = abs(balance_copy["net_balance"])
            if net == 0:
                balance_copy["status"] = "balanced"
            elif balance_copy["total_volume"] > 0 and net / balance_copy["total_volume"] > 0.15:
                balance_copy["status"] = "needs_trueup"
            else:
                balance_copy["status"] = "normal"
            
            balances.append(balance_copy)
        
        return balances
    
    def get_partner_summary(self, partner_id: str) -> dict:
        """Get summary of all balances for a partner"""
        if partner_id not in self.ledger["partners"]:
            raise ValueError(f"Partner {partner_id} not found")
        
        summary = {
            "partner_id": partner_id,
            "partner_name": self.ledger["partners"][partner_id]["name"],
            "balances": [],
            "total_credits_earned": 0.0,
            "total_credits_spent": 0.0
        }
        
        # Calculate from transactions
        for txn in self.ledger["transactions"]:
            if txn["to"] == partner_id:
                summary["total_credits_earned"] += txn["adjusted_credits"]
            elif txn["from"] == partner_id:
                summary["total_credits_spent"] += txn["adjusted_credits"]
        
        # Get all balances involving this partner
        for pair_key, balance in self.ledger["balances"].items():
            if partner_id in [balance["partner_a"], balance["partner_b"]]:
                balance_copy = balance.copy()
                
                # Flip perspective if needed
                if partner_id == balance["partner_b"]:
                    balance_copy["net_balance"] *= -1
                    balance_copy["other_partner"] = balance["partner_a"]
                else:
                    balance_copy["other_partner"] = balance["partner_b"]
                
                summary["balances"].append(balance_copy)
        
        summary["net_position"] = summary["total_credits_earned"] - summary["total_credits_spent"]
        
        return summary
    
    def get_expiring_credits(self, days: int = 30) -> List[dict]:
        """Get credits expiring within specified days"""
        cutoff = datetime.now() + timedelta(days=days)
        expiring = []
        
        for txn in self.ledger["transactions"]:
            expiry = datetime.fromisoformat(txn["expiry"])
            if expiry <= cutoff:
                days_until_expiry = (expiry - datetime.now()).days
                expiring.append({
                    **txn,
                    "days_until_expiry": days_until_expiry
                })
        
        return sorted(expiring, key=lambda x: x["days_until_expiry"])


def main():
    """CLI for ledger management"""
    import sys
    
    ledger = CreditLedger()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  ledger.py add-partner <id> <name> <contact>")
        print("  ledger.py record <from> <to> <credits> <wo_id> <description> [multiplier]")
        print("  ledger.py balance <partner_a> <partner_b>")
        print("  ledger.py summary <partner_id>")
        print("  ledger.py balances")
        print("  ledger.py expiring [days]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add-partner":
        partner_id, name, contact = sys.argv[2:5]
        ledger.add_partner(partner_id, name, contact)
        print(f"✓ Added partner: {name} ({partner_id})")
    
    elif command == "record":
        from_p, to_p, credits, wo_id, desc = sys.argv[2:7]
        multiplier = float(sys.argv[7]) if len(sys.argv) > 7 else 1.0
        txn = ledger.record_transaction(from_p, to_p, float(credits), wo_id, desc, multiplier)
        print(f"✓ Recorded transaction: {txn['id']}")
        print(f"  {from_p} → {to_p}: {credits} credits (×{multiplier} = {txn['adjusted_credits']})")
    
    elif command == "balance":
        partner_a, partner_b = sys.argv[2:4]
        balance = ledger.get_balance(partner_a, partner_b)
        print(f"Balance between {partner_a} and {partner_b}:")
        print(f"  Net: {balance['net_balance']:.1f} credits")
        print(f"  Volume: {balance['total_volume']:.1f} credits")
        print(f"  Status: {balance['status']}")
    
    elif command == "summary":
        partner_id = sys.argv[2]
        summary = ledger.get_partner_summary(partner_id)
        print(f"Summary for {summary['partner_name']} ({partner_id}):")
        print(f"  Credits earned: {summary['total_credits_earned']:.1f}")
        print(f"  Credits spent: {summary['total_credits_spent']:.1f}")
        print(f"  Net position: {summary['net_position']:.1f}")
        print(f"\n  Balances with other partners:")
        for bal in summary['balances']:
            print(f"    {bal['other_partner']}: {bal['net_balance']:.1f} credits")
    
    elif command == "balances":
        balances = ledger.get_all_balances()
        print(f"All partner balances ({len(balances)} pairs):")
        for bal in balances:
            print(f"  {bal['partner_a']} ↔ {bal['partner_b']}: {bal['net_balance']:.1f} credits ({bal['status']})")
    
    elif command == "expiring":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        expiring = ledger.get_expiring_credits(days)
        print(f"Credits expiring in next {days} days ({len(expiring)} transactions):")
        for txn in expiring:
            print(f"  {txn['id']}: {txn['adjusted_credits']:.1f} credits in {txn['days_until_expiry']} days")
            print(f"    {txn['from']} → {txn['to']}: {txn['description']}")


if __name__ == "__main__":
    main()
