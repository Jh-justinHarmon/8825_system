# 🔨 Partner Forge

**Gamified Partner Credit Marketplace**

Forge partnerships through collaborative work and automation. Build, craft, and strengthen partner relationships through achievements, leaderboards, and challenges.

---

## Quick Start

```bash
cd 8825_core/protocols/partner_credit_marketplace

# View your dashboard
./partner_forge.py dashboard smart

# Check leaderboard
./partner_forge.py leaderboard

# View achievements
./partner_forge.py achievements smart
```

---

## 🏆 Achievements

### Starter Achievements
- **🎯 First Blood** (10 pts) - Complete your first transaction
- **🤖 Automation Pioneer** (25 pts) - Build your first automation
- **📜 License Lord** (50 pts) - License your first automation

### Advanced Achievements
- **🤝 Consensus Builder** (75 pts) - Get 3 proposals approved
- **⚖️ Perfect Balance** (100 pts) - Maintain ±5% balance for 30 days
- **🏆 Governance Champion** (100 pts) - Vote on 20 proposals

### Elite Achievements
- **⚡ Sprint Master** (125 pts) - Complete 3 work orders in 7 days
- **🐋 Credit Whale** (150 pts) - Earn 1000+ credits
- **🏭 Automation Factory** (200 pts) - Build 10 automations
- **💎 Innovation Bounty** (250 pts) - Build automation worth 100+ credits

---

## 📊 Leaderboards

### Rankings By:
1. **Total Points** - Achievement points earned
2. **Credits Earned** - Total credits from work orders
3. **Automations Built** - Number of automations created
4. **Licenses Issued** - Automations licensed to others
5. **Governance Participation** - Voting record

### Ranks:
- 🥇 **#1** - Gold Medal
- 🥈 **#2** - Silver Medal
- 🥉 **#3** - Bronze Medal
- 🎯 **#4+** - Challenger

---

## ⚡ Quests & Challenges

### Active Quest Types:

**Sprint Challenges**
- Complete X work orders in Y days
- Earn Z credits in a week
- Build automation in 48 hours

**Innovation Challenges**
- Create automation with 5+ licenses
- Build cross-partner integration
- Achieve 100% test coverage

**Governance Challenges**
- Vote on 10 proposals
- Get 3 proposals approved
- Achieve 90% participation rate

### Forge Custom Quest:
```bash
./partner_forge.py quest "Sprint Week" "Complete 3 WOs in 7 days" sprint 3 125 7
```

---

## 🎯 Dashboard

Your personal dashboard shows:

### Stats
- 💰 **Credits**: Earned, spent, net position
- 🤖 **Automations**: Built, licensed, revenue
- 🗳️ **Governance**: Votes cast, participation rate

### Progress
- Current rank and points
- Achievements unlocked (X/10)
- Active quests
- Next 3 achievements to unlock

### Notifications
- 🎉 New achievements unlocked
- ⚡ Quest progress updates
- 🏆 Rank changes

---

## 🔨 How to Forge

### 1. Start Forging
```bash
# Add yourself as a partner
./ledger.py add-partner smart "Smart Inc" "contact@smart.com"

# View your dashboard
./credit_quest.py dashboard smart
```

### 2. Earn Points
- Complete transactions → Unlock "First Blood"
- Build automations → Unlock "Automation Pioneer"
- License to others → Unlock "License Lord"
- Vote on proposals → Unlock "Governance Champion"

### 3. Climb the Leaderboard
```bash
# Check your rank
./credit_quest.py leaderboard
```

### 4. Complete Quests
- Accept active quests
- Complete objectives
- Earn bonus points

---

## 🏅 Point System

### Achievement Points
- Starter: 10-50 points
- Advanced: 75-100 points
- Elite: 125-250 points

### Quest Rewards
- Sprint challenges: 100-150 points
- Innovation challenges: 150-250 points
- Governance challenges: 75-125 points

### Leaderboard Bonuses
- 🥇 #1: +50 points/month
- 🥈 #2: +30 points/month
- 🥉 #3: +20 points/month

---

## 🎨 Visual Dashboard

### Coming Soon:
- Web-based dashboard
- Real-time leaderboard
- Achievement showcase
- Quest progress bars
- Partner network graph
- Credit flow visualization

---

## 🤝 Multiplayer Features

### Team Quests
- Cross-partner challenges
- Collaborative goals
- Shared rewards

### Competitions
- Monthly tournaments
- Head-to-head challenges
- Winner takes all

### Social Features
- Achievement sharing
- Quest invitations
- Partner endorsements

---

## 📈 Strategy Tips

### Fast Start
1. Complete first transaction (10 pts)
2. Build first automation (25 pts)
3. License it (50 pts)
4. **Total: 85 points in first week**

### Automation Focus
- Build 10 automations (200 pts)
- License each 3+ times
- Earn Innovation Bounty (250 pts)
- **Total: 450+ points**

### Governance Path
- Vote on 20 proposals (100 pts)
- Get 3 approved (75 pts)
- Maintain participation (bonus)
- **Total: 175+ points**

---

## 🎯 Example Session

```bash
# Check dashboard
./partner_forge.py dashboard smart

🔨 PARTNER FORGE - SMART
======================================================================

🥇 Rank: #1 | ⭐ Points: 285
🏆 Achievements: 5/10

🎉 NEW ACHIEVEMENTS UNLOCKED!
  🤖 Automation Pioneer (+25 points)
     Build your first automation

📊 STATS
  💰 Credits: 250 earned | 100 spent | 150 net
  🤖 Automations: 3 built | 5 licensed | 125 revenue
  🗳️  Governance: 8 votes | 80% participation

🎯 NEXT ACHIEVEMENTS
  🤝 Consensus Builder (75 points)
     Get 3 proposals approved
  ⚖️ Perfect Balance (100 points)
     Maintain ±5% balance for 30 days
```

---

## 🚀 Integration

Partner Forge automatically tracks:
- All ledger transactions
- Automation catalog activity
- Governance participation

No extra work needed - just use the marketplace and earn achievements!

---

**Ready to forge? Fire up the anvil!**

```bash
./partner_forge.py dashboard <your_partner_id>
```
