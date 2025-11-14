#!/usr/bin/env python3
"""
Partner Credit Marketplace - Governance System
Voting, proposals, and steering group management
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional

# Configuration
GOV_DIR = Path(__file__).parent / "data"
PROPOSALS_FILE = GOV_DIR / "proposals.json"
VOTES_FILE = GOV_DIR / "votes.json"

# Ensure data directory exists
GOV_DIR.mkdir(parents=True, exist_ok=True)


class GovernanceSystem:
    """Steering group governance and voting"""
    
    def __init__(self):
        self.proposals = self._load_proposals()
        self.votes = self._load_votes()
    
    def _load_proposals(self) -> dict:
        """Load proposals from disk"""
        if PROPOSALS_FILE.exists():
            with open(PROPOSALS_FILE, 'r') as f:
                return json.load(f)
        
        return {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "proposals": []
        }
    
    def _load_votes(self) -> dict:
        """Load votes from disk"""
        if VOTES_FILE.exists():
            with open(VOTES_FILE, 'r') as f:
                return json.load(f)
        
        return {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "votes": []
        }
    
    def _save_proposals(self):
        """Save proposals to disk"""
        with open(PROPOSALS_FILE, 'w') as f:
            json.dump(self.proposals, f, indent=2)
    
    def _save_votes(self):
        """Save votes to disk"""
        with open(VOTES_FILE, 'w') as f:
            json.dump(self.votes, f, indent=2)
    
    def create_proposal(
        self,
        title: str,
        description: str,
        proposer: str,
        proposal_type: str,
        voting_period_days: int = 7,
        requires_consensus: bool = False
    ) -> dict:
        """Create a new proposal"""
        proposal = {
            "id": f"PROP-{len(self.proposals['proposals']) + 1:04d}",
            "title": title,
            "description": description,
            "proposer": proposer,
            "type": proposal_type,
            "created": datetime.now().isoformat(),
            "voting_deadline": (datetime.now() + timedelta(days=voting_period_days)).isoformat(),
            "requires_consensus": requires_consensus,
            "status": "open",
            "votes_for": 0,
            "votes_against": 0,
            "votes_abstain": 0
        }
        
        self.proposals["proposals"].append(proposal)
        self._save_proposals()
        return proposal
    
    def cast_vote(
        self,
        proposal_id: str,
        voter: str,
        vote: str,
        comment: Optional[str] = None
    ) -> dict:
        """Cast a vote on a proposal"""
        # Validate vote
        if vote not in ["for", "against", "abstain"]:
            raise ValueError("Vote must be 'for', 'against', or 'abstain'")
        
        # Get proposal
        proposal = self.get_proposal(proposal_id)
        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found")
        
        if proposal["status"] != "open":
            raise ValueError(f"Proposal {proposal_id} is {proposal['status']}, cannot vote")
        
        # Check if already voted
        existing_vote = next(
            (v for v in self.votes["votes"] if v["proposal_id"] == proposal_id and v["voter"] == voter),
            None
        )
        
        if existing_vote:
            # Update existing vote
            old_vote = existing_vote["vote"]
            existing_vote["vote"] = vote
            existing_vote["comment"] = comment
            existing_vote["updated"] = datetime.now().isoformat()
            
            # Update proposal counts
            proposal[f"votes_{old_vote}"] -= 1
            proposal[f"votes_{vote}"] += 1
        else:
            # Create new vote
            vote_record = {
                "id": f"VOTE-{len(self.votes['votes']) + 1:04d}",
                "proposal_id": proposal_id,
                "voter": voter,
                "vote": vote,
                "comment": comment,
                "cast": datetime.now().isoformat()
            }
            
            self.votes["votes"].append(vote_record)
            
            # Update proposal counts
            proposal[f"votes_{vote}"] += 1
        
        self._save_proposals()
        self._save_votes()
        
        # Check if voting is complete
        self._check_proposal_status(proposal_id)
        
        return proposal
    
    def _check_proposal_status(self, proposal_id: str):
        """Check if proposal voting is complete"""
        proposal = self.get_proposal(proposal_id)
        if not proposal or proposal["status"] != "open":
            return
        
        # Check if deadline passed
        deadline = datetime.fromisoformat(proposal["voting_deadline"])
        if datetime.now() > deadline:
            self._finalize_proposal(proposal_id)
    
    def _finalize_proposal(self, proposal_id: str):
        """Finalize proposal voting"""
        proposal = self.get_proposal(proposal_id)
        if not proposal:
            return
        
        total_votes = proposal["votes_for"] + proposal["votes_against"] + proposal["votes_abstain"]
        
        if total_votes == 0:
            proposal["status"] = "expired"
        elif proposal["requires_consensus"]:
            # Consensus requires all votes to be "for"
            if proposal["votes_against"] == 0 and proposal["votes_for"] > 0:
                proposal["status"] = "approved"
            else:
                proposal["status"] = "rejected"
        else:
            # Majority vote
            if proposal["votes_for"] > proposal["votes_against"]:
                proposal["status"] = "approved"
            elif proposal["votes_against"] > proposal["votes_for"]:
                proposal["status"] = "rejected"
            else:
                proposal["status"] = "tied"
        
        proposal["finalized"] = datetime.now().isoformat()
        self._save_proposals()
    
    def get_proposal(self, proposal_id: str) -> Optional[dict]:
        """Get proposal by ID"""
        for proposal in self.proposals["proposals"]:
            if proposal["id"] == proposal_id:
                return proposal
        return None
    
    def get_open_proposals(self) -> List[dict]:
        """Get all open proposals"""
        return [p for p in self.proposals["proposals"] if p["status"] == "open"]
    
    def get_proposal_votes(self, proposal_id: str) -> List[dict]:
        """Get all votes for a proposal"""
        return [v for v in self.votes["votes"] if v["proposal_id"] == proposal_id]
    
    def get_partner_voting_record(self, partner: str) -> dict:
        """Get voting record for a partner"""
        partner_votes = [v for v in self.votes["votes"] if v["voter"] == partner]
        
        record = {
            "partner": partner,
            "total_votes": len(partner_votes),
            "votes_for": len([v for v in partner_votes if v["vote"] == "for"]),
            "votes_against": len([v for v in partner_votes if v["vote"] == "against"]),
            "votes_abstain": len([v for v in partner_votes if v["vote"] == "abstain"]),
            "participation_rate": 0.0
        }
        
        total_proposals = len(self.proposals["proposals"])
        if total_proposals > 0:
            record["participation_rate"] = len(partner_votes) / total_proposals
        
        return record


def main():
    """CLI for governance system"""
    import sys
    
    gov = GovernanceSystem()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  governance.py propose <title> <description> <proposer> <type> [days] [consensus]")
        print("  governance.py vote <prop_id> <voter> <for|against|abstain> [comment]")
        print("  governance.py show <prop_id>")
        print("  governance.py open")
        print("  governance.py record <partner>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "propose":
        title, desc, proposer, prop_type = sys.argv[2:6]
        days = int(sys.argv[6]) if len(sys.argv) > 6 else 7
        consensus = sys.argv[7].lower() == "true" if len(sys.argv) > 7 else False
        
        proposal = gov.create_proposal(title, desc, proposer, prop_type, days, consensus)
        print(f"✓ Created proposal: {proposal['id']}")
        print(f"  Title: {title}")
        print(f"  Voting deadline: {proposal['voting_deadline']}")
        print(f"  Requires consensus: {consensus}")
    
    elif command == "vote":
        prop_id, voter, vote = sys.argv[2:5]
        comment = sys.argv[5] if len(sys.argv) > 5 else None
        
        proposal = gov.cast_vote(prop_id, voter, vote, comment)
        print(f"✓ Vote cast on {prop_id}")
        print(f"  Current tally: {proposal['votes_for']} for, {proposal['votes_against']} against, {proposal['votes_abstain']} abstain")
        print(f"  Status: {proposal['status']}")
    
    elif command == "show":
        prop_id = sys.argv[2]
        proposal = gov.get_proposal(prop_id)
        if not proposal:
            print(f"Proposal {prop_id} not found")
            sys.exit(1)
        
        print(f"Proposal: {proposal['id']}")
        print(f"  Title: {proposal['title']}")
        print(f"  Description: {proposal['description']}")
        print(f"  Proposer: {proposal['proposer']}")
        print(f"  Type: {proposal['type']}")
        print(f"  Status: {proposal['status']}")
        print(f"  Votes: {proposal['votes_for']} for, {proposal['votes_against']} against, {proposal['votes_abstain']} abstain")
        
        votes = gov.get_proposal_votes(prop_id)
        if votes:
            print(f"\n  Vote details:")
            for vote in votes:
                print(f"    {vote['voter']}: {vote['vote']}")
                if vote.get('comment'):
                    print(f"      Comment: {vote['comment']}")
    
    elif command == "open":
        proposals = gov.get_open_proposals()
        print(f"Open proposals ({len(proposals)}):")
        for prop in proposals:
            print(f"  {prop['id']}: {prop['title']}")
            print(f"    Status: {prop['status']}, Deadline: {prop['voting_deadline']}")
            print(f"    Votes: {prop['votes_for']} for, {prop['votes_against']} against")
    
    elif command == "record":
        partner = sys.argv[2]
        record = gov.get_partner_voting_record(partner)
        print(f"Voting record for {partner}:")
        print(f"  Total votes: {record['total_votes']}")
        print(f"  For: {record['votes_for']}, Against: {record['votes_against']}, Abstain: {record['votes_abstain']}")
        print(f"  Participation rate: {record['participation_rate']:.1%}")


if __name__ == "__main__":
    main()
