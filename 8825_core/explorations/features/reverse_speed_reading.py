#!/usr/bin/env python3
"""
Reverse Speed Reading - Predictive Text Composer
AI predicts the rest of your message as you type, reframing with each word
"""

import json
import os
import sys
from datetime import datetime

# Mock contact list (would integrate with actual contacts)
CONTACTS = {
    "justin": "Justin Harmon",
    "becky": "Becky Harmon",
    "smart": "Smart (Partner)",
    "hcss": "HCSS Team",
    "team76": "Team76"
}

class PredictiveComposer:
    """AI-powered predictive text composer"""
    
    def __init__(self):
        self.history = []
        self.current_message = {
            "to": None,
            "topic": None,
            "words": [],
            "predictions": []
        }
    
    def get_contact(self, name_input):
        """Match contact from input"""
        name_lower = name_input.lower()
        for key, full_name in CONTACTS.items():
            if name_lower in key or name_lower in full_name.lower():
                return full_name
        return name_input  # Return as-is if no match
    
    def predict_next(self, words_so_far, topic=None):
        """
        Predict the rest of the message based on words typed so far
        In production, this would call OpenAI/Claude API
        For prototype, using rule-based predictions
        """
        word_count = len(words_so_far)
        context = " ".join(words_so_far)
        
        # Rule-based predictions for prototype
        # In production: call LLM with context
        
        if word_count == 0:
            return "I wanted to reach out about..."
        
        if word_count == 1:
            first_word = words_so_far[0].lower()
            
            if first_word in ["hi", "hey", "hello"]:
                return "I hope this message finds you well. I wanted to discuss..."
            elif first_word in ["quick", "fast"]:
                return "question about the project we discussed..."
            elif first_word in ["thanks", "thank"]:
                return "so much for your help with..."
            elif first_word in ["can", "could"]:
                return "you help me with something? I need..."
            elif first_word in ["meeting", "call"]:
                return "scheduled for tomorrow - wanted to confirm..."
            else:
                return f"to follow up on {first_word}..."
        
        if word_count == 2:
            first = words_so_far[0].lower()
            second = words_so_far[1].lower()
            
            if first == "quick" and second == "question":
                return "about the timeline for the project. When can we expect..."
            elif first == "thanks" and second == "for":
                return "your help yesterday. It really made a difference..."
            elif first == "can" and second == "you":
                return "review this document before our meeting? I need feedback on..."
            elif first == "meeting" and second == "tomorrow":
                return "at 2pm - just wanted to confirm you're still available..."
            else:
                return f"regarding {second}. I think we should..."
        
        if word_count == 3:
            # More specific predictions based on 3-word context
            if "question" in context.lower():
                return "the deadline and deliverables. Let me know when you have time to discuss."
            elif "thanks" in context.lower():
                return "the support. Looking forward to working together again soon."
            elif "meeting" in context.lower():
                return "and wanted to share the agenda beforehand. Please let me know if this works."
            else:
                return "this further. Would you be available for a quick call?"
        
        # 4+ words - getting more specific
        return "this in more detail. Let me know your thoughts and availability."
    
    def compose_interactive(self):
        """Interactive composition with live predictions"""
        print("\n" + "="*70)
        print("🚀 REVERSE SPEED READING - Predictive Text Composer")
        print("="*70)
        print("\nHow it works:")
        print("1. Enter recipient name")
        print("2. Enter 2-3 word topic")
        print("3. Type words one at a time")
        print("4. AI predicts the rest after each word")
        print("5. Type 'done' when prediction matches your intent")
        print("6. Type 'restart' to start over")
        print("\n" + "-"*70)
        
        # Get recipient
        recipient_input = input("\n👤 To: ").strip()
        if not recipient_input:
            print("❌ Recipient required")
            return
        
        self.current_message["to"] = self.get_contact(recipient_input)
        print(f"   → {self.current_message['to']}")
        
        # Get topic
        topic_input = input("\n📌 Topic (2-3 words): ").strip()
        if not topic_input:
            print("❌ Topic required")
            return
        
        self.current_message["topic"] = topic_input
        print(f"   → {topic_input}")
        
        # Interactive word-by-word composition
        print("\n" + "="*70)
        print("💬 START TYPING (one word at a time, press Enter after each)")
        print("="*70)
        
        words = []
        iteration = 0
        
        while True:
            iteration += 1
            
            # Show current context
            if words:
                print(f"\n📝 So far: {' '.join(words)}")
            
            # Get prediction
            prediction = self.predict_next(words, self.current_message["topic"])
            
            print(f"\n🤖 AI predicts: {prediction}")
            print("-"*70)
            
            # Get next word
            next_word = input(f"Word #{iteration} (or 'done'/'restart'): ").strip()
            
            if not next_word:
                continue
            
            if next_word.lower() == "done":
                # User accepts prediction
                final_message = " ".join(words) + " " + prediction
                self.finalize_message(final_message)
                break
            
            if next_word.lower() == "restart":
                print("\n🔄 Restarting...")
                return self.compose_interactive()
            
            # Add word and continue
            words.append(next_word)
            self.current_message["words"] = words
            
            # Store prediction history
            self.current_message["predictions"].append({
                "after_word": iteration,
                "context": " ".join(words),
                "prediction": prediction
            })
    
    def finalize_message(self, final_text):
        """Show final composed message"""
        print("\n" + "="*70)
        print("✅ FINAL MESSAGE")
        print("="*70)
        print(f"\nTo: {self.current_message['to']}")
        print(f"Re: {self.current_message['topic']}")
        print(f"\n{final_text}")
        print("\n" + "="*70)
        
        # Save to history
        message_record = {
            "timestamp": datetime.now().isoformat(),
            "to": self.current_message["to"],
            "topic": self.current_message["topic"],
            "final_text": final_text,
            "word_count": len(self.current_message["words"]),
            "iterations": len(self.current_message["predictions"])
        }
        
        self.history.append(message_record)
        
        # Ask to send (mock)
        send = input("\n📤 Send this message? (y/n): ").strip().lower()
        if send == 'y':
            print("✅ Message sent! (mock)")
        else:
            print("💾 Message saved as draft")
    
    def show_stats(self):
        """Show composition statistics"""
        if not self.history:
            print("\n📊 No messages composed yet")
            return
        
        print("\n" + "="*70)
        print("📊 COMPOSITION STATS")
        print("="*70)
        
        total = len(self.history)
        avg_words = sum(m["word_count"] for m in self.history) / total
        avg_iterations = sum(m["iterations"] for m in self.history) / total
        
        print(f"\nTotal messages: {total}")
        print(f"Avg words typed: {avg_words:.1f}")
        print(f"Avg iterations: {avg_iterations:.1f}")
        print(f"Time saved: ~{total * 30}s (estimated)")
        
        print("\n📝 Recent messages:")
        for msg in self.history[-5:]:
            print(f"  • To {msg['to']}: {msg['topic']} ({msg['word_count']} words)")


def main():
    """CLI for reverse speed reading"""
    composer = PredictiveComposer()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "stats":
            composer.show_stats()
            return
        elif command == "help":
            print(__doc__)
            print("\nCommands:")
            print("  python3 reverse_speed_reading.py        # Start interactive composer")
            print("  python3 reverse_speed_reading.py stats  # Show statistics")
            print("  python3 reverse_speed_reading.py help   # Show this help")
            return
    
    # Default: interactive composition
    try:
        composer.compose_interactive()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
