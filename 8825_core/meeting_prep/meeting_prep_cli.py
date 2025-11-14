#!/usr/bin/env python3
"""
Meeting Prep CLI - Interactive meeting preparation
"""

import sys
from datetime import datetime
from prep_generator import (
    MeetingPrepGenerator, MeetingPrep, Person, TopOfMind,
    SMARTGoal, BigIdea, MeetingSchedule
)


class MeetingPrepCLI:
    """Interactive CLI for meeting prep"""
    
    def __init__(self):
        self.generator = MeetingPrepGenerator()
    
    def run(self):
        """Run interactive meeting prep"""
        print("\n" + "="*60)
        print("🚀 Meeting Prep System - Excitement Before Logistics")
        print("="*60 + "\n")
        
        # Get person info
        person = self.get_person_info()
        
        # Get top of mind
        print("\n" + "-"*60)
        print("📋 Step 1: Top of Mind (Ground Yourself)")
        print("-"*60)
        top_of_mind = self.get_top_of_mind()
        
        # Get SMART goals (excitement starts here)
        print("\n" + "-"*60)
        print("🎯 Step 2: SMART Goals (Get Strategic)")
        print("-"*60)
        smart_goal = self.get_smart_goal(person)
        
        # Get big ideas (peak excitement)
        print("\n" + "-"*60)
        print("💡 Step 3: Big Ideas (Get Inspired!)")
        print("-"*60)
        big_ideas = self.get_big_ideas()
        
        # Get questions (specific conversation)
        print("\n" + "-"*60)
        print("❓ Step 4: Specific Questions")
        print("-"*60)
        questions = self.get_questions(person)
        
        # Get schedule (now you're motivated!)
        print("\n" + "-"*60)
        print("✅ Step 5: Make It Happen (You're Ready!)")
        print("-"*60)
        schedule = self.get_schedule()
        
        # Action items
        action_items = self.get_action_items(person)
        
        # Generate prep
        prep = MeetingPrep(
            person=person,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M'),
            top_of_mind=top_of_mind,
            smart_goal=smart_goal,
            big_ideas=big_ideas,
            specific_questions=questions,
            schedule=schedule,
            action_items=action_items
        )
        
        filepath = self.generator.generate(prep)
        
        print("\n" + "="*60)
        print(f"✅ Meeting prep created: {filepath}")
        print("="*60)
        print("\n🚀 You're ready for this conversation!\n")
    
    def get_person_info(self) -> Person:
        """Get person information"""
        print("Who are you meeting with?\n")
        
        name = input("Name: ").strip()
        role = input("Role (e.g., CTO, Client, Mentor): ").strip()
        expertise = input("Expertise (e.g., Technical architecture, Marketing): ").strip()
        relationship = input("Relationship (colleague/client/mentor/etc): ").strip()
        
        return Person(name=name, role=role, expertise=expertise, relationship=relationship)
    
    def get_top_of_mind(self) -> TopOfMind:
        """Get top of mind items"""
        print("\nWhat's on your mind right now?\n")
        
        current_priorities = self.get_list("Current priorities (one per line, empty to finish)")
        recent_wins = self.get_list("Recent wins")
        open_loops = self.get_list("Open loops needing closure")
        time_sensitive = self.get_list("Time-sensitive items")
        
        return TopOfMind(
            current_priorities=current_priorities,
            recent_wins=recent_wins,
            open_loops=open_loops,
            time_sensitive=time_sensitive
        )
    
    def get_smart_goal(self, person: Person) -> SMARTGoal:
        """Get SMART goal"""
        print(f"\nWhy does meeting with {person.name} matter?\n")
        
        why_this_matters = input("Why this meeting matters: ").strip()
        
        print("\nYour strengths (how to flex them):")
        strengths = []
        while True:
            strength = input("  Strength (empty to finish): ").strip()
            if not strength:
                break
            relevance = input(f"  How is '{strength}' relevant to {person.name}? ").strip()
            strengths.append({strength: relevance})
        
        print("\nYour weaknesses (how they can help):")
        weaknesses = []
        while True:
            weakness = input("  Weakness/Gap (empty to finish): ").strip()
            if not weakness:
                break
            help_text = input(f"  How can {person.name} help with '{weakness}'? ").strip()
            weaknesses.append({weakness: help_text})
        
        print("\nSMART Goal for this meeting:")
        specific = input("  Specific (exact outcome): ").strip()
        measurable = input("  Measurable (how you'll know it worked): ").strip()
        achievable = input("  Achievable (why it's realistic): ").strip()
        relevant = input(f"  Relevant (why {person.name} specifically): ").strip()
        time_bound = input("  Time-bound (deadline): ").strip()
        
        return SMARTGoal(
            why_this_matters=why_this_matters,
            strengths_to_flex=strengths,
            weaknesses_to_mitigate=weaknesses,
            specific=specific,
            measurable=measurable,
            achievable=achievable,
            relevant=relevant,
            time_bound=time_bound
        )
    
    def get_big_ideas(self) -> list:
        """Get big ideas"""
        print("\nWhat's possible if this conversation goes well?\n")
        
        ideas = []
        while True:
            title = input("Big idea title (empty to finish): ").strip()
            if not title:
                break
            description = input("  Description: ").strip()
            upside = input("  The upside (what could happen): ").strip()
            ideas.append(BigIdea(title=title, description=description, upside=upside))
        
        return ideas
    
    def get_questions(self, person: Person) -> list:
        """Get specific questions"""
        print(f"\nWhat specific questions do you have for {person.name}?\n")
        print("(Think about their unique expertise and perspective)\n")
        
        return self.get_list("Questions")
    
    def get_schedule(self) -> MeetingSchedule:
        """Get scheduling info"""
        print("\nWhen should this meeting happen?\n")
        
        recommended = input("Recommended time (e.g., 'Next Tuesday 2pm'): ").strip()
        backup = input("Backup time: ").strip()
        deadline = input("Schedule by (creates urgency): ").strip()
        calendar_link = input("Calendar link (optional): ").strip()
        
        return MeetingSchedule(
            recommended_time=recommended or None,
            backup_time=backup or None,
            schedule_deadline=deadline or None,
            calendar_link=calendar_link or None
        )
    
    def get_action_items(self, person: Person) -> list:
        """Get action items"""
        default_items = [
            f"Schedule meeting with {person.name}",
            "Send calendar invite",
            "Follow up after meeting"
        ]
        
        print("\nAction items (defaults provided, add more if needed):")
        for item in default_items:
            print(f"  - {item}")
        
        additional = self.get_list("\nAdditional action items (optional)")
        
        return default_items + additional
    
    def get_list(self, prompt: str) -> list:
        """Get list of items"""
        print(f"\n{prompt} (one per line, empty line to finish):")
        items = []
        while True:
            item = input("  - ").strip()
            if not item:
                break
            items.append(item)
        return items


def main():
    """Main entry point"""
    cli = MeetingPrepCLI()
    cli.run()


if __name__ == '__main__':
    main()
