#!/usr/bin/env python3
"""
Partner Forge - Gamified Partner Credit Marketplace
Forge partnerships through collaborative work and automation
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

from ledger import CreditLedger
from automation_catalog import AutomationCatalog
from governance import GovernanceSystem

# Configuration
GAME_DIR = Path(__file__).parent / "data"
ACHIEVEMENTS_FILE = GAME_DIR / "achievements.json"
LEADERBOARD_FILE = GAME_DIR / "leaderboard.json"
QUESTS_FILE = GAME_DIR / "quests.json"

GAME_DIR.mkdir(parents=True, exist_ok=True)


class PartnerForge:
    """Game engine for Partner Forge"""
    
    # Achievement definitions
    ACHIEVEMENTS = {
        "first_blood": {
            "name": "First Blood",
            "description": "Complete your first transaction",
            "icon": "🎯",
            "points": 10
        },
        "automation_pioneer": {
            "name": "Automation Pioneer",
            "description": "Build your first automation",
            "icon": "🤖",
            "points": 25
        },
        "license_lord": {
            "name": "License Lord",
            "description": "License your first automation to another partner",
            "icon": "📜",
            "points": 50
        },
        "consensus_builder": {
            "name": "Consensus Builder",
            "description": "Get 3 proposals approved",
            "icon": "🤝",
            "points": 75
        },
        "perfect_balance": {
            "name": "Perfect Balance",
            "description": "Maintain ±5% balance for 30 days",
            "icon": "⚖️",
            "points": 100
        },
        "credit_whale": {
            "name": "Credit Whale",
            "description": "Earn 1000+ credits",
            "icon": "🐋",
            "points": 150
        },
        "automation_factory": {
            "name": "Automation Factory",
            "description": "Build 10 automations",
            "icon": "🏭",
            "points": 200
        },
        "governance_champion": {
            "name": "Governance Champion",
            "description": "Vote on 20 proposals",
            "icon": "🏆",
            "points": 100
        },
        "sprint_master": {
            "name": "Sprint Master",
            "description": "Complete 3 work orders in 7 days",
            "icon": "⚡",
            "points": 125
        },
        "innovation_bounty": {
            "name": "Innovation Bounty",
            "description": "Build automation worth 100+ credits in licensing",
            "icon": "💎",
            "points": 250
        }
    }
    
    def __init__(self):
        self.ledger = CreditLedger()
        self.catalog = AutomationCatalog()
        self.governance = GovernanceSystem()
        self.achievements = self._load_achievements()
        self.leaderboard = self._load_leaderboard()
        self.quests = self._load_quests()
    
    def _load_achievements(self) -> dict:
        """Load achievement progress"""
        if ACHIEVEMENTS_FILE.exists():
            with open(ACHIEVEMENTS_FILE, 'r') as f:
                return json.load(f)
        return {"players": {}}
    
    def _load_leaderboard(self) -> dict:
        """Load leaderboard data"""
        if LEADERBOARD_FILE.exists():
            with open(LEADERBOARD_FILE, 'r') as f:
                return json.load(f)
        return {"rankings": []}
    
    def _load_quests(self) -> dict:
        """Load active quests"""
        if QUESTS_FILE.exists():
            with open(QUESTS_FILE, 'r') as f:
                return json.load(f)
        return {"active_quests": []}
    
    def _save_achievements(self):
        """Save achievement progress"""
        with open(ACHIEVEMENTS_FILE, 'w') as f:
            json.dump(self.achievements, f, indent=2)
    
    def _save_leaderboard(self):
        """Save leaderboard"""
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(self.leaderboard, f, indent=2)
    
    def _save_quests(self):
        """Save quests"""
        with open(QUESTS_FILE, 'w') as f:
            json.dump(self.quests, f, indent=2)
    
    def check_achievements(self, player: str):
        """Check and award achievements for player"""
        if player not in self.achievements["players"]:
            self.achievements["players"][player] = {
                "unlocked": [],
                "total_points": 0
            }
        
        player_data = self.achievements["players"][player]
        newly_unlocked = []
        
        # Get player stats
        summary = self.ledger.get_partner_summary(player)
        builder_stats = self.catalog.get_builder_stats(player)
        voting_record = self.governance.get_partner_voting_record(player)
        
        # Check each achievement
        checks = {
            "first_blood": len(self.ledger.ledger["transactions"]) > 0,
            "automation_pioneer": builder_stats["total_automations"] >= 1,
            "license_lord": builder_stats["total_licenses"] >= 1,
            "consensus_builder": self._count_approved_proposals(player) >= 3,
            "credit_whale": summary["total_credits_earned"] >= 1000,
            "automation_factory": builder_stats["total_automations"] >= 10,
            "governance_champion": voting_record["total_votes"] >= 20,
            "innovation_bounty": self._has_high_value_automation(player, 100)
        }
        
        for achievement_id, unlocked in checks.items():
            if unlocked and achievement_id not in player_data["unlocked"]:
                achievement = self.ACHIEVEMENTS[achievement_id]
                player_data["unlocked"].append(achievement_id)
                player_data["total_points"] += achievement["points"]
                newly_unlocked.append(achievement)
        
        self._save_achievements()
        self._update_leaderboard()
        
        return newly_unlocked
    
    def _count_approved_proposals(self, player: str) -> int:
        """Count approved proposals by player"""
        return len([
            p for p in self.governance.proposals["proposals"]
            if p["proposer"] == player and p["status"] == "approved"
        ])
    
    def _has_high_value_automation(self, player: str, threshold: float) -> bool:
        """Check if player has automation worth threshold credits"""
        for auto in self.catalog.catalog["automations"]:
            if auto["builder"] == player and auto["total_revenue"] >= threshold:
                return True
        return False
    
    def _update_leaderboard(self):
        """Update leaderboard rankings"""
        rankings = []
        
        for player, data in self.achievements["players"].items():
            summary = self.ledger.get_partner_summary(player)
            builder_stats = self.catalog.get_builder_stats(player)
            
            rankings.append({
                "player": player,
                "total_points": data["total_points"],
                "achievements_unlocked": len(data["unlocked"]),
                "credits_earned": summary["total_credits_earned"],
                "automations_built": builder_stats["total_automations"],
                "licenses_issued": builder_stats["total_licenses"]
            })
        
        # Sort by total points
        rankings.sort(key=lambda x: x["total_points"], reverse=True)
        
        # Add ranks
        for i, ranking in enumerate(rankings, 1):
            ranking["rank"] = i
        
        self.leaderboard["rankings"] = rankings
        self._save_leaderboard()
    
    def create_quest(
        self,
        title: str,
        description: str,
        quest_type: str,
        target: int,
        reward_points: int,
        duration_days: int = 7
    ) -> dict:
        """Create a new quest/challenge"""
        quest = {
            "id": f"QUEST-{len(self.quests['active_quests']) + 1:04d}",
            "title": title,
            "description": description,
            "type": quest_type,
            "target": target,
            "reward_points": reward_points,
            "created": datetime.now().isoformat(),
            "expires": (datetime.now().timestamp() + duration_days * 86400),
            "participants": []
        }
        
        self.quests["active_quests"].append(quest)
        self._save_quests()
        return quest
    
    def get_player_dashboard(self, player: str) -> dict:
        """Get complete dashboard for player"""
        # Check for new achievements
        new_achievements = self.check_achievements(player)
        
        # Get player data
        player_data = self.achievements["players"].get(player, {
            "unlocked": [],
            "total_points": 0
        })
        
        summary = self.ledger.get_partner_summary(player)
        builder_stats = self.catalog.get_builder_stats(player)
        voting_record = self.governance.get_partner_voting_record(player)
        
        # Get rank
        rank = next(
            (r["rank"] for r in self.leaderboard["rankings"] if r["player"] == player),
            None
        )
        
        return {
            "player": player,
            "rank": rank,
            "total_points": player_data["total_points"],
            "achievements_unlocked": len(player_data["unlocked"]),
            "achievements_total": len(self.ACHIEVEMENTS),
            "new_achievements": new_achievements,
            "stats": {
                "credits_earned": summary["total_credits_earned"],
                "credits_spent": summary["total_credits_spent"],
                "net_position": summary["net_position"],
                "automations_built": builder_stats["total_automations"],
                "licenses_issued": builder_stats["total_licenses"],
                "total_revenue": builder_stats["total_revenue"],
                "votes_cast": voting_record["total_votes"],
                "participation_rate": voting_record["participation_rate"]
            },
            "active_quests": self._get_player_quests(player),
            "next_achievements": self._get_next_achievements(player)
        }
    
    def _get_player_quests(self, player: str) -> List[dict]:
        """Get active quests for player"""
        now = datetime.now().timestamp()
        return [
            q for q in self.quests["active_quests"]
            if q["expires"] > now
        ]
    
    def _get_next_achievements(self, player: str) -> List[dict]:
        """Get next 3 achievements player can unlock"""
        unlocked = self.achievements["players"].get(player, {}).get("unlocked", [])
        
        next_achievements = []
        for achievement_id, achievement in self.ACHIEVEMENTS.items():
            if achievement_id not in unlocked:
                next_achievements.append({
                    "id": achievement_id,
                    **achievement
                })
        
        return next_achievements[:3]
    
    def print_dashboard(self, player: str):
        """Print colorful dashboard"""
        dashboard = self.get_player_dashboard(player)
        
        print("\n" + "="*70)
        print(f"🔨 PARTNER FORGE - {player.upper()}")
        print("="*70)
        
        # Rank and points
        rank_emoji = "🥇" if dashboard["rank"] == 1 else "🥈" if dashboard["rank"] == 2 else "🥉" if dashboard["rank"] == 3 else "🎯"
        print(f"\n{rank_emoji} Rank: #{dashboard['rank']} | ⭐ Points: {dashboard['total_points']}")
        print(f"🏆 Achievements: {dashboard['achievements_unlocked']}/{dashboard['achievements_total']}")
        
        # New achievements
        if dashboard["new_achievements"]:
            print("\n🎉 NEW ACHIEVEMENTS UNLOCKED!")
            for ach in dashboard["new_achievements"]:
                print(f"  {ach['icon']} {ach['name']} (+{ach['points']} points)")
                print(f"     {ach['description']}")
        
        # Stats
        stats = dashboard["stats"]
        print("\n📊 STATS")
        print(f"  💰 Credits: {stats['credits_earned']:.0f} earned | {stats['credits_spent']:.0f} spent | {stats['net_position']:.0f} net")
        print(f"  🤖 Automations: {stats['automations_built']} built | {stats['licenses_issued']} licensed | {stats['total_revenue']:.0f} revenue")
        print(f"  🗳️  Governance: {stats['votes_cast']} votes | {stats['participation_rate']:.0%} participation")
        
        # Next achievements
        if dashboard["next_achievements"]:
            print("\n🎯 NEXT ACHIEVEMENTS")
            for ach in dashboard["next_achievements"]:
                print(f"  {ach['icon']} {ach['name']} ({ach['points']} points)")
                print(f"     {ach['description']}")
        
        # Active quests
        if dashboard["active_quests"]:
            print("\n⚡ ACTIVE QUESTS")
            for quest in dashboard["active_quests"]:
                print(f"  {quest['title']} ({quest['reward_points']} points)")
                print(f"     {quest['description']}")
        
        print("\n" + "="*70)


def main():
    """CLI for Partner Forge"""
    import sys
    
    game = PartnerForge()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  partner_forge.py dashboard <player>")
        print("  partner_forge.py leaderboard")
        print("  partner_forge.py achievements <player>")
        print("  partner_forge.py quest <title> <desc> <type> <target> <points> [days]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "dashboard":
        player = sys.argv[2]
        game.print_dashboard(player)
    
    elif command == "leaderboard":
        print("\n🏆 PARTNER FORGE LEADERBOARD")
        print("="*70)
        for ranking in game.leaderboard["rankings"][:10]:
            rank_emoji = "🥇" if ranking["rank"] == 1 else "🥈" if ranking["rank"] == 2 else "🥉" if ranking["rank"] == 3 else f"{ranking['rank']}."
            print(f"{rank_emoji} {ranking['player']}")
            print(f"   ⭐ {ranking['total_points']} points | 🏆 {ranking['achievements_unlocked']} achievements")
            print(f"   💰 {ranking['credits_earned']:.0f} credits | 🤖 {ranking['automations_built']} automations")
            print()
    
    elif command == "achievements":
        player = sys.argv[2]
        player_data = game.achievements["players"].get(player, {"unlocked": []})
        print(f"\n🏆 ACHIEVEMENTS - {player.upper()}")
        print("="*70)
        for ach_id in player_data["unlocked"]:
            ach = game.ACHIEVEMENTS[ach_id]
            print(f"{ach['icon']} {ach['name']} ({ach['points']} points)")
            print(f"   {ach['description']}")
    
    elif command == "quest":
        title, desc, quest_type, target, points = sys.argv[2:7]
        days = int(sys.argv[7]) if len(sys.argv) > 7 else 7
        quest = game.create_quest(title, desc, quest_type, int(target), int(points), days)
        print(f"✓ Created quest: {quest['id']} - {title}")


if __name__ == "__main__":
    main()
