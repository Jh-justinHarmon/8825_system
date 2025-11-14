# User Learning Attributes Separation Plan

**Created:** 2025-11-13  
**Status:** Design Phase  
**Priority:** High (Foundation for multi-user system)

---

## Problem Statement

**Current State:**
- Justin's learning preferences hardcoded in `LEARNING_FUNDAMENTALS_PROTOCOL.md`
- No separation between core principles and user-specific attributes
- New users would inherit Justin's preferences
- No mechanism to learn new users' preferences

**Desired State:**
- Core learning principles in protocol (universal)
- User-specific preferences in user profile (personal)
- New users start with sensible defaults
- System learns and adapts to each user's style

---

## Architecture

### **Three-Layer System:**

```
Layer 1: Core Protocol (Universal)
  └─ Learning dimensions and principles
  └─ Teaching mode triggers
  └─ Observation patterns
  └─ File: 8825_core/protocols/LEARNING_FUNDAMENTALS_PROTOCOL.md

Layer 2: User Profile (Personal)
  └─ Individual learning preferences
  └─ Observed patterns
  └─ Teaching moments that worked/failed
  └─ File: users/{username}/profile/learning_profile.json

Layer 3: Learning Engine (Adaptive)
  └─ Observes user interactions
  └─ Updates user profile
  └─ Suggests teaching approaches
  └─ File: 8825_core/brain/learning_engine.py
```

---

## Detailed Design

### **Layer 1: Core Protocol (Universal)**

**File:** `8825_core/protocols/LEARNING_FUNDAMENTALS_PROTOCOL.md`

**Contents:**
```markdown
# Learning Fundamentals Protocol

## Learning Style Dimensions (Universal)

### 1. Information Density
- Sparse: High-level only
- Moderate: Concepts + examples
- Dense: Full details + edge cases

### 2. Example Preference
- Concrete: Real examples from their work
- Abstract: Theoretical examples
- Comparative: Analogies to known concepts

### 3. Depth Approach
- Top-down: Big picture → details
- Bottom-up: Specifics → concepts
- Middle-out: Familiar → expand

### 4. Interaction Style
- Show me: Demonstrate
- Walk through: Step-by-step
- Let me try: Explore
- Explain first: Theory before practice

### 5. Error Tolerance
- High: Try and fail
- Low: Understand first
- Medium: Guided experimentation

## Teaching Mode Triggers (Universal)

- "Walk me through it" → Activate teaching mode
- "Explain" → Theory focus
- "Show me" → Demo focus
- "Help me understand" → Adaptive based on profile

## Observation Patterns (Universal)

Track these signals:
- Understanding: "Makes sense", deeper questions
- Confusion: Silence, repeat questions
- Boredom: "Yeah yeah", interrupts
- Overwhelm: "Wait what?", asks to slow down
- Engagement: Asks follow-up, tries variations

## Adaptation Rules (Universal)

If confusion → simplify
If boredom → accelerate
If overwhelm → chunk smaller
If engagement → go deeper
```

**NO user-specific content in core protocol**

---

### **Layer 2: User Profile (Personal)**

**File:** `users/{username}/profile/learning_profile.json`

**Schema:**
```json
{
  "user_id": "justin_harmon",
  "created_at": "2025-11-13T...",
  "last_updated": "2025-11-13T...",
  
  "learning_preferences": {
    "information_density": {
      "preference": "moderate",
      "confidence": 0.95,
      "last_updated": "2025-11-13T..."
    },
    "example_preference": {
      "preference": "concrete",
      "confidence": 0.98,
      "last_updated": "2025-11-13T..."
    },
    "depth_approach": {
      "preference": "top_down",
      "confidence": 0.92,
      "last_updated": "2025-11-13T..."
    },
    "interaction_style": {
      "preference": "show_and_explain",
      "confidence": 0.90,
      "last_updated": "2025-11-13T..."
    },
    "error_tolerance": {
      "preference": "high",
      "confidence": 0.95,
      "last_updated": "2025-11-13T..."
    }
  },
  
  "observed_patterns": {
    "what_works": [
      {
        "pattern": "Real code from project",
        "context": "API Key Management",
        "timestamp": "2025-11-12T...",
        "confidence": 0.95
      },
      {
        "pattern": "Show implementation, then explain pattern",
        "context": "Meeting Automation",
        "timestamp": "2025-11-10T...",
        "confidence": 0.90
      }
    ],
    "what_fails": [
      {
        "pattern": "Theoretical examples disconnected from work",
        "context": "Early tutorials",
        "timestamp": "2025-11-08T...",
        "confidence": 0.85
      },
      {
        "pattern": "Long explanations before showing",
        "context": "Protocol introduction",
        "timestamp": "2025-11-09T...",
        "confidence": 0.80
      }
    ]
  },
  
  "teaching_moments": {
    "successful": [
      {
        "topic": "API Key Management",
        "approach": "show_and_explain",
        "timestamp": "2025-11-12T...",
        "rating": 5,
        "notes": "User got it immediately, no confusion"
      }
    ],
    "unsuccessful": [
      {
        "topic": "Theoretical concepts",
        "approach": "explain_first",
        "timestamp": "2025-11-08T...",
        "rating": 2,
        "notes": "User disengaged, asked to 'just do it'"
      }
    ]
  },
  
  "adaptations": {
    "recent_changes": [
      {
        "dimension": "interaction_style",
        "from": "explain_first",
        "to": "show_and_explain",
        "reason": "User consistently prefers doing first",
        "timestamp": "2025-11-10T..."
      }
    ]
  }
}
```

