# Goose MCP Bridge - User Guide

**For:** All Team Members  
**Version:** 2.0.0  
**Last Updated:** November 10, 2025

---

## 👋 Welcome!

This guide will help you use Goose to manage Joju tasks, query user feedback, and interact with the 8825 system using natural language.

**No technical knowledge required!** Just talk to Goose naturally.

---

## 🚀 Getting Started

### First Time Setup (5 minutes)

**Step 1: Install Goose**
```bash
pip install goose-ai
```

**Step 2: Configure for 8825**
Ask your admin to run:
```bash
cd 8825_core/integrations/goose
./SETUP_GOOSE.sh
```

**Step 3: Start Goose**
```bash
cd "/path/to/8825/workspace"
goose session start
```

That's it! You're ready to use Goose.

---

## 💬 How to Talk to Goose

### Natural Language - Just Ask!

You don't need to memorize commands. Just talk naturally:

**Good Examples:**
- "Show me all tasks that are in progress"
- "Create a high priority task for workflow automation"
- "What user feedback do we have about AI features?"
- "Mark task ABC123 as done"
- "Get me a summary of all user testing"

**Not Necessary:**
- ❌ "Use list_tasks with status=In Progress"
- ❌ "Call the create_task function"

Goose understands context and intent!

---

## 📋 Common Tasks

### Task Management

#### See All Your Tasks
```
"Show me all my tasks"
"What tasks am I working on?"
"List all tasks assigned to me"
```

#### See Team Tasks
```
"Show me all tasks in progress"
"What are the critical priority tasks?"
"List all bugs"
"Show me tasks for this sprint"
```

#### Create a New Task
```
"Create a high priority feature task for workflow automation"
"Add a bug report for the login issue, make it critical"
"Create a task: Implement context-aware AI based on user feedback"
```

#### Update Task Status
```
"Mark task ABC123 as done"
"Move task XYZ789 to in progress"
"Change the priority of task ABC to critical"
"Update task XYZ to in review"
```

#### Search Tasks
```
"Find all tasks about AI"
"Search for tasks related to workflow"
"Show me tasks mentioning customization"
```

#### Sync with Notion
```
"Sync tasks with Notion"
"Pull the latest tasks"
"Update task list from Notion"
```

---

### User Feedback

#### Get Summary
```
"Show me a summary of user feedback"
"What's the overall user testing data?"
"Give me user engagement stats"
```

#### Query Specific Feedback
```
"What did users say about workflow?"
"Show me feedback from Kayson"
"What feedback do we have about AI features?"
"Show me pain points users mentioned"
```

#### Create Tasks from Feedback
```
"Create a task from this feedback: Users want better customization"
"Turn this into a high priority task: Workflow automation needed"
```

---

### System Operations

#### Check Status
```
"What's the system status?"
"Check 8825 status"
"Show me inbox stats"
```

#### Process Inbox
```
"Process the inbox"
"Run the inbox pipeline"
"Check for new files and process them"
```

#### Review Tickets
```
"Show me teaching tickets"
"What tickets need review?"
"List pending tickets"
```

---

## 🎯 Workflows

### Morning Standup
```
1. "Show me all tasks in progress"
2. "What are today's critical tasks?"
3. "Get user feedback summary"
```

### Planning Session
```
1. "Show me all backlog items"
2. "List high priority features"
3. "What user feedback do we have about [feature]?"
4. "Create tasks for top 3 user requests"
```

### End of Day
```
1. "Mark task [ID] as done"
2. "Update task [ID] to in review"
3. "Sync tasks with Notion"
```

### User Research Review
```
1. "Get user feedback summary"
2. "What did users say about [theme]?"
3. "Create a task from this feedback: [quote]"
4. "Show me all tasks created from user feedback"
```

---

## 💡 Tips & Tricks

### Be Specific When Needed
```
✅ "Show me critical priority tasks"
✅ "Create a feature task with high priority"
✅ "Search for tasks about AI features"
```

### Use Context
```
✅ "Show me tasks" → "Now filter for high priority" → "Create a similar task"
```

### Ask for Help
```
"What tools are available?"
"How do I create a task?"
"Show me examples of task management"
```

### Combine Operations
```
"Check status and process inbox if there are new files"
"Show me user feedback about workflow and create a task for the top issue"
```

---

## 🆘 Troubleshooting

### "I don't see any tasks"
**Solution:**
```
"Sync tasks with Notion"
```
Wait a moment, then:
```
"Show me all tasks"
```

### "Task creation failed"
**Check:**
- Is Notion configured? (Ask admin)
- Did you include a title?
- Try: "Create a simple test task"

