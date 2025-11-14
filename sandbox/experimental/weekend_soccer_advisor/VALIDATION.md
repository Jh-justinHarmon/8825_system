# Weekend Soccer Advisor - Validation Checklist

**Status:** 🔴 Not Started  
**Last Updated:** 2025-11-09

---

## ✅ VALIDATION STAGES

### **Stage 1: Component Testing**

#### **Calendar Detection:**
- [ ] Can query calendar for weekend events
- [ ] Can filter by "Soccer" keyword
- [ ] Can extract event details (time, location, name)
- [ ] Handles multiple events in one weekend
- [ ] Handles no events gracefully

#### **Travel Calculation:**
- [ ] Can get travel time from Maps API
- [ ] Handles missing location data
- [ ] Accounts for traffic conditions
- [ ] Adds 45-minute early arrival buffer
- [ ] Adds 10-minute safety buffer

#### **Leave By Logic:**
- [ ] Calculates correct leave_by time
- [ ] Formula: start - 45min - travel - 10min
- [ ] Handles edge cases (games at weird times)
- [ ] Rounds to practical times (not 8:47, say 8:45)

#### **Notifications:**
- [ ] Can schedule notification
- [ ] Sends at correct time (leave_by - 10min)
- [ ] Message format is clear
- [ ] Includes game name and leave time
- [ ] Works for both SMS and push

---

### **Stage 2: Integration Testing**

#### **End-to-End Flow:**
- [ ] Friday preview generates correctly
- [ ] Game day alert triggers on time
- [ ] Full workflow runs without errors
- [ ] Handles multiple games per day
- [ ] Works for both Saturday and Sunday

#### **Error Handling:**
- [ ] Gracefully handles missing event data
- [ ] Falls back if Maps API fails
- [ ] Notifies if calculation impossible
- [ ] Logs errors for debugging
- [ ] Doesn't crash on bad data

---

### **Stage 3: Real-World Testing**

#### **Live Weekend Test:**
- [ ] Tested with real soccer schedule
- [ ] Friday preview sent successfully
- [ ] Game day alerts received on time
- [ ] Travel time calculations accurate
- [ ] Justin confirms usefulness

#### **Edge Cases:**
- [ ] Multiple games same day
- [ ] Back-to-back games
- [ ] Games at unusual times (early morning, late afternoon)
- [ ] Events with missing/incomplete data
- [ ] Calendar changes after preview sent

---

## 🎯 ACCEPTANCE CRITERIA

### **Must Pass:**
1. ✅ **Accuracy:** Travel time within 5 minutes of actual
2. ✅ **Reliability:** Notifications never missed
3. ✅ **Clarity:** Messages easy to understand
4. ✅ **Timeliness:** Alerts at useful times (not too early/late)
5. ✅ **Robustness:** Handles errors gracefully

### **Should Pass:**
1. ✅ **Traffic awareness:** Accounts for typical traffic
2. ✅ **Family friendly:** Works for all family schedules
3. ✅ **Flexible:** Easy to adjust buffer times
4. ✅ **Learnable:** Can improve from history

---

## 🧪 TEST SCENARIOS

### **Scenario 1: Perfect Weekend**
**Setup:**
- Saturday 10am: Soccer Game @ Field A (20 min away)
- Sunday 2pm: Soccer Practice @ Field B (15 min away)

**Expected Behavior:**
- Friday 5pm: Preview shows both games with leave times
- Saturday 8:45am: Alert "Leave by 8:55 for Soccer Game"
- Sunday 12:35pm: Alert "Leave by 12:45 for Soccer Practice"

**Pass Criteria:**
- [ ] Friday preview accurate
- [ ] Saturday alert on time
- [ ] Sunday alert on time
- [ ] Travel times reasonable
- [ ] Messages clear

---

### **Scenario 2: Last-Minute Change**
**Setup:**
- Saturday game moved from 10am to 11am on Friday night

**Expected Behavior:**
- System detects change
- Updates leave_by time
- Sends corrected alert

**Pass Criteria:**
- [ ] Detects calendar change
- [ ] Recalculates leave_by
- [ ] Sends updated notification
- [ ] No duplicate/stale alerts

---

### **Scenario 3: Missing Location**
**Setup:**
- Sunday game has no location specified

**Expected Behavior:**
- Friday preview shows "Location TBD"
- Saturday: Reminder to check location
- Skips travel calculation
- Generic notification

**Pass Criteria:**
- [ ] Doesn't crash on missing data
- [ ] Notifies about missing info
- [ ] Still shows game in preview
- [ ] Clear about what's missing

---

### **Scenario 4: Heavy Traffic**
**Setup:**
- Normal travel: 20 min
- Game day traffic: 35 min

**Expected Behavior:**
- Maps API returns traffic-adjusted time
- Leave_by calculated with 35 min travel
- Earlier departure alert

**Pass Criteria:**
- [ ] Uses real-time traffic data
- [ ] Adjusts leave_by accordingly
- [ ] Notifies if significantly different
- [ ] Prevents late arrival

---

## 📊 VALIDATION METRICS

### **Performance:**
- Calendar query: < 2 seconds
- Maps API call: < 3 seconds
- Total workflow: < 10 seconds
- Notification delivery: < 30 seconds

### **Accuracy:**
- Travel time: ±5 minutes of actual
- Leave_by calculation: exact (no rounding errors)
- Notification timing: ±1 minute of scheduled

### **Reliability:**
- Success rate: > 99%
- False negatives: 0 (never miss a game)
- False positives: < 1% (rare spurious alerts)

---

## 🚀 GRADUATION CHECKLIST

**Ready to promote when:**
- [ ] All Stage 1 tests pass
- [ ] All Stage 2 tests pass
- [ ] All Stage 3 tests pass
- [ ] All acceptance criteria met
- [ ] Justin confirms it's useful
- [ ] Documentation complete
- [ ] No critical bugs
- [ ] Code reviewed and clean

---

## 📝 VALIDATION LOG

### **Session 1: [Date]**
- [ ] Tests run: 
- [ ] Results: 
- [ ] Issues found: 
- [ ] Next steps: 

### **Session 2: [Date]**
- [ ] Tests run: 
- [ ] Results: 
- [ ] Issues found: 
- [ ] Next steps: 

---

**Validation plan ready. Start testing when implementation complete.** ✅