---

### **Layer 3: Learning Engine (Adaptive)**

**File:** `8825_core/brain/learning_engine.py`

**Functionality:**
```python
class LearningEngine:
    """
    Observes user interactions and updates learning profile
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.profile = self.load_profile()
    
    def load_profile(self) -> LearningProfile:
        """Load user's learning profile or create default"""
        profile_path = get_user_dir(self.user_id) / 'profile' / 'learning_profile.json'
        
        if profile_path.exists():
            return LearningProfile.from_json(profile_path)
        else:
            return self.create_default_profile()
    
    def create_default_profile(self) -> LearningProfile:
        """Create default profile for new users"""
        return LearningProfile(
            information_density='moderate',
            example_preference='concrete',
            depth_approach='top_down',
            interaction_style='show_and_explain',
            error_tolerance='medium',
            confidence=0.5  # Low confidence, will adjust
        )
    
    def observe_interaction(self, interaction: Interaction):
        """Track user interaction and update profile"""
        # Detect signals
        signals = self.detect_signals(interaction)
        
        # Update preferences based on signals
        if signals.understanding:
            self.reinforce_current_approach()
        elif signals.confusion:
            self.adjust_approach()
        elif signals.boredom:
            self.increase_pace()
        elif signals.overwhelm:
            self.decrease_complexity()
    
    def suggest_teaching_approach(self, topic: str) -> TeachingApproach:
        """Suggest best approach based on profile"""
        return TeachingApproach(
            density=self.profile.information_density,
            examples=self.profile.example_preference,
            depth=self.profile.depth_approach,
            style=self.profile.interaction_style,
            confidence=self.calculate_confidence()
        )
    
    def track_teaching_moment(self, moment: TeachingMoment):
        """Record outcome of teaching moment"""
        self.profile.add_teaching_moment(moment)
        
        if moment.successful:
            self.reinforce_approach(moment.approach)
        else:
            self.adjust_approach(moment.approach)
        
        self.save_profile()
    
    def calculate_confidence(self) -> float:
        """Calculate confidence in current profile"""
        # Based on:
        # - Number of successful teaching moments
        # - Consistency of preferences
        # - Time since last adjustment
        pass
```

---

## Migration Strategy

### **Phase 1: Extract Core Principles (1 hour)**

1. **Review current protocol**
   - Identify universal principles
   - Identify Justin-specific content
   - Create separation plan

2. **Refactor protocol**
   - Keep only universal content
   - Remove all "Justin's..." sections
   - Add examples that are generic

3. **Create reference**
   - Document what was moved where
   - Update protocol README

### **Phase 2: Create User Profile System (2 hours)**

1. **Define profile schema**
   - JSON structure
   - All dimensions
   - Confidence scores
   - Observation tracking

2. **Create Justin's profile**
   - Extract current preferences
   - Convert to JSON
   - Save to `users/justin_harmon/profile/learning_profile.json`

3. **Create profile utilities**
   - Load profile
   - Save profile
   - Update profile
   - Query profile

### **Phase 3: Build Learning Engine (3 hours)**

1. **Create learning_engine.py**
   - Profile loading
   - Default profile generation
   - Observation tracking
   - Adaptation logic

2. **Integrate with brain**
   - Connect to brain daemon
   - Track interactions
   - Update profiles
   - Log changes

3. **Create CLI tools**
   - View profile: `8825 profile view`
   - Update profile: `8825 profile update`
   - Reset profile: `8825 profile reset`

### **Phase 4: Integration (2 hours)**

1. **Update protocols**
   - Reference user profile
   - Use profile in teaching modes
   - Remove hardcoded preferences

2. **Update agents**
   - Brain learning exporter
   - Teaching moments tracker
   - Adaptation suggestions

3. **Test with new user**
   - Create test user
   - Verify default profile
   - Simulate learning
   - Verify adaptation

### **Phase 5: Documentation (1 hour)**

1. **Update LEARNING_FUNDAMENTALS_PROTOCOL.md**
   - Remove user-specific content
   - Add profile reference
   - Document how to customize

2. **Create profile documentation**
   - How profiles work
   - How to view/edit profile
   - How system learns
   - Privacy considerations

---

## File Structure

