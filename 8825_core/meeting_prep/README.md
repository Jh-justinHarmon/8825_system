# Meeting Prep System

**Excitement before logistics** - Get inspired, then schedule.

---

## Philosophy

### The Problem
Traditional meeting prep feels like a chore:
1. Look at calendar (ugh)
2. Try to think of what to talk about
3. Procrastinate
4. Meeting never happens

### The Solution
**Reverse the flow:**
1. Ground yourself (what's on your mind)
2. Get strategic (what you'll accomplish)
3. Get inspired (what's possible!)
4. Get specific (the conversation)
5. Get it done (now you're motivated to schedule)

**By the time you hit scheduling, you're excited about the meeting.**

---

## The Framework

### 1. Top of Mind
- Current priorities
- Recent wins/challenges
- Open loops
- Time-sensitive items

**Purpose:** Ground yourself in current context

### 2. Context-Specific SMART Goals
- Why this meeting matters (get excited!)
- Your strengths (how to flex them)
- Your weaknesses (how they can help)
- SMART goal for the meeting

**Purpose:** Get strategic about what you'll accomplish

### 3. Big Ideas
- Strategic opportunities
- Innovation concepts
- What's possible if this goes well
- The upside

**Purpose:** Get inspired and excited!

### 4. Specific Questions
- Questions leveraging their unique expertise
- Questions about opportunities
- Questions seeking their help

**Purpose:** Visualize the actual conversation

### 5. Let's Make It Happen
- Recommended meeting time
- Backup time
- Schedule deadline (creates urgency)
- Easy scheduling link

**Purpose:** Make scheduling feel like enabling the conversation, not a chore

---

## Quick Start

### Interactive Mode
```bash
cd 8825_core/meeting_prep
python3 meeting_prep_cli.py
```

Follow the prompts through all 5 steps.

### Programmatic Mode
```python
from prep_generator import *

prep = MeetingPrep(
    person=Person(
        name="Matthew",
        role="CTO",
        expertise="Technical architecture",
        relationship="colleague"
    ),
    # ... fill in other fields
)

generator = MeetingPrepGenerator()
filepath = generator.generate(prep)
```

---

## Output

### Markdown File
Clean, readable prep document with all 5 sections.

**Location:** `~/Documents/8825/meeting_prep/YYYYMMDD_PersonName_prep.md`

### JSON File
Structured data for programmatic access.

**Location:** `~/Documents/8825/meeting_prep/YYYYMMDD_PersonName_prep.json`

---

## Example Output

```markdown
# Meeting Prep: Matthew

**Role**: CTO  
**Expertise**: Technical architecture  

---

## 1. Top of Mind

### Current Priorities
- Joju technical roadmap
- 8825 inbox system complete

### Recent Wins
- Built intelligent inbox with AI sweep

---

## 2. Context-Specific SMART Goals

### 🎯 Why This Meeting Matters

Matthew's technical expertise can validate the 8825+Goose 
architecture before we build too far.

### 💪 Your Strengths (How to Flex)

- **System thinking**: Show him the two-lane inbox architecture
- **AI integration**: Demonstrate the AI sweep pattern

### 🔧 Your Weaknesses (How to Mitigate)

- **Technical depth**: Get his input on MCP server architecture

### 🎯 SMART Goal

- **Specific**: Get technical validation on 8825+Goose pattern
- **Measurable**: Walk away with 3 specific recommendations
- **Achievable**: He has expertise, we have concrete design
- **Relevant**: His CTO perspective prevents wrong decisions
- **Time-bound**: Before we start building (next 2 weeks)

---

## 3. Big Ideas (What's Possible)

### 8825 as Brain, Goose as Execution Layer

Two-layer automation where 8825 produces task specs 
and Goose executes via MCP.

### 🚀 The Upside

- Could unlock fully automated workflows
- Keeps 8825's context layer intact
- Proves pattern with real use case

---

## 4. Specific Questions

1. What technical risks do you see in the architecture?
2. How would you structure the MCP communication layer?
3. What's the right abstraction boundary?
4. Should we build this or refactor existing patterns?

---

## 5. Let's Make It Happen ✅

**Recommended Time**: Next Tuesday 2pm  
**Backup Time**: Thursday 10am  
**Schedule By**: End of this week

**Action Items:**
- [ ] Schedule meeting by Friday
- [ ] Send Matthew the architecture doc
- [ ] Prepare demo of inbox system
- [ ] Follow up with technical recommendations

---

**You're ready for this conversation!** 🚀
```

---

## The Psychology

### Old Flow (Logistics First)
```
Calendar → "Ugh, I need to schedule..."
         → "What would we even talk about?"
         → Procrastinate
         → Never happens
```

### New Flow (Excitement First)
```
Top of Mind → "Here's where I am"
SMART Goals → "Here's what I'll accomplish"
Big Ideas   → "Wow, this could be huge!"
Questions   → "I need to talk to them NOW!"
Schedule    → "Let's make this happen!" ✅
```

**Scheduling becomes enabling the opportunity, not a chore.**

---

## Integration with 8825

### Save Location
`~/Documents/8825/meeting_prep/`

### Future Enhancements
- Track meeting outcomes
- Build people database with context
- Create templates for recurring meeting types
- Calendar screenshot analysis
- Auto-suggest meeting times
- Integration with inbox system

---

## Files

```
8825_core/meeting_prep/
├── prep_generator.py      # Core generator
├── meeting_prep_cli.py    # Interactive CLI
└── README.md             # This file
```

---

## Usage Tips

### Before the Meeting
1. Run the prep generator
2. Review the output
3. Get excited about the conversation
4. Schedule it (you're motivated now!)

### During the Meeting
- Reference your SMART goal
- Ask your specific questions
- Listen for the upside opportunities

### After the Meeting
- Check off action items
- Note what happened
- Follow up

---

**Status:** Production Ready  
**Version:** 1.0  
**Built:** 2025-11-08

**Get excited, then schedule. That's the system.** 🚀
