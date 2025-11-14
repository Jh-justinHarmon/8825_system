#!/usr/bin/env python3
"""
Partner Credit Marketplace - Unified CLI
Single interface for ledger, catalog, and governance
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ledger import CreditLedger
from automation_catalog import AutomationCatalog
from governance import GovernanceSystem


def print_menu():
    """Print main menu"""
    print("\n" + "="*60)
    print("PARTNER CREDIT MARKETPLACE")
    print("="*60)
    print("\n📊 LEDGER")
    print("  1. Add partner")
    print("  2. Record transaction")
    print("  3. View balance")
    print("  4. View all balances")
    print("  5. Partner summary")
    print("  6. Expiring credits")
    print("\n🤖 AUTOMATION CATALOG")
    print("  7. Add automation")
    print("  8. Search automations")
    print("  9. License automation")
    print(" 10. Builder stats")
    print(" 11. My licenses")
    print("\n🗳️  GOVERNANCE")
    print(" 12. Create proposal")
    print(" 13. Cast vote")
    print(" 14. View proposal")
    print(" 15. Open proposals")
    print(" 16. Voting record")
    print("\n 0. Exit")
    print("="*60)


def ledger_menu(ledger: CreditLedger):
    """Ledger submenu"""
    choice = input("\nLedger action (1-6): ").strip()
    
    if choice == "1":
        partner_id = input("Partner ID: ").strip()
        name = input("Name: ").strip()
        contact = input("Contact: ").strip()
        ledger.add_partner(partner_id, name, contact)
        print(f"✓ Added partner: {name}")
    
    elif choice == "2":
        from_p = input("From partner: ").strip()
        to_p = input("To partner: ").strip()
        credits = float(input("Credits: ").strip())
        wo_id = input("Work order ID: ").strip()
        desc = input("Description: ").strip()
        multiplier = float(input("Skill multiplier (default 1.0): ").strip() or "1.0")
        
        txn = ledger.record_transaction(from_p, to_p, credits, wo_id, desc, multiplier)
        print(f"✓ Recorded: {txn['id']} - {credits} credits (×{multiplier} = {txn['adjusted_credits']})")
    
    elif choice == "3":
        partner_a = input("Partner A: ").strip()
        partner_b = input("Partner B: ").strip()
        balance = ledger.get_balance(partner_a, partner_b)
        print(f"\nBalance: {balance['net_balance']:.1f} credits")
        print(f"Volume: {balance['total_volume']:.1f} credits")
        print(f"Status: {balance['status']}")
    
    elif choice == "4":
        balances = ledger.get_all_balances()
        print(f"\nAll balances ({len(balances)} pairs):")
        for bal in balances:
            print(f"  {bal['partner_a']} ↔ {bal['partner_b']}: {bal['net_balance']:.1f} credits ({bal['status']})")
    
    elif choice == "5":
        partner_id = input("Partner ID: ").strip()
        summary = ledger.get_partner_summary(partner_id)
        print(f"\nSummary for {summary['partner_name']}:")
        print(f"  Earned: {summary['total_credits_earned']:.1f} credits")
        print(f"  Spent: {summary['total_credits_spent']:.1f} credits")
        print(f"  Net: {summary['net_position']:.1f} credits")
    
    elif choice == "6":
        days = int(input("Days ahead (default 30): ").strip() or "30")
        expiring = ledger.get_expiring_credits(days)
        print(f"\nExpiring in {days} days ({len(expiring)} transactions):")
        for txn in expiring[:10]:  # Show first 10
            print(f"  {txn['id']}: {txn['adjusted_credits']:.1f} credits in {txn['days_until_expiry']} days")


def catalog_menu(catalog: AutomationCatalog):
    """Catalog submenu"""
    choice = input("\nCatalog action (7-11): ").strip()
    
    if choice == "7":
        name = input("Automation name: ").strip()
        desc = input("Description: ").strip()
        builder = input("Builder: ").strip()
        category = input("Category: ").strip()
        tags = input("Tags (comma-separated): ").strip().split(",")
        
        auto = catalog.add_automation(name, desc, builder, category, tags)
        print(f"✓ Added: {auto['id']} - {name}")
    
    elif choice == "8":
        query = input("Search query (or Enter for all): ").strip() or None
        results = catalog.search_automations(query=query)
        print(f"\nFound {len(results)} automations:")
        for auto in results[:10]:  # Show first 10
            print(f"  {auto['id']}: {auto['name']} ({auto['category']})")
            print(f"    Builder: {auto['builder']}, Licenses: {auto['license_count']}")
    
    elif choice == "9":
        auto_id = input("Automation ID: ").strip()
        licensee = input("Licensee: ").strip()
        lic_type = input("Type (internal/external, default internal): ").strip() or "internal"
        
        lic = catalog.license_automation(auto_id, licensee, lic_type)
        print(f"✓ Licensed: {lic['id']} - {lic['automation_name']} to {licensee}")
    
    elif choice == "10":
        builder = input("Builder: ").strip()
        stats = catalog.get_builder_stats(builder)
        print(f"\nStats for {builder}:")
        print(f"  Automations: {stats['total_automations']}")
        print(f"  Licenses: {stats['total_licenses']}")
        print(f"  Revenue: {stats['total_revenue']:.1f} credits")
    
    elif choice == "11":
        licensee = input("Licensee: ").strip()
        licenses = catalog.get_licensee_automations(licensee)
        print(f"\nLicenses for {licensee} ({len(licenses)}):")
        for lic in licenses[:10]:  # Show first 10
            print(f"  {lic['automation_name']} (from {lic['builder']})")


def governance_menu(gov: GovernanceSystem):
    """Governance submenu"""
    choice = input("\nGovernance action (12-16): ").strip()
    
    if choice == "12":
        title = input("Proposal title: ").strip()
        desc = input("Description: ").strip()
        proposer = input("Proposer: ").strip()
        prop_type = input("Type: ").strip()
        days = int(input("Voting period (days, default 7): ").strip() or "7")
        
        proposal = gov.create_proposal(title, desc, proposer, prop_type, days)
        print(f"✓ Created: {proposal['id']} - {title}")
    
    elif choice == "13":
        prop_id = input("Proposal ID: ").strip()
        voter = input("Voter: ").strip()
        vote = input("Vote (for/against/abstain): ").strip()
        comment = input("Comment (optional): ").strip() or None
        
        proposal = gov.cast_vote(prop_id, voter, vote, comment)
        print(f"✓ Vote cast on {prop_id}")
        print(f"  Tally: {proposal['votes_for']} for, {proposal['votes_against']} against")
    
    elif choice == "14":
        prop_id = input("Proposal ID: ").strip()
        proposal = gov.get_proposal(prop_id)
        if proposal:
            print(f"\n{proposal['id']}: {proposal['title']}")
            print(f"  Status: {proposal['status']}")
            print(f"  Votes: {proposal['votes_for']} for, {proposal['votes_against']} against")
        else:
            print("Proposal not found")
    
    elif choice == "15":
        proposals = gov.get_open_proposals()
        print(f"\nOpen proposals ({len(proposals)}):")
        for prop in proposals:
            print(f"  {prop['id']}: {prop['title']}")
            print(f"    Deadline: {prop['voting_deadline']}")
    
    elif choice == "16":
        partner = input("Partner: ").strip()
        record = gov.get_partner_voting_record(partner)
        print(f"\nVoting record for {partner}:")
        print(f"  Total votes: {record['total_votes']}")
        print(f"  Participation: {record['participation_rate']:.1%}")


def main():
    """Main CLI loop"""
    ledger = CreditLedger()
    catalog = AutomationCatalog()
    gov = GovernanceSystem()
    
    print("\n🚀 Welcome to Partner Credit Marketplace!")
    
    while True:
        print_menu()
        choice = input("\nSelect action (0-16): ").strip()
        
        if choice == "0":
            print("\n✓ Goodbye!")
            break
        
        try:
            if choice in ["1", "2", "3", "4", "5", "6"]:
                ledger_menu(ledger)
            elif choice in ["7", "8", "9", "10", "11"]:
                catalog_menu(catalog)
            elif choice in ["12", "13", "14", "15", "16"]:
                governance_menu(gov)
            else:
                print("Invalid choice")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