```
8825-system/
├── 8825_core/
│   ├── protocols/
│   │   └── LEARNING_FUNDAMENTALS_PROTOCOL.md  # Universal principles only
│   └── brain/
│       ├── learning_engine.py                  # Adaptive learning system
│       └── profile_manager.py                  # Profile CRUD operations
│
├── users/
│   ├── justin_harmon/
│   │   └── profile/
│   │       ├── learning_profile.json           # Justin's preferences
│   │       └── teaching_history.json           # Justin's teaching moments
│   └── {new_user}/
│       └── profile/
│           ├── learning_profile.json           # Starts with defaults
│           └── teaching_history.json           # Builds over time
│
└── 8825_core/templates/
    └── user_profile_template.json              # Default for new users
```

---

## Default Profile for New Users

```json
{
  "user_id": "new_user",
  "created_at": "2025-11-13T...",
  "learning_preferences": {
    "information_density": {
      "preference": "moderate",
      "confidence": 0.5
    },
    "example_preference": {
      "preference": "concrete",
      "confidence": 0.5
    },
    "depth_approach": {
      "preference": "top_down",
      "confidence": 0.5
    },
    "interaction_style": {
      "preference": "show_and_explain",
      "confidence": 0.5
    },
    "error_tolerance": {
      "preference": "medium",
      "confidence": 0.5
    }
  },
  "observed_patterns": {
    "what_works": [],
    "what_fails": []
  },
  "teaching_moments": {
    "successful": [],
    "unsuccessful": []
  }
}
```

**Defaults are:**
- Middle-of-the-road preferences
- Low confidence (will adapt quickly)
- Based on most common learning styles
- Can be adjusted during onboarding

---

## Onboarding Enhancement

Add to `scripts/onboard.sh`:

```bash
# Learning Style Assessment (optional)
echo "Let's learn how you learn!"
echo ""
echo "1. When learning something new, do you prefer:"
echo "   a) See it working first, then understand why"
echo "   b) Understand the theory first, then see it"
echo "   c) Jump in and figure it out as I go"

read -p "Choice (a/b/c): " learning_style

# Update profile based on answers
python3 8825_core/brain/profile_manager.py --init \
  --interaction-style "$learning_style" \
  --user "$USERNAME"
```

---

## API / CLI

### **View Profile:**
```bash
8825 profile view
# Shows current learning preferences with confidence scores
```

### **Update Profile:**
```bash
8825 profile update --dimension information_density --value dense
```

### **Reset Profile:**
```bash
8825 profile reset
# Starts learning from scratch
```

### **Export Profile:**
```bash
8825 profile export --format json
# For sharing or backup
```

---

## Benefits

### **For Justin:**
- ✅ Your preferences preserved
- ✅ Can continue using system as-is
- ✅ System still knows your style

### **For New Users:**
- ✅ Start with sensible defaults
- ✅ System learns their style
- ✅ Not forced into Justin's preferences

### **For System:**
- ✅ Scalable to N users
- ✅ Each user gets personalized experience
- ✅ Core principles remain universal
- ✅ Learning improves over time

---

## Privacy Considerations

**Learning profiles contain:**
- Teaching preferences
- Interaction patterns
- Success/failure patterns

**Stored:**
- Locally in user directory
- Never shared without consent
- User can view/edit/delete anytime

**Brain system:**
- Observes interactions
- Updates local profile only
- No external transmission

---

## Testing Strategy

### **Test 1: Extract Justin's Profile**
- Run extraction script
- Verify all preferences captured
- Verify confidence scores accurate

### **Test 2: Create New User**
- Create test user
- Verify default profile created
- Verify low confidence scores

### **Test 3: Simulate Learning**
- Feed synthetic interactions
- Verify profile updates
- Verify confidence increases

### **Test 4: Teaching Mode**
- Trigger teaching moment
- Verify uses correct profile
- Verify adapts based on signals

---

## Timeline

- **Phase 1:** Extract core principles (1 hour)
- **Phase 2:** Create profile system (2 hours)
- **Phase 3:** Build learning engine (3 hours)
- **Phase 4:** Integration (2 hours)
- **Phase 5:** Documentation (1 hour)

**Total:** 9 hours over 2-3 sessions

---

## Success Criteria

**Separation is successful when:**
- ✅ Core protocol has no user-specific content
- ✅ Justin's preferences in his profile
- ✅ New users get default profile
- ✅ System learns from interactions
- ✅ Teaching adapts per user
- ✅ Profiles can be viewed/edited

**System is working when:**
- ✅ Justin's experience unchanged
- ✅ New user gets personalized over time
- ✅ Teaching moments tracked per user
- ✅ Confidence scores increase with data
- ✅ Adaptation happens automatically

---

## Next Steps

### **Immediate:**
1. Review this plan
2. Approve approach
3. Start Phase 1 (extract core principles)

### **This Week:**
1. Complete Phases 1-2 (profile system)
2. Test with Justin's profile
3. Verify no regression

### **Next Week:**
1. Complete Phases 3-4 (learning engine)
2. Test with new user
3. Document system

---

**This creates foundation for true multi-user system while preserving your personalized experience.**

**Ready to start Phase 1?**
