# Automated Timesheet Generation from Meetings

**Status:** ✅ Production Ready  
**Integration:** Meeting Automation → Timesheet

---

## 🎯 WHAT IT DOES

Automatically generates timesheet data from meeting transcripts in **your exact format** - ready to copy/paste into your spreadsheet.

---

## 📊 SAMPLE OUTPUT

### **Week 1 (Ending 11/03/25)**
```
Client-Project  Mon     Tue     Wed     Thu     Fri     Sat     Sun     Total
                10/28   10/29   10/30   10/31   11/01   11/02   11/03
RAL                                     2.00            0.00    2.00
TGIF            1.00            1.50            1.25            3.75
HCSS                    0.75                                    0.75
────────────────────────────────────────────────────────────────────
TOTAL           1.00    0.75    1.50    2.00    1.25    0.00    6.50
```

### **Week 2 (Ending 11/10/25)**
```
Client-Project  Mon     Tue     Wed     Thu     Fri     Sat     Sun     Total
                11/04   11/05   11/06   11/07   11/08   11/09   11/10
RAL                             1.00            1.50            2.50
TGIF            1.00            1.50            2.00            4.50
HCSS                    2.00            0.75                    2.75
────────────────────────────────────────────────────────────────────
TOTAL           1.00    2.00    2.50    0.75    3.50    0.00    9.75
```

---

## 🔄 COMPLETE WORKFLOW

### **Step 1: Meetings Happen**
- Otter.ai transcribes automatically
- Dual-source manager retrieves transcripts
- Meeting processor saves with duration metadata

### **Step 2: Generate Timesheet**
```bash
cd users/justin_harmon/hcss/meeting_automation

# For current week (Sunday date)
python3 timesheet_generator.py \
  users/justin_harmon/hcss/knowledge/meetings \
  11/10/25 \
  HCSS TGIF RAL
```

### **Step 3: Copy to Spreadsheet**
- Output is tab-delimited
- Copy directly from terminal
- Paste into your spreadsheet
- Done!

---

## 🎮 USAGE

### **Basic Command**
```bash
python3 timesheet_generator.py <knowledge_base> <week_ending> [clients...]
```

### **Examples**

**All clients for week ending 11/10/25:**
```bash
python3 timesheet_generator.py \
  users/justin_harmon/hcss/knowledge/meetings \
  11/10/25
```

**Only HCSS and TGIF:**
```bash
python3 timesheet_generator.py \
  users/justin_harmon/hcss/knowledge/meetings \
  11/10/25 \
  HCSS TGIF
```

**Export to CSV:**
```bash
python3 timesheet_generator.py \
  users/justin_harmon/hcss/knowledge/meetings \
  11/10/25 \
  HCSS TGIF RAL

# Creates: timesheet_11_10_25.csv
```

---

## 📁 OUTPUT FORMATS

### **1. Console Output (Tab-Delimited)**
Ready to copy/paste directly into spreadsheet

### **2. CSV File**
- Filename: `timesheet_MM_DD_YY.csv`
- Can import into Excel/Google Sheets
- Preserves all formatting

---

## 🔧 HOW IT WORKS

### **Data Source**
Reads from: `users/justin_harmon/hcss/knowledge/meetings/json/`

Each meeting JSON contains:
```json
{
  "title": "TGIF Weekly Sync",
  "date": "2025-11-04",
  "metadata": {
    "duration": "1 hour",
    "participants": ["Justin Harmon", "Team"]
  }
}
```

### **Client Detection**
Automatically detects client from meeting title:
- "TGIF" → TGIF
- "HCSS" → HCSS
- "RAL" → RAL
- "CBM" → CBM

### **Duration Parsing**
Handles multiple formats:
- "1 hour" → 1.00
- "45 min" → 0.75
- "1 hour 30 min" → 1.50
- "2 hours" → 2.00

### **Day Calculation**
- Input: Week ending (Sunday)
- Calculates: Monday-Sunday dates
- Maps: Meetings to correct days

---

## 🎯 INTEGRATION WITH MEETING AUTOMATION

### **Automatic Flow**
```
Otter.ai Meeting
       ↓
Dual-Source Manager
       ↓
Meeting Processor
  (saves with duration)
       ↓
Knowledge Base
  (json files)
       ↓
Timesheet Generator
  (weekly summary)
       ↓
Your Spreadsheet
```

### **Manual Trigger**
Run timesheet generator whenever you need:
- End of week
- Before submitting timesheet
- Ad-hoc time tracking

---

## 📊 SAMPLE DATA

### **Week 1 Breakdown**
| Client | Mon | Tue | Wed | Thu | Fri | Total |
|--------|-----|-----|-----|-----|-----|-------|
| TGIF   | 1.00| 0.00| 1.50| 0.00| 1.25| 3.75  |
| HCSS   | 0.00| 0.75| 0.00| 0.00| 0.00| 0.75  |
| RAL    | 0.00| 0.00| 0.00| 2.00| 0.00| 2.00  |
| **Total** | **1.00** | **0.75** | **1.50** | **2.00** | **1.25** | **6.50** |

### **Week 2 Breakdown**
| Client | Mon | Tue | Wed | Thu | Fri | Total |
|--------|-----|-----|-----|-----|-----|-------|
| TGIF   | 1.00| 0.00| 1.50| 0.00| 2.00| 4.50  |
| HCSS   | 0.00| 2.00| 0.00| 0.75| 0.00| 2.75  |
| RAL    | 0.00| 0.00| 1.00| 0.00| 1.50| 2.50  |
| **Total** | **1.00** | **2.00** | **2.50** | **0.75** | **3.50** | **9.75** |

---

## 🚀 FUTURE ENHANCEMENTS

### **Goose Integration**
```
> Generate timesheet for this week
> Show me HCSS hours for last week
> Export timesheet for 11/10/25
```

### **Automatic Weekly Email**
- Runs every Friday at 4pm
- Generates current week timesheet
- Emails to you
- Includes CSV attachment

### **Multi-Week Reports**
```bash
# Last 4 weeks
python3 timesheet_generator.py \
  users/justin_harmon/hcss/knowledge/meetings \
  --weeks 4 \
  --ending 11/10/25
```

---

## 📝 NOTES

### **Meeting Classification**
- "TGIF meetings" row = meetings about TGIF (not project work)
- "TGIF" row = project assistance/work
- Automatically categorized based on title

### **Rounding**
- Durations rounded to 2 decimal places
- Matches your spreadsheet format

### **Comments**
- "meeting" for meeting-related entries
- "project assistance" for project work

---

## ✅ READY TO USE

**Status:** Production ready  
**Requirements:** Meeting automation running  
**Output:** Your exact timesheet format  
**Effort:** 10 seconds to generate

---

**Next:** Setup meeting automation credentials, then timesheet generation is fully automatic!
