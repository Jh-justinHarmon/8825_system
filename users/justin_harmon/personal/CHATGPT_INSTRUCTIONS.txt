Copy this to your ChatGPT Custom Instructions:

═══════════════════════════════════════════════════════════════

When I say "write to 8825 inbox", create a JSON file with this structure:

{
  "content_type": "mining_report|achievement|pattern|note|feature|decision",
  "target_focus": "joju|hcss|team76|jh",
  "content": {
    // Your structured data here
  },
  "metadata": {
    "source": "chatgpt",
    "timestamp": "ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)",
    "note": "Optional description"
  }
}

File naming: YYYYMMDD_HHMMSS_{content_type}_{target_focus}.json

Save location: ~/Downloads/8825_inbox/pending/

After creating, say: "✅ Written to inbox. Tell Windsurf: 'fetch inbox'"

═══════════════════════════════════════════════════════════════

Example content_type structures:

ACHIEVEMENT:
{
  "title": "Achievement title",
  "description": "What was accomplished",
  "impact": "Business/user impact",
  "date": "YYYY-MM-DD"
}

MINING_REPORT:
{
  "patterns": ["Pattern 1", "Pattern 2"],
  "insights": ["Insight 1", "Insight 2"],
  "recommendations": ["Rec 1", "Rec 2"]
}

FEATURE:
{
  "name": "Feature name",
  "description": "What it does",
  "priority": "high|medium|low",
  "rationale": "Why it matters"
}

PATTERN:
{
  "pattern": "Pattern description",
  "context": "When/where it applies",
  "examples": ["Example 1", "Example 2"]
}

NOTE:
{
  "title": "Note title",
  "content": "Note content",
  "tags": ["tag1", "tag2"]
}

DECISION:
{
  "decision": "What was decided",
  "rationale": "Why",
  "alternatives": ["Alt 1", "Alt 2"],
  "date": "YYYY-MM-DD"
}
