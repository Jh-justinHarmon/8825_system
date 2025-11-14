# Weekend Soccer Advisor - Quick Start

**Status:** 🟢 Ready to Test  
**Built:** 2025-11-09

---

## 🚀 QUICK TEST

### **Option 1: Direct Command Line**

```bash
cd users/justin_harmon/jh_assistant/poc/weekend_soccer_advisor/implementation
./test_advisor.sh
```

**What it does:**
- Scans your calendar for weekend soccer events
- Calculates travel time for each game
- Shows when to leave (game time - 45min - travel - 10min buffer)
- Saves results to `~/Downloads/soccer_schedule.json`

---

### **Option 2: Via MCP (Windsurf/Goose)**

Just ask:
```
> "Show me my weekend soccer schedule"
```

Or explicitly:
```
> Use the soccer_weekend_preview tool
```

---

## 📋 WHAT YOU'LL SEE

### **Example Output:**

```
⚽ Weekend Soccer Schedule
==================================================

📍 Soccer Game
   Saturday at 10:00 AM
   Location: Field Complex, 123 Main St
   🚗 Leave by: 08:55 AM
   (Travel: 20 min + 45 min early + 10 min buffer)

📍 Soccer Practice
   Sunday at 02:00 PM
   Location: Same field
   🚗 Leave by: 12:55 PM
   (Travel: 20 min + 45 min early + 10 min buffer)
```

---

## ⚙️ CONFIGURATION

### **Optional: Google Maps API**

For accurate travel times, set your Maps API key:

```bash
export GOOGLE_MAPS_API_KEY=your_key_here
```

**Without API key:** Uses default 20-minute travel time

---

### **Customizing Times:**

Edit `soccer_advisor.py` to adjust:

```python
EARLY_ARRIVAL_MINUTES = 45  # How early to arrive
BUFFER_MINUTES = 10         # Safety buffer
NOTIFICATION_ADVANCE_MINUTES = 10  # Alert timing
```

---

## 🧪 VALIDATION CHECKLIST

After running, verify:

- [ ] **Detects all soccer events** - Check both Saturday and Sunday
- [ ] **Correct game times** - Matches your calendar
- [ ] **Reasonable travel times** - Makes sense for your location
- [ ] **Leave-by times** - Early enough to arrive 45min before game
- [ ] **Output saved** - JSON file in Downloads

---

## 🐛 TROUBLESHOOTING

### **No events found**
- Make sure events have "Soccer" in the title
- Check calendar permissions
- Verify events are this weekend (not past)

### **Travel time always 20 minutes**
- Maps API key not set
- Location data missing from calendar event
- Maps API quota exceeded

### **Authentication error**
- Run from command line first to authenticate
- Check `8825_core/integrations/google/credentials.json` exists
- Token will be saved to `8825_core/integrations/google/token.json`

---

## 📊 OUTPUT FILES

**JSON Output:** `~/Downloads/soccer_schedule.json`

```json
{
  "events": [
    {
      "name": "Soccer Game",
      "start": "2025-11-09T10:00:00",
      "location": "Field Complex"
    }
  ],
  "preview": "⚽ Weekend Soccer Schedule...",
  "generated_at": "2025-11-09T19:32:00"
}
```

---

## 🎯 NEXT PHASE

**After 2 weekends of testing:**

If it's useful and accurate:
- ✅ Graduate to `workflows/`
- ✅ Add automated Friday preview
- ✅ Add game-day notifications
- ✅ Integrate with family calendar

---

## 🆘 NEED HELP?

**Common Issues:**
1. **Calendar not found** → Check Google Calendar authentication
2. **No travel time** → Set GOOGLE_MAPS_API_KEY or accept default
3. **Wrong weekend** → Script finds NEXT weekend from current time
4. **Missing events** → Ensure "Soccer" is in event title

---

**Ready to test! Run `./test_advisor.sh` to get started.** 🚀
