# Accountability Loop Agent - Examples

**Quick Start:** Add loops for things you want to be held accountable for.

---

## Example 1: Exercise

```bash
# Add exercise loop
python3 accountability_loop_agent.py \
  --add "Exercise" \
  --description "Stay active and healthy" \
  --metric-name "Workouts" \
  --metric-target 3 \
  --metric-unit "sessions/week"

# Update after workout
python3 accountability_loop_agent.py \
  --update exercise \
  --metric "Workouts" \
  --value 2

# Check status
python3 accountability_loop_agent.py --check exercise
```

**Output:**
```
⚠️ Exercise: Workouts at 67% of target (2.0/3.0 sessions/week)
   💡 Need 1.0 more sessions/week. Still recoverable with focused effort.
```

---

## Example 2: HCSS Meeting Processing

```bash
# Add HCSS health loop
python3 accountability_loop_agent.py \
  --add "HCSS Health" \
  --description "Meeting automation reliability" \
  --metric-name "Success Rate" \
  --metric-target 100 \
  --metric-unit "percent"

# Update with current success rate
python3 accountability_loop_agent.py \
  --update hcss_health \
  --metric "Success Rate" \
  --value 95 \
  --trend stable

# Check status
python3 accountability_loop_agent.py --check hcss_health
```

**Output:**
```
✅ HCSS Health: Success Rate target achieved! (95.0/100.0 percent)
```

---

## Example 3: Joju User Growth

```bash
# Add Joju validation loop
python3 accountability_loop_agent.py \
  --add "Joju Users" \
  --description "User acquisition and growth" \
  --metric-name "Active Users" \
  --metric-target 20 \
  --metric-unit "users"

# Update with current user count
python3 accountability_loop_agent.py \
  --update joju_users \
  --metric "Active Users" \
  --value 8 \
  --trend increasing

# Check status
python3 accountability_loop_agent.py --check joju_users
```

**Output:**
```
🔴 Joju Users: Active Users at 40% of target (8.0/20.0 users)
   💡 Need 12.0 more users to reach target. Consider immediate action.
```

---

## Example 4: Weekly Relationship Check-ins

```bash
# Add relationship loop
python3 accountability_loop_agent.py \
  --add "Relationships" \
  --description "Stay connected with key people" \
  --metric-name "Check-ins" \
  --metric-target 5 \
  --metric-unit "contacts/week"

# Update after reaching out
python3 accountability_loop_agent.py \
  --update relationships \
  --metric "Check-ins" \
  --value 3

# Check status
python3 accountability_loop_agent.py --check relationships
```

**Output:**
```
⚠️ Relationships: Check-ins at 60% of target (3.0/5.0 contacts/week)
   💡 Need 2.0 more contacts/week. Still recoverable with focused effort.
```

---

## Example 5: Learning Goals

```bash
# Add learning loop
python3 accountability_loop_agent.py \
  --add "Python Practice" \
  --description "Build Python skills" \
  --metric-name "Practice Sessions" \
  --metric-target 3 \
  --metric-unit "sessions/week"

# Update after practice
python3 accountability_loop_agent.py \
  --update python_practice \
  --metric "Practice Sessions" \
  --value 1 \
  --trend decreasing

# Check status
python3 accountability_loop_agent.py --check python_practice
```

**Output:**
```
🔴 Python Practice: Practice Sessions at 33% of target (1.0/3.0 sessions/week)
   💡 Need 2.0 more sessions/week to reach target. Consider immediate action.
⚠️ Python Practice: Practice Sessions trending down
   💡 Investigate cause of decline
```

---

## Check All Loops

```bash
# Check everything at once
python3 accountability_loop_agent.py --check-all
```

**Output:**
```
Checking all accountability loops...

## Exercise

⚠️ Exercise: Workouts at 67% of target (2.0/3.0 sessions/week)
   💡 Need 1.0 more sessions/week. Still recoverable with focused effort.

## Joju Users

🔴 Joju Users: Active Users at 40% of target (8.0/20.0 users)
   💡 Need 12.0 more users to reach target. Consider immediate action.

## Python Practice

🔴 Python Practice: Practice Sessions at 33% of target (1.0/3.0 sessions/week)
   💡 Need 2.0 more sessions/week to reach target. Consider immediate action.
⚠️ Python Practice: Practice Sessions trending down
   💡 Investigate cause of decline
```

---

## Status Report

```bash
# Get full status report
python3 accountability_loop_agent.py --status
```

