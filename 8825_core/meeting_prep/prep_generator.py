#!/usr/bin/env python3
"""
Meeting Prep Generator - Excitement-first meeting preparation
"""

import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any


@dataclass
class Person:
    """Person you're meeting with"""
    name: str
    role: str
    expertise: str
    relationship: str  # colleague, client, mentor, etc.


@dataclass
class TopOfMind:
    """Current priorities and context"""
    current_priorities: List[str]
    recent_wins: List[str]
    open_loops: List[str]
    time_sensitive: List[str]


@dataclass
class SMARTGoal:
    """Context-specific SMART goal"""
    why_this_matters: str
    strengths_to_flex: List[Dict[str, str]]  # {strength: how_relevant}
    weaknesses_to_mitigate: List[Dict[str, str]]  # {weakness: how_they_help}
    specific: str
    measurable: str
    achievable: str
    relevant: str
    time_bound: str


@dataclass
class BigIdea:
    """Strategic opportunity"""
    title: str
    description: str
    upside: str


@dataclass
class MeetingSchedule:
    """Scheduling information"""
    recommended_time: Optional[str]
    backup_time: Optional[str]
    schedule_deadline: Optional[str]
    calendar_link: Optional[str]


@dataclass
class MeetingPrep:
    """Complete meeting prep document"""
    person: Person
    created_at: str
    top_of_mind: TopOfMind
    smart_goal: SMARTGoal
    big_ideas: List[BigIdea]
    specific_questions: List[str]
    schedule: MeetingSchedule
    action_items: List[str]


class MeetingPrepGenerator:
    """Generate meeting prep documents"""
    
    TEMPLATE = """# Meeting Prep: {person_name}

**Role**: {person_role}  
**Expertise**: {person_expertise}  
**Relationship**: {person_relationship}  
**Prep Created**: {created_at}

---

## 1. Top of Mind (Right Now)

### Current Priorities
{current_priorities}

### Recent Wins
{recent_wins}

### Open Loops
{open_loops}

### Time-Sensitive Items
{time_sensitive}

---

## 2. Context-Specific SMART Goals

### 🎯 Why This Meeting Matters

{why_this_matters}

### 💪 Your Strengths (How to Flex)

{strengths}

### 🔧 Your Weaknesses (How to Mitigate)

{weaknesses}

### 🎯 SMART Goal for This Meeting

- **Specific**: {specific}
- **Measurable**: {measurable}
- **Achievable**: {achievable}
- **Relevant**: {relevant}
- **Time-bound**: {time_bound}

---

## 3. Big Ideas (What's Possible)

{big_ideas}

### 🚀 The Upside

{upside}

---

## 4. Specific Questions

{questions}

---

## 5. Let's Make It Happen ✅

{schedule_info}

**Action Items:**
{action_items}

---

**You're ready for this conversation!** 🚀
"""
    
    def __init__(self, output_dir: Optional[str] = None):
        if output_dir is None:
            output_dir = Path.home() / 'Documents' / '8825' / 'meeting_prep'
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(self, prep: MeetingPrep) -> str:
        """Generate meeting prep markdown"""
        
        # Format sections
        current_priorities = self._format_list(prep.top_of_mind.current_priorities)
        recent_wins = self._format_list(prep.top_of_mind.recent_wins)
        open_loops = self._format_list(prep.top_of_mind.open_loops)
        time_sensitive = self._format_list(prep.top_of_mind.time_sensitive)
        
        # Format strengths
        strengths = []
        for item in prep.smart_goal.strengths_to_flex:
            for strength, relevance in item.items():
                strengths.append(f"- **{strength}**: {relevance}")
        strengths_text = '\n'.join(strengths) if strengths else "- (Add your strengths)"
        
        # Format weaknesses
        weaknesses = []
        for item in prep.smart_goal.weaknesses_to_mitigate:
            for weakness, help_text in item.items():
                weaknesses.append(f"- **{weakness}**: {help_text}")
        weaknesses_text = '\n'.join(weaknesses) if weaknesses else "- (Add areas where they can help)"
        
        # Format big ideas
        big_ideas_text = []
        upside_parts = []
        for idea in prep.big_ideas:
            big_ideas_text.append(f"### {idea.title}\n\n{idea.description}\n")
            if idea.upside:
                upside_parts.append(f"- {idea.upside}")
        
        big_ideas_formatted = '\n'.join(big_ideas_text) if big_ideas_text else "### (Add your big ideas)"
        upside_formatted = '\n'.join(upside_parts) if upside_parts else "(What happens if this conversation unlocks something)"
        
        # Format questions
        questions = '\n'.join(f"{i}. {q}" for i, q in enumerate(prep.specific_questions, 1))
        if not questions:
            questions = "1. (Add your questions)"
        
        # Format schedule
        schedule_parts = []
        if prep.schedule.recommended_time:
            schedule_parts.append(f"**Recommended Time**: {prep.schedule.recommended_time}")
        if prep.schedule.backup_time:
            schedule_parts.append(f"**Backup Time**: {prep.schedule.backup_time}")
        if prep.schedule.schedule_deadline:
            schedule_parts.append(f"**Schedule By**: {prep.schedule.schedule_deadline}")
        if prep.schedule.calendar_link:
            schedule_parts.append(f"\n[📅 Schedule Now]({prep.schedule.calendar_link})")
        
        schedule_info = '\n'.join(schedule_parts) if schedule_parts else "**Schedule this meeting!**"
        
        # Format action items
        action_items = '\n'.join(f"- [ ] {item}" for item in prep.action_items)
        if not action_items:
            action_items = "- [ ] Schedule meeting\n- [ ] Send calendar invite\n- [ ] Follow up after meeting"
        
        # Generate markdown
        content = self.TEMPLATE.format(
            person_name=prep.person.name,
            person_role=prep.person.role,
            person_expertise=prep.person.expertise,
            person_relationship=prep.person.relationship,
            created_at=prep.created_at,
            current_priorities=current_priorities,
            recent_wins=recent_wins,
            open_loops=open_loops,
            time_sensitive=time_sensitive,
            why_this_matters=prep.smart_goal.why_this_matters,
            strengths=strengths_text,
            weaknesses=weaknesses_text,
            specific=prep.smart_goal.specific,
            measurable=prep.smart_goal.measurable,
            achievable=prep.smart_goal.achievable,
            relevant=prep.smart_goal.relevant,
            time_bound=prep.smart_goal.time_bound,
            big_ideas=big_ideas_formatted,
            upside=upside_formatted,
            questions=questions,
            schedule_info=schedule_info,
            action_items=action_items
        )
        
        # Save to file
        filename = f"{datetime.now().strftime('%Y%m%d')}_{prep.person.name.replace(' ', '_')}_prep.md"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        # Also save as JSON
        json_file = filepath.with_suffix('.json')
        with open(json_file, 'w') as f:
            json.dump(self._prep_to_dict(prep), f, indent=2)
        
        return str(filepath)
    
    def _format_list(self, items: List[str]) -> str:
        """Format list items"""
        if not items:
            return "- (Add items)"
        return '\n'.join(f"- {item}" for item in items)
    
    def _prep_to_dict(self, prep: MeetingPrep) -> dict:
        """Convert prep to dict for JSON"""
        return {
            'person': asdict(prep.person),
            'created_at': prep.created_at,
            'top_of_mind': asdict(prep.top_of_mind),
            'smart_goal': asdict(prep.smart_goal),
            'big_ideas': [asdict(idea) for idea in prep.big_ideas],
            'specific_questions': prep.specific_questions,
            'schedule': asdict(prep.schedule),
            'action_items': prep.action_items
        }


