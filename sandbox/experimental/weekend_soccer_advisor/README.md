# Weekend Soccer Advisor - PoC

**Status:** 🔴 Not Started  
**Created:** 2025-11-09  
**Owner:** Justin Harmon

---

## 🎯 GOAL

Automated weekend soccer game advisor that:
1. Detects soccer games on calendar
2. Calculates travel time + buffer
3. Notifies when to leave
4. Learns from history to improve accuracy

---

## 📋 REQUIREMENTS

### **Functional:**
- ✅ Detect weekend events with "Soccer" tag
- ✅ Calculate travel time using Maps API
- ✅ Account for 45-minute early arrival requirement
- ✅ Add 10-minute buffer
- ✅ Send "leave by" notification
- ✅ Friday evening weekend preview

### **Technical:**
- Google Calendar API (read events)
- Google Maps API (travel time)
- Notification system (alerts)
- History tracking (optional: learn from actuals)

### **User Experience:**
- Friday 5pm: "This weekend's soccer schedule"
- Game day: "Leave by X:XX for [Game Name]"
- Optional: Traffic updates if delays

---

## 🏗️ AVAILABLE COMPONENTS

### **Already Built (v3.0):**
- ✅ Google Calendar integration (read/write)
- ✅ Google Maps API access
- ✅ Event detection (calendar queries)
- ✅ Notification system (alerts)

### **Need to Build:**
- 🔧 Weekend event filter
- 🔧 Travel time calculator
- 🔧 "Leave by" logic (start - 45m - travel - buffer)
- 🔧 Notification scheduler
- 🔧 Weekend preview generator

---

## 📊 VALIDATION CRITERIA

### **Must Have:**
- [ ] Correctly detects all weekend soccer events
- [ ] Calculates accurate travel time
- [ ] Sends notifications at correct time
- [ ] Handles missing location data gracefully
- [ ] Works for both Saturday and Sunday games

### **Should Have:**
- [ ] Friday preview shows full weekend schedule
- [ ] Accounts for traffic conditions
- [ ] Adjusts for different game types (practice vs game)
- [ ] Sends reminder if Justin hasn't left on time

### **Nice to Have:**
- [ ] Learns from actual departure times
- [ ] Suggests earlier departure if traffic is bad
- [ ] Integrates with family calendar
- [ ] Weather warnings for outdoor games

---

## 🔄 WORKFLOW DESIGN

### **Friday Preview (5pm):**
```
1. Query calendar: Saturday + Sunday
2. Filter: events containing "Soccer"
3. For each game:
   - Extract: time, location, type
   - Calculate: travel time + buffer
   - Determine: leave by time
4. Generate: Weekend preview message
5. Send: Notification to Justin
```

### **Game Day Alert:**
```
1. Detect: Soccer event today
2. Calculate: leave_by = start - 45m - travel - 10m
3. Schedule: notification at (leave_by - 10m)
4. Send: "Leave by X:XX for [Game Name]"
5. Optional: Traffic check at leave_by
```

---

## 🧪 TEST CASES

### **Test 1: Saturday Morning Game**
- Event: "Soccer Game" @ 10:00 AM
- Location: Field 20 minutes away
- Expected: Leave by 8:55 AM (10:00 - 0:45 - 0:20 - 0:10)
- Alert: 8:45 AM ("Leave in 10 minutes")

### **Test 2: Sunday Afternoon Practice**
- Event: "Soccer Practice" @ 2:00 PM
- Location: Same field (20 min)
- Expected: Leave by 12:55 PM
- Alert: 12:45 PM

### **Test 3: No Location Data**
- Event: "Soccer Game" @ 10:00 AM
- Location: Missing
- Expected: Use default field or skip calculation
- Alert: Generic "Check event location"

### **Test 4: Friday Preview**
- Weekend has 2 games (Sat 10am, Sun 2pm)
- Expected: Both shown in preview
- Sent: Friday 5pm

### **Test 5: Traffic Delay**
- Normal travel: 20 min
- With traffic: 35 min
- Expected: Adjust leave_by accordingly
- Alert: Earlier departure time

---

## 📁 IMPLEMENTATION PLAN

### **Phase 1: Basic Detection** (1 hour)
- Calendar query for weekend events
- Filter by "Soccer" keyword
- Extract time and location

### **Phase 2: Travel Calculation** (1 hour)
- Maps API integration
- Calculate travel time
- Add 45min early + 10min buffer
- Determine leave_by time

### **Phase 3: Notifications** (1 hour)
- Friday preview generator
- Game day alert scheduler
- Send notifications

### **Phase 4: Validation** (Testing)
- Test with real calendar data
- Verify calculations accurate
- Confirm notifications work
- Get Justin's feedback

---

## 🚀 GRADUATION CRITERIA

**Ready to promote to workflows/ when:**
- ✅ All "Must Have" validation criteria met
- ✅ Tested with real weekend schedule
- ✅ Justin confirms it's useful
- ✅ No critical bugs
- ✅ Documentation complete

---

## 📝 NOTES

**Key Insight from Analysis:**
- All infrastructure components exist (Calendar, Maps, Notifications)
- This is an **assembly problem**, not a development problem
- Estimated effort: 3-4 hours total

**Critical Questions:**
1. What's Justin's typical "leave by" time? (start - 45min)
2. Does this apply to both games and practices?
3. Which family members need notifications?
4. Default field location if not specified?

**Dependencies:**
- Google Calendar API (✅ available)
- Google Maps API (✅ available)
- Notification system (✅ available)

---

## 🔗 RELATED

- Infrastructure: `8825_core/integrations/google/`
- Calendar integration: Already built
- Maps API: Already available
- Future: Could extend to other kid activities

---

**PoC created. Ready for implementation.** 🚀
