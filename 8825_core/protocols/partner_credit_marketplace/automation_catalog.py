#!/usr/bin/env python3
"""
Partner Credit Marketplace - Automation Catalog
Browse and license automations built by partners
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# Configuration
CATALOG_DIR = Path(__file__).parent / "data"
CATALOG_FILE = CATALOG_DIR / "automation_catalog.json"
LICENSES_FILE = CATALOG_DIR / "licenses.json"

# Ensure data directory exists
CATALOG_DIR.mkdir(parents=True, exist_ok=True)


class AutomationCatalog:
    """Automation catalog and licensing system"""
    
    def __init__(self):
        self.catalog = self._load_catalog()
        self.licenses = self._load_licenses()
    
    def _load_catalog(self) -> dict:
        """Load catalog from disk"""
        if CATALOG_FILE.exists():
            with open(CATALOG_FILE, 'r') as f:
                return json.load(f)
        
        return {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "automations": []
        }
    
    def _load_licenses(self) -> dict:
        """Load licenses from disk"""
        if LICENSES_FILE.exists():
            with open(LICENSES_FILE, 'r') as f:
                return json.load(f)
        
        return {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "licenses": []
        }
    
    def _save_catalog(self):
        """Save catalog to disk"""
        with open(CATALOG_FILE, 'w') as f:
            json.dump(self.catalog, f, indent=2)
    
    def _save_licenses(self):
        """Save licenses to disk"""
        with open(LICENSES_FILE, 'w') as f:
            json.dump(self.licenses, f, indent=2)
    
    def add_automation(
        self,
        name: str,
        description: str,
        builder: str,
        category: str,
        tags: List[str],
        internal_use: bool = True,
        external_license_available: bool = False,
        license_price_credits: Optional[float] = None,
        revenue_split: str = "80/20"
    ) -> dict:
        """Add automation to catalog"""
        automation = {
            "id": f"AUTO-{len(self.catalog['automations']) + 1:04d}",
            "name": name,
            "description": description,
            "builder": builder,
            "category": category,
            "tags": tags,
            "created": datetime.now().isoformat(),
            "internal_use": internal_use,
            "external_license_available": external_license_available,
            "license_price_credits": license_price_credits,
            "revenue_split": revenue_split,
            "usage_count": 0,
            "license_count": 0,
            "total_revenue": 0.0
        }
        
        self.catalog["automations"].append(automation)
        self._save_catalog()
        return automation
    
    def search_automations(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        builder: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[dict]:
        """Search automations in catalog"""
        results = self.catalog["automations"]
        
        if query:
            query_lower = query.lower()
            results = [
                a for a in results
                if query_lower in a["name"].lower() or query_lower in a["description"].lower()
            ]
        
        if category:
            results = [a for a in results if a["category"] == category]
        
        if builder:
            results = [a for a in results if a["builder"] == builder]
        
        if tags:
            results = [
                a for a in results
                if any(tag in a["tags"] for tag in tags)
            ]
        
        return results
    
    def get_automation(self, automation_id: str) -> Optional[dict]:
        """Get automation by ID"""
        for automation in self.catalog["automations"]:
            if automation["id"] == automation_id:
                return automation
        return None
    
    def license_automation(
        self,
        automation_id: str,
        licensee: str,
        license_type: str = "internal",
        price_credits: Optional[float] = None
    ) -> dict:
        """License an automation"""
        automation = self.get_automation(automation_id)
        if not automation:
            raise ValueError(f"Automation {automation_id} not found")
        
        # Internal use is free for partners
        if license_type == "internal":
            price_credits = 0.0
        elif price_credits is None:
            price_credits = automation.get("license_price_credits", 0.0)
        
        # Create license
        license_record = {
            "id": f"LIC-{len(self.licenses['licenses']) + 1:04d}",
            "automation_id": automation_id,
            "automation_name": automation["name"],
            "licensee": licensee,
            "builder": automation["builder"],
            "license_type": license_type,
            "price_credits": price_credits,
            "issued": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.licenses["licenses"].append(license_record)
        
        # Update automation stats
        automation["license_count"] += 1
        if price_credits > 0:
            automation["total_revenue"] += price_credits
        
        self._save_catalog()
        self._save_licenses()
        
        return license_record
    
    def get_builder_stats(self, builder: str) -> dict:
        """Get statistics for a builder"""
        automations = [a for a in self.catalog["automations"] if a["builder"] == builder]
        
        stats = {
            "builder": builder,
            "total_automations": len(automations),
            "total_licenses": sum(a["license_count"] for a in automations),
            "total_revenue": sum(a["total_revenue"] for a in automations),
            "categories": {}
        }
        
        # Count by category
        for auto in automations:
            cat = auto["category"]
            if cat not in stats["categories"]:
                stats["categories"][cat] = 0
            stats["categories"][cat] += 1
        
        return stats
    
    def get_licensee_automations(self, licensee: str) -> List[dict]:
        """Get all automations licensed by a partner"""
        return [
            lic for lic in self.licenses["licenses"]
            if lic["licensee"] == licensee and lic["status"] == "active"
        ]
    
    def calculate_revenue_distribution(self, automation_id: str) -> dict:
        """Calculate revenue distribution for an automation"""
        automation = self.get_automation(automation_id)
        if not automation:
            raise ValueError(f"Automation {automation_id} not found")
        
        total_revenue = automation["total_revenue"]
        split = automation["revenue_split"]
        
        # Parse split (e.g., "80/20")
        if "/" in split:
            builder_pct, requester_pct = map(int, split.split("/"))
        else:
            builder_pct, requester_pct = 100, 0
        
        return {
            "automation_id": automation_id,
            "total_revenue": total_revenue,
            "builder": automation["builder"],
            "builder_share": total_revenue * (builder_pct / 100),
            "requester_share": total_revenue * (requester_pct / 100),
            "split": split
        }


def main():
    """CLI for automation catalog"""
    import sys
    
    catalog = AutomationCatalog()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  catalog.py add <name> <description> <builder> <category> <tags>")
        print("  catalog.py search [query]")
        print("  catalog.py license <auto_id> <licensee> [type] [price]")
        print("  catalog.py stats <builder>")
        print("  catalog.py licenses <licensee>")
        print("  catalog.py revenue <auto_id>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add":
        name, desc, builder, category = sys.argv[2:6]
        tags = sys.argv[6].split(",") if len(sys.argv) > 6 else []
        auto = catalog.add_automation(name, desc, builder, category, tags)
        print(f"✓ Added automation: {auto['id']} - {name}")
    
    elif command == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else None
        results = catalog.search_automations(query=query)
        print(f"Found {len(results)} automations:")
        for auto in results:
            print(f"  {auto['id']}: {auto['name']} ({auto['category']})")
            print(f"    Builder: {auto['builder']}")
            print(f"    Licenses: {auto['license_count']}, Revenue: {auto['total_revenue']:.1f} credits")
    
    elif command == "license":
        auto_id, licensee = sys.argv[2:4]
        lic_type = sys.argv[4] if len(sys.argv) > 4 else "internal"
        price = float(sys.argv[5]) if len(sys.argv) > 5 else None
        lic = catalog.license_automation(auto_id, licensee, lic_type, price)
        print(f"✓ Licensed automation: {lic['id']}")
        print(f"  {auto_id} → {licensee}")
        print(f"  Type: {lic_type}, Price: {lic['price_credits']:.1f} credits")
    
    elif command == "stats":
        builder = sys.argv[2]
        stats = catalog.get_builder_stats(builder)
        print(f"Stats for {builder}:")
        print(f"  Automations: {stats['total_automations']}")
        print(f"  Licenses: {stats['total_licenses']}")
        print(f"  Revenue: {stats['total_revenue']:.1f} credits")
        print(f"  Categories: {stats['categories']}")
    
    elif command == "licenses":
        licensee = sys.argv[2]
        licenses = catalog.get_licensee_automations(licensee)
        print(f"Automations licensed by {licensee} ({len(licenses)}):")
        for lic in licenses:
            print(f"  {lic['id']}: {lic['automation_name']}")
            print(f"    Builder: {lic['builder']}, Type: {lic['license_type']}")
    
    elif command == "revenue":
        auto_id = sys.argv[2]
        dist = catalog.calculate_revenue_distribution(auto_id)
        print(f"Revenue distribution for {auto_id}:")
        print(f"  Total: {dist['total_revenue']:.1f} credits")
        print(f"  Builder ({dist['builder']}): {dist['builder_share']:.1f} credits")
        print(f"  Requester: {dist['requester_share']:.1f} credits")
        print(f"  Split: {dist['split']}")


if __name__ == "__main__":
    main()
