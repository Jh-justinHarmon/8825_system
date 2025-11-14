# Jh COMMs - Chat-Based Protocol

**Version:** 1.1.0  
**Created:** 2025-11-11  
**Status:** Active

---

## 🎯 Philosophy

**Three options → Lane selection → Refinement**

When working through chat (vs CLI tool):
- Start with context analysis
- Generate three response options (brief/standard/detailed)
- User selects a lane
- Refine iteratively based on feedback
- Present final version with copy-ready formatting

---

## 📋 Chat Workflow

### 1. Initial Request
User provides:
- Screenshot or text of message
- Basic context (optional)

### 2. Context Analysis (Show)
Display understanding:
```
**From:** [Name/Source]
**Type:** [Professional/Personal]
**Context:** [Key details]
**Sentiment:** [Tone]
```

### 3. Initial Response Generation
Provide THREE response options:
- Brief (concise)
- Standard (balanced)
- Detailed (thorough)

User selects a lane to work from.

### 4. Refinement Phase (After Lane Selection)
**Key principle:** Once in refinement, stay in refinement lane

**Do NOT:**
- Re-offer all three options
- Restart the process
- Over-explain changes

**DO:**
- Make requested changes
- Show updated version
- Ask "Good?" or similar brief confirmation
- Keep momentum

### 5. Final Delivery
Present in copy-ready format:
```
## Final Response

[Wrapped version for readability]
[60-80 char line breaks]

**Copy-ready version:**
```
[Single-line version for copying]
```
```

Click copy icon to copy to clipboard.

---

## 🔄 Refinement Examples

### ❌ Wrong Approach
```
User: "Remove this part"
AI: "Here are three new options:
     1. BRIEF...
     2. STANDARD...
     3. DETAILED..."
```

### ✅ Right Approach
```
User: "Remove this part"
AI: "[Updated response with change]
     Good?"
```

---

## 💡 Key Principles

### 1. Three Options Start
- Analyze context
- Generate THREE responses (brief/standard/detailed)
- User selects lane
- THEN refine from there

### 2. Stay in Refinement Lane
- Once editing starts, keep editing
- No re-offering all options
- Quick iterations
- Maintain flow

### 3. Copy-Ready Formatting
- Wrapped version (readability)
- Single-line version (copying)
- Code blocks with copy icons
- No manual selection needed

### 4. Minimal Friction
- Brief confirmations ("Good?")
- Quick iterations
- No over-explanation
- Fast turnaround

---

## 🎨 Response Formatting

### Standard Format
```markdown
## Final Response

```
[Wrapped at 60-80 chars for readability]
```

**Copy-ready version:**
```
[Single line, no breaks, ready to paste]
```
```

### Why Both Versions?
- **Wrapped:** Easy to read and review in chat
- **Single-line:** Direct copy/paste into SMS/email/Slack
- **Code blocks:** Built-in copy buttons in IDE

---

## 📊 Context Analysis Template

```markdown
**From:** [Name/Organization]
**Phone/Email:** [Contact info if relevant]
**Time:** [When received]
**Type:** [Professional/Personal/Client]

**Context:**
- [Key detail 1]
- [Key detail 2]
- [Key detail 3]

**Message Type:** [Request/Confirmation/Update/Question]
**Urgency:** [High/Medium/Low]
**Formality:** [Casual/Professional/Formal]
**Sentiment:** [Positive/Neutral/Negative]
```

---

## 🔧 Refinement Patterns

### Pattern 1: Content Changes
```
User: "Remove X, add Y"
AI: [Updated response]
    Good?
```

### Pattern 2: Tone Adjustments
```
User: "Make it more casual"
AI: [Adjusted response]
    Better?
```

### Pattern 3: Length Changes
```
User: "Shorter"
AI: [Condensed response]
    Work?
```

### Pattern 4: Reframing
```
User: "She doesn't know about X yet, reframe"
AI: [Reframed response]
    Good?
```

---

## 🎯 Success Criteria

**Good chat session:**
- ✅ Quick context analysis
- ✅ Three initial options
- ✅ Lane selection
- ✅ Fast refinement iterations
- ✅ Copy-ready final format
- ✅ No re-offering options during refinement

**Poor chat session:**
- ❌ Multiple options every time
- ❌ Restarting process after feedback
- ❌ Over-explaining changes
- ❌ No copy-ready format
- ❌ Too much friction

---

## 📝 Learning Notes

### What to Track (Silently)
- Context patterns that lead to refinement
- Common adjustment types
- User's tone preferences
- Formality patterns by contact type
- Length preferences by situation

### What NOT to Show
- "I learned that you prefer..."
- "Based on past interactions..."
- "The system recommends..."
- Analysis details during refinement

---

## 🚀 Quick Reference

**Initial request** → Context analysis → Three options  
**Lane selection** → User picks one  
**Refinement** → Quick edits → Brief confirmation  
**Final** → Wrapped + copy-ready versions  
**Done** → Move on

---

**This is the chat protocol: Fast, focused, frictionless.** 🚀