if __name__ == '__main__':
    # Test with example
    generator = MeetingPrepGenerator()
    
    prep = MeetingPrep(
        person=Person(
            name="Matthew",
            role="CTO",
            expertise="Technical architecture, system design",
            relationship="colleague"
        ),
        created_at=datetime.now().strftime('%Y-%m-%d %H:%M'),
        top_of_mind=TopOfMind(
            current_priorities=["Joju technical roadmap", "8825 inbox system complete"],
            recent_wins=["Built intelligent inbox with AI sweep", "Two-lane architecture working"],
            open_loops=["Goose + 8825 integration pattern", "MCP server architecture"],
            time_sensitive=["Q1 planning deadline approaching"]
        ),
        smart_goal=SMARTGoal(
            why_this_matters="Matthew's technical expertise can validate the 8825+Goose architecture and identify potential issues before we build too far.",
            strengths_to_flex=[
                {"System thinking": "Show him the two-lane inbox architecture"},
                {"AI integration": "Demonstrate the AI sweep pattern"}
            ],
            weaknesses_to_mitigate=[
                {"Technical depth": "Get his input on MCP server architecture"},
                {"Scalability concerns": "Validate the approach will scale"}
            ],
            specific="Get Matthew's technical validation on 8825+Goose integration pattern",
            measurable="Walk away with 3 specific technical recommendations",
            achievable="He has the expertise and we have a concrete design to review",
            relevant="His CTO perspective prevents us from building the wrong thing",
            time_bound="Before we start building (next 2 weeks)"
        ),
        big_ideas=[
            BigIdea(
                title="8825 as Brain, Goose as Execution Layer",
                description="Two-layer automation where 8825 produces task specs and Goose executes via MCP",
                upside="Could unlock fully automated workflows while keeping 8825's context layer intact"
            ),
            BigIdea(
                title="Scanned Letter → Calendar Events",
                description="OCR → 8825 routing → deadline extraction → automated calendar creation",
                upside="Proves the pattern works with a real business use case"
            )
        ],
        specific_questions=[
            "What technical risks do you see in the 8825+Goose architecture?",
            "How would you structure the MCP communication layer?",
            "What's the right abstraction boundary between brain and execution?",
            "Should we build this or refactor existing patterns?"
        ],
        schedule=MeetingSchedule(
            recommended_time="Next Tuesday 2pm",
            backup_time="Thursday 10am",
            schedule_deadline="End of this week",
            calendar_link=None
        ),
        action_items=[
            "Schedule meeting by Friday",
            "Send Matthew the 8825+Goose architecture doc",
            "Prepare demo of inbox system",
            "Follow up with technical recommendations"
        ]
    )
    
    filepath = generator.generate(prep)
    print(f"Generated: {filepath}")
