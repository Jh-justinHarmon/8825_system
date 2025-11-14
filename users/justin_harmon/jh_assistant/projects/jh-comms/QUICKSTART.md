# Jh Assistant - Quick Start

**Get started in 5 minutes!**

---

## 🚀 Installation

### 1. Install Dependencies
```bash
pip3 install pytesseract Pillow
brew install tesseract
```

### 2. Make Scripts Executable
```bash
cd /Users/justinharmon/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/windsurf-project\ -\ 8825\ version\ 2.0/Jh_sandbox/projects/jh-assistant

chmod +x scripts/*.py
chmod +x core/*.py
```

---

## 🎯 Basic Usage

### From Screenshot
```bash
python3 scripts/rapid_response.py --screenshot ~/Desktop/message.png
```

### From Text
```bash
python3 scripts/rapid_response.py --text "Can you send me the report by EOD?"
```

### Interactive Mode
```bash
python3 scripts/rapid_response.py --interactive
```

### With Contact Context
```bash
python3 scripts/rapid_response.py --screenshot ~/Desktop/message.png --contact "John"
```

---

## 📋 What It Does

1. **Extracts text** from screenshot (OCR)
2. **Analyzes context** (sentiment, urgency, message type)
3. **Looks up contact** (if name provided)
4. **Generates 3 responses**:
   - Brief (1-2 sentences)
   - Standard (2-4 sentences)
   - Detailed (4-6 sentences)
5. **Copies to clipboard** (your choice)

---

## 💡 Example Session

```bash
$ python3 scripts/rapid_response.py --text "Hey, can you review this doc when you get a chance?" --interactive

🚀 Rapid Response Tool
============================================================

📋 Extracted text (50 characters)
------------------------------------------------------------
Hey, can you review this doc when you get a chance?
------------------------------------------------------------

🔍 Analyzing context...
   Type: request
   Sentiment: neutral
   Urgency: low
   Requires action: True

💬 Generating responses...

============================================================
RESPONSE OPTIONS
============================================================

1. BRIEF (7 words)
------------------------------------------------------------
On it. I'll have this to you soon.

2. STANDARD (29 words)
------------------------------------------------------------
Absolutely, I'm on it. I'll prioritize this and have it to you within the next few hours. I'll send you a quick update if anything comes up.

3. DETAILED (58 words)
------------------------------------------------------------
Absolutely, I'm happy to help with this. I'll prioritize this request and start working on it right away. Based on what you've shared, I should be able to have this completed within the next few hours. I'll keep you updated on my progress and let you know immediately if I run into any issues or need clarification on anything. Thanks for trusting me with this, I'll make sure it's done well.

============================================================

Select response (1-3) or press Enter to skip: 2

📋 Copied to clipboard!

✅ STANDARD response copied to clipboard!
```

---

## 👥 Managing Contacts

### Add a Contact
```python
from core.contact_matrix import ContactMatrix

matrix = ContactMatrix()

contact_id = matrix.add_contact({
    'name': 'Jane Smith',
    'email': 'jane@example.com',
    'relationship_type': 'professional',
    'closeness': 8,
    'formality': 'professional',
    'communication_style': 'friendly'
})
```

### List Contacts
```python
contacts = matrix.list_contacts()
for contact in contacts:
    print(f"{contact['name']} - {contact['relationship']['type']}")
```

### Find Contact
```python
contact = matrix.find_contact(name="Jane")
print(contact)
```

---

## ⚙️ Customization

### Voice Profile
Edit `data/voice_profile.json` to customize your communication style:

```json
{
  "tone": "professional_friendly",
  "formality": "medium",
  "verbosity": "medium",
  "personality_traits": ["direct", "helpful", "thoughtful"],
  "common_phrases": ["Happy to help", "Let me know"],
  "avoid_phrases": ["As per my last email"]
}
```

### Contact Matrix
Edit `data/contact_matrix.json` to add/modify contacts

---

## 🎯 Use Cases

### Quick Email Responses
```bash
# Take screenshot of email
# Run tool
python3 scripts/rapid_response.py --screenshot ~/Desktop/email.png

# Select response
# Paste into email client
```

### Slack/Discord Messages
```bash
# Screenshot conversation
python3 scripts/rapid_response.py --screenshot ~/Desktop/slack.png --contact "TeamMember"

# Get contextually appropriate response
# Paste into chat
```

### Text Messages
```bash
# Screenshot message thread
python3 scripts/rapid_response.py --screenshot ~/Desktop/imessage.png

# Choose response level
# Send message
```

---

## 🔧 Testing Components

### Test Context Analyzer
```bash
python3 core/context_analyzer.py
```

### Test Response Generator
```bash
python3 core/response_generator.py
```

### Test Contact Matrix
```bash
python3 core/contact_matrix.py
```

---

## 📊 Tips

1. **Take clear screenshots** - Better OCR results
2. **Add contacts** - Better context-aware responses
3. **Use interactive mode** - Choose best response
4. **Review and edit** - Responses are starting points
5. **Log interactions** - System learns over time

---

## 🚧 Roadmap

### Phase 1: Desktop CLI ✅ (Current)
- Screenshot OCR
- Context analysis
- Response generation
- Contact matrix
- Clipboard integration

### Phase 2: Learning Engine (Next)
- Track response success
- Learn from corrections
- Improve voice matching
- Adapt to preferences

### Phase 3: iOS App (Future)
- Share sheet integration
- Native UI
- Offline mode
- iCloud sync

---

## 🔒 Privacy

- All data stored locally
- No cloud sync by default
- You control all information
- Contact matrix is private

---

**Your personal AI assistant is ready!** 🚀

**Start with:** `python3 scripts/rapid_response.py --interactive`