**Output:**
```markdown
# Accountability Loops Status

**Checked:** 2025-11-13 19:00

## 🟢 On Track

- **HCSS Health**: All metrics meeting targets

## 🟡 At Risk

### Exercise
- Workouts: 67% of target (2.0/3.0 sessions/week)

### Relationships
- Check-ins: 60% of target (3.0/5.0 contacts/week)

## 🔴 Off Track

### Joju Users
- Active Users: 40% of target (8.0/20.0 users)

**Alerts:**
- 🔴 Joju Users: Active Users at 40% of target (8.0/20.0 users)
   💡 Need 12.0 more users to reach target. Consider immediate action.

### Python Practice
- Practice Sessions: 33% of target (1.0/3.0 sessions/week)

**Alerts:**
- 🔴 Python Practice: Practice Sessions at 33% of target (1.0/3.0 sessions/week)
   💡 Need 2.0 more sessions/week to reach target. Consider immediate action.
- ⚠️ Python Practice: Practice Sessions trending down
   💡 Investigate cause of decline
```

---

## List All Loops

```bash
# See all configured loops
python3 accountability_loop_agent.py --list
```

**Output:**
```
# Accountability Loops

🟢 [✓] HCSS Health (hcss_health)
   Meeting automation reliability
   Metrics: 1 | Check: daily
   Last checked: 2025-11-13 19:00

🟡 [✓] Exercise (exercise)
   Stay active and healthy
   Metrics: 1 | Check: daily
   Last checked: 2025-11-13 19:00

🔴 [✓] Joju Users (joju_users)
   User acquisition and growth
   Metrics: 1 | Check: daily
   Last checked: 2025-11-13 19:00
```

---

## Advanced: Multiple Metrics

You can manually edit `~/.8825/accountability_loops.json` to add multiple metrics:

```json
{
  "joju_validation": {
    "id": "joju_validation",
    "name": "Joju Validation",
    "description": "Complete validation loop for Joju",
    "metrics": [
      {
        "name": "Active Users",
        "current": 8,
        "target": 20,
        "unit": "users"
      },
      {
        "name": "Referrals",
        "current": 2,
        "target": 5,
        "unit": "referrals/week"
      },
      {
        "name": "Pricing Acceptance",
        "current": 60,
        "target": 70,
        "unit": "percent"
      }
    ],
    "check_frequency": "daily",
    "data_source": "joju_database",
    "enabled": true
  }
}
```

Then check:
```bash
python3 accountability_loop_agent.py --check joju_validation
```

**Output:**
```
🔴 Joju Validation: Active Users at 40% of target (8.0/20.0 users)
   💡 Need 12.0 more users to reach target. Consider immediate action.
⚠️ Joju Validation: Referrals at 40% of target (2.0/5.0 referrals/week)
   💡 Need 3.0 more referrals/week. Still recoverable with focused effort.
⚠️ Joju Validation: Pricing Acceptance at 86% of target (60.0/70.0 percent)
   💡 Need 10.0 more percent. Still recoverable with focused effort.
```

---

## Automation Ideas

### Daily Check (via cron)
```bash
# Add to crontab
0 9 * * * cd /path/to/8825_core/agents && python3 accountability_loop_agent.py --check-all > /tmp/accountability_report.txt && cat /tmp/accountability_report.txt
```

### Weekly Report (via cron)
```bash
# Every Monday at 9am
0 9 * * 1 cd /path/to/8825_core/agents && python3 accountability_loop_agent.py --status > ~/weekly_accountability_$(date +\%Y-\%m-\%d).md
```

### Integration with Brain Daemon
Add to brain daemon to check loops automatically and store alerts in brain state.

---

## Common Patterns

### Pattern 1: Weekly Goals
```bash
# Exercise, relationships, learning
--metric-target 3 --metric-unit "sessions/week"
--metric-target 5 --metric-unit "contacts/week"
--metric-target 3 --metric-unit "hours/week"
```

### Pattern 2: Success Rates
```bash
# HCSS, deployments, tests
--metric-target 100 --metric-unit "percent"
--metric-target 95 --metric-unit "percent"
```

### Pattern 3: Growth Metrics
```bash
# Users, revenue, content
--metric-target 20 --metric-unit "users"
--metric-target 5000 --metric-unit "dollars/month"
--metric-target 10 --metric-unit "posts/month"
```

### Pattern 4: Time-Based
```bash
# Response time, processing time
--metric-target 24 --metric-unit "hours"
--metric-target 60 --metric-unit "seconds"
```

---

## Next Steps

1. **Add your first loop** - Start with something simple (exercise, meetings)
2. **Update daily** - Make it a habit to update metrics
3. **Review weekly** - Check status report every Monday
4. **Automate updates** - Connect to data sources (databases, APIs)
5. **Expand** - Add more loops as you find value

**The agent holds you accountable. You just need to feed it data.**