### "No user feedback found"
**Check:**
- Has user testing data been imported?
- Try: "Get user feedback summary" to see what's available

### "Goose doesn't respond"
**Try:**
1. Exit and restart: `Ctrl+C` then `goose session start`
2. Check connection: "List available tools"
3. Ask admin to check logs

---

## 📊 Understanding Results

### Task Lists
```
Status: In Progress (3)
────────────────────────────────────
🟠 Implement workflow automation
   Type: Feature | Priority: High
   Owner: Justin Harmon
   Due: 2025-12-15
```

### User Feedback
```
Total Sessions: 5
Total Quotes: 91
Filtered: 19 quotes about "workflow"

Top Themes:
- Workflow integration (19 mentions)
- Customization (6 mentions)
- AI features (3 mentions)
```

### System Status
```
8825 System Status:
- Pending files: 3
- Processed today: 12
- Errors: 0
```

---

## 🔐 Permissions

### What You Can Do
- ✅ View all tasks
- ✅ Create tasks
- ✅ Update tasks you own
- ✅ Query user feedback
- ✅ Check system status

### What Requires Admin
- ❌ Configure Notion
- ❌ Modify MCP bridge
- ❌ Change authentication
- ❌ Access logs directly

---

## 📚 Quick Reference

### Task Properties

**Types:**
- Feature
- Bug
- Enhancement
- Research
- Documentation

**Priorities:**
- Critical
- High
- Medium
- Low

**Statuses:**
- Backlog
- To Do
- In Progress
- In Review
- Done

**Sources:**
- User Feedback
- Team Idea
- Bug Report
- Survey
- Competitive Analysis

---

## 🎓 Learning Path

### Week 1: Basics
- Day 1: View tasks
- Day 2: Create simple tasks
- Day 3: Update task status
- Day 4: Search tasks
- Day 5: Query user feedback

### Week 2: Workflows
- Day 1: Morning standup routine
- Day 2: Planning session workflow
- Day 3: User research review
- Day 4: End of day updates
- Day 5: Weekly sync

### Week 3: Advanced
- Day 1: Create tasks from feedback
- Day 2: Complex searches
- Day 3: Multi-step workflows
- Day 4: Team collaboration
- Day 5: Optimization

---

## 💬 Example Conversations

### Example 1: Daily Standup
```
You: "Good morning! Show me my tasks"
Goose: [Lists your tasks]

You: "What's the status of the workflow automation task?"
Goose: [Shows task details]

You: "Move it to in progress"
Goose: ✅ Task updated

You: "What's critical today?"
Goose: [Lists critical tasks]
```

### Example 2: User Research
```
You: "Get user feedback summary"
Goose: [Shows 91 quotes, 5 sessions, 7 themes]

You: "What did users say about workflow?"
Goose: [Shows 19 workflow-related quotes]

You: "Create a high priority task for the top workflow issue"
Goose: ✅ Task created: "Improve workflow integration"

You: "Link it to the Kayson feedback"
Goose: ✅ Task linked to feedback
```

### Example 3: Sprint Planning
```
You: "Show me all backlog items"
Goose: [Lists backlog]

You: "Filter for high priority features"
Goose: [Filtered list]

You: "Move the top 3 to To Do"
Goose: ✅ Tasks updated

You: "Assign them to the team"
Goose: [Asks for assignments]
```

---

## 🎉 Best Practices

### Do:
- ✅ Sync tasks regularly
- ✅ Use descriptive task titles
- ✅ Link tasks to user feedback
- ✅ Update status as you work
- ✅ Search before creating duplicates

### Don't:
- ❌ Create vague tasks
- ❌ Forget to sync
- ❌ Leave tasks in "In Progress" forever
- ❌ Ignore user feedback data

---

## 📞 Getting Help

### In Goose
```
"What tools are available?"
"How do I [action]?"
"Show me examples"
```

### From Team
- Ask your admin for Notion access
- Check team Slack for tips
- Review this guide

### Documentation
- [PRODUCTION_READY.md](PRODUCTION_READY.md) - Technical details
- [INDEX.md](INDEX.md) - All documentation
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues

---

## 🚀 You're Ready!

Start with simple commands:
1. "Show me all tasks"
2. "Get user feedback summary"
3. "Check system status"

Then explore from there. Goose is smart - just ask naturally!

**Questions?** Ask in team Slack or check the docs.

---

**Version:** 2.0.0  
**Last Updated:** November 10, 2025  
**Happy Goose-ing!** 🦢
