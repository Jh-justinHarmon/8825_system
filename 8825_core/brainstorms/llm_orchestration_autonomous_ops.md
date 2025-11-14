# LLM Orchestration for Autonomous Operations
**Created:** 2025-11-12  
**Purpose:** Define how to control LLM selection for background tasks without keyboard intervention

---

## The Core Question

**"How do I ensure the right LLM is used for the right task when I'm not at the keyboard?"**

This is about **autonomous intelligence orchestration** - the system making smart decisions about which model to use, when, and why.

---

## Current State: Dual-Layer Intelligence

From `dual_layer_intelligence.md`:

### **Three-Tier Decision Model:**

**Tier 0: Pattern Matching (FREE)**
- Regex/keyword detection
- Rule-based routing
- No LLM needed
- Cost: $0

**Tier 1: Intelligence Layer (CHEAP)**
- Model: `gpt-4o-mini` ($0.15/1M tokens)
- Purpose: Triage and route
- Handles: Simple tasks, complexity analysis
- Cost: ~$0.003 per 100 files

**Tier 2: User Layer (EXPENSIVE)**
- Model: `gpt-4o` ($2.50/1M tokens) or Claude Sonnet 4.5
- Purpose: Complex analysis
- Handles: Deep content, nuanced decisions
- Cost: ~$0.125 per 100 files

**Result: 95% cost reduction while maintaining quality**

---

## The Problem for Customer Platform

### **Autonomous Operations Needed:**

**1. Email Processing (Background)**
```
Customer emails data → System processes → Responds
No human intervention
Which LLM? When? Why?
```

**2. Weekly Analysis (Scheduled)**
```
Sunday 10pm → Brain analyzes week's data → Emails summary
No human intervention
Which LLM? When? Why?
```

**3. Context Updates (Real-time)**
```
New data arrives → Extract/categorize → Update database
No human intervention
Which LLM? When? Why?
```

**4. Pattern Learning (Continuous)**
```
Brain observes patterns → Updates memory → Improves future decisions
No human intervention
Which LLM? When? Why?
```

---

## Solution: Task-Based LLM Router

### **Architecture:**

```
Task arrives
    ↓
Task Classifier (pattern matching - FREE)
    ↓
Complexity Analyzer (gpt-4o-mini - CHEAP)
    ↓
LLM Router (selects appropriate model)
    ↓
Execute with selected model
    ↓
Log decision + cost
```

---

## Task Classification System

### **Task Types & LLM Assignment:**

**Type 1: Simple Extraction**
- **Example:** Extract date from email subject
- **Pattern Match:** Can regex handle it?
- **If yes:** FREE (no LLM)
- **If no:** gpt-4o-mini
- **Never:** gpt-4o (overkill)

**Type 2: Simple Categorization**
- **Example:** Is this a lab result or prescription?
- **Pattern Match:** Check for keywords
- **If confident:** FREE
- **If uncertain:** gpt-4o-mini
- **Never:** gpt-4o (overkill)

**Type 3: Content Analysis**
- **Example:** Extract structured data from medical document
- **Pattern Match:** Can't handle
- **Complexity Check:** gpt-4o-mini analyzes document
- **If simple:** gpt-4o-mini extracts
- **If complex:** gpt-4o extracts

**Type 4: Trend Analysis**
- **Example:** Weekly health summary with insights
- **Pattern Match:** Can't handle
- **Complexity Check:** Always complex
- **Always:** gpt-4o (quality matters)

**Type 5: Conversational Response**
- **Example:** Answer customer's health question
- **Pattern Match:** Can't handle
- **Complexity Check:** gpt-4o-mini analyzes question
- **If simple:** gpt-4o-mini answers
- **If complex:** gpt-4o answers

---

## Implementation: LLM Router

### **Core Router Logic:**

```javascript
// lib/llm_router.js

class LLMRouter {
  constructor() {
    this.costs = {
      'pattern': 0,
      'gpt-4o-mini': 0.15 / 1_000_000,  // per token
      'gpt-4o': 2.50 / 1_000_000,        // per token
      'claude-sonnet-4.5': 3.00 / 1_000_000
    };
    
    this.usage = {
      pattern: 0,
      'gpt-4o-mini': 0,
      'gpt-4o': 0,
      'claude-sonnet-4.5': 0
    };
  }
  
  async route(task) {
    // Step 1: Try pattern matching (FREE)
    const patternResult = this.tryPatternMatch(task);
    if (patternResult.success) {
      this.logUsage('pattern', task);
      return { model: 'pattern', result: patternResult.data, cost: 0 };
    }
    
    // Step 2: Analyze complexity (CHEAP)
    const complexity = await this.analyzeComplexity(task);
    
    // Step 3: Route based on complexity
    const model = this.selectModel(task.type, complexity);
    
    // Step 4: Execute with selected model
    const result = await this.execute(model, task);
    
    // Step 5: Log usage and cost
    this.logUsage(model, task, result.tokens);
    
    return { model, result: result.data, cost: result.cost };
  }
  
  tryPatternMatch(task) {
    // Pattern matching rules
    const patterns = {
      extract_date: /\d{4}-\d{2}-\d{2}/,
      detect_lab_result: /\b(cholesterol|blood pressure|glucose)\b/i,
      detect_prescription: /\b(prescription|medication|mg|daily)\b/i,
      extract_email: /[\w.-]+@[\w.-]+\.\w+/
    };
    
    // Try each pattern
    for (const [name, pattern] of Object.entries(patterns)) {
      if (task.type === name) {
        const match = task.content.match(pattern);
        if (match) {
          return { success: true, data: match, confidence: 1.0 };
        }
      }
    }
    
    return { success: false };
  }
  
  async analyzeComplexity(task) {
    // Use cheap model to analyze complexity
    const prompt = `
      Analyze this task's complexity:
      
      Task type: ${task.type}
      Content preview: ${task.content.substring(0, 500)}
      
      Respond with JSON:
      {
        "complexity": "simple" | "medium" | "complex",
        "reasoning": "brief explanation",
        "confidence": 0.0-1.0
      }
    `;
    
    const response = await this.callModel('gpt-4o-mini', prompt);
    return JSON.parse(response);
  }
  
  selectModel(taskType, complexity) {
    // Task-specific routing rules
    const rules = {
      // Always use expensive model for quality-critical tasks
      weekly_analysis: 'gpt-4o',
      customer_response: complexity.complexity === 'complex' ? 'gpt-4o' : 'gpt-4o-mini',
      
      // Use cheap model for routine tasks
      extract_data: complexity.complexity === 'complex' ? 'gpt-4o' : 'gpt-4o-mini',
      categorize: 'gpt-4o-mini',
      
      // Use expensive model for nuanced tasks
      pattern_learning: 'gpt-4o',
      merge_decision: 'gpt-4o'
    };
    
    return rules[taskType] || 'gpt-4o-mini'; // Default to cheap
  }
  
  async execute(model, task) {
    if (model === 'pattern') {
      throw new Error('Pattern matching should be handled before execute()');
    }
    
    const response = await this.callModel(model, task.prompt);
    
    return {
      data: response,
      tokens: this.estimateTokens(task.prompt + response),
      cost: this.calculateCost(model, task.prompt + response)
    };
  }
  
  async callModel(model, prompt) {
    switch (model) {
      case 'gpt-4o-mini':
        return await this.callOpenAI('gpt-4o-mini', prompt);
      case 'gpt-4o':
        return await this.callOpenAI('gpt-4o', prompt);
      case 'claude-sonnet-4.5':
        return await this.callClaude('claude-sonnet-4-20250514', prompt);
      default:
        throw new Error(`Unknown model: ${model}`);
    }
  }
  
  async callOpenAI(model, prompt) {
    const OpenAI = require('openai');
    const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    
    const response = await openai.chat.completions.create({
      model: model,
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.7
    });
    
    return response.choices[0].message.content;
  }
  
  async callClaude(model, prompt) {
    const Anthropic = require('@anthropic-ai/sdk');
    const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
    
    const response = await anthropic.messages.create({
      model: model,
      max_tokens: 4096,
      messages: [{ role: 'user', content: prompt }]
    });
    
    return response.content[0].text;
  }
  
  estimateTokens(text) {
    // Rough estimate: 1 token ≈ 4 characters
    return Math.ceil(text.length / 4);
  }
  
  calculateCost(model, text) {
    const tokens = this.estimateTokens(text);
    return tokens * this.costs[model];
  }
  
  logUsage(model, task, tokens = 0) {
    this.usage[model]++;
    
    const cost = tokens > 0 ? this.calculateCost(model, tokens) : 0;
    
    console.log(JSON.stringify({
      timestamp: new Date().toISOString(),
      model: model,
      task_type: task.type,
      tokens: tokens,
      cost: cost,
      total_usage: this.usage
    }));
  }
  
  getStats() {
    return {
      usage: this.usage,
      total_cost: this.calculateTotalCost()
    };
  }
  
  calculateTotalCost() {
    // This would need to track actual token usage
    // Simplified for example
    return Object.entries(this.usage).reduce((total, [model, count]) => {
      return total + (count * this.costs[model] * 1000); // Rough estimate
    }, 0);
  }
}

module.exports = LLMRouter;
```

---

## Usage in Customer Platform

### **Email Processing:**

```javascript
// email_gateway.js
const LLMRouter = require('./lib/llm_router');
const router = new LLMRouter();

async function handleEmail(email) {
  const customer_id = routeEmail(email.to);
  
  // Task 1: Extract data from attachment (if present)
  if (email.attachment) {
    const extractTask = {
      type: 'extract_data',
      content: email.attachment.text,
      prompt: `Extract structured health data from this document: ${email.attachment.text}`
    };
    
    const extraction = await router.route(extractTask);
    // extraction.model will be 'pattern', 'gpt-4o-mini', or 'gpt-4o'
    // extraction.cost will be tracked
    
    await ingest(customer_id, extraction.result);
  }
  
  // Task 2: Generate response
  if (email.body) {
    const responseTask = {
      type: 'customer_response',
      content: email.body,
      prompt: `Answer this health question: ${email.body}`
    };
    
    const response = await router.route(responseTask);
    await sendEmail(email.from, response.result);
  }
}
```

---

### **Weekly Analysis:**

```javascript
// scheduler.js
const LLMRouter = require('./lib/llm_router');
const router = new LLMRouter();

async function runWeeklyAnalysis(customer_id) {
  const brain = loadBrain(customer_id);
  const weekData = loadWeekData(customer_id);
  
  // Always use expensive model for weekly analysis (quality matters)
  const analysisTask = {
    type: 'weekly_analysis',
    content: JSON.stringify(weekData),
    prompt: `
      You are ${brain.customer_name}'s health analysis brain.
      
      Analyze this week's health data and generate a comprehensive summary:
      ${JSON.stringify(weekData, null, 2)}
      
      Include trends, insights, and recommendations.
    `
  };
  
  const analysis = await router.route(analysisTask);
  // Will use gpt-4o because task.type === 'weekly_analysis'
  
  await sendEmail(brain.email, analysis.result);
  
  // Log cost for monitoring
  console.log(`Weekly analysis cost: $${analysis.cost.toFixed(4)}`);
}
```

---

### **Pattern Learning:**

```javascript
// brain_daemon.js
const LLMRouter = require('./lib/llm_router');
const router = new LLMRouter();

async function learnPatterns(customer_id) {
  const brain = loadBrain(customer_id);
  const recentData = loadRecentData(customer_id, days = 30);
  
  // Use expensive model for pattern learning (quality matters)
  const learningTask = {
    type: 'pattern_learning',
    content: JSON.stringify(recentData),
    prompt: `
      Analyze this customer's data and identify patterns:
      
      Current patterns known:
      ${JSON.stringify(brain.memory.patterns, null, 2)}
      
      Recent data:
      ${JSON.stringify(recentData, null, 2)}
      
      Identify new patterns or updates to existing patterns.
    `
  };
  
  const patterns = await router.route(learningTask);
  
  // Update brain memory
  brain.memory.patterns = patterns.result;
  saveBrain(customer_id, brain);
}
```

---

## Configuration System

### **Task Routing Rules (Configurable):**

```json
{
  "routing_rules": {
    "extract_date": {
      "try_pattern": true,
      "fallback": "gpt-4o-mini",
      "never_use": ["gpt-4o", "claude-sonnet-4.5"]
    },
    "extract_data": {
      "try_pattern": false,
      "complexity_check": true,
      "simple": "gpt-4o-mini",
      "complex": "gpt-4o"
    },
    "customer_response": {
      "try_pattern": false,
      "complexity_check": true,
      "simple": "gpt-4o-mini",
      "complex": "gpt-4o",
      "quality_threshold": 0.8
    },
    "weekly_analysis": {
      "try_pattern": false,
      "complexity_check": false,
      "always_use": "gpt-4o",
      "reason": "quality_critical"
    },
    "pattern_learning": {
      "try_pattern": false,
      "complexity_check": false,
      "always_use": "gpt-4o",
      "reason": "accuracy_critical"
    },
    "categorize": {
      "try_pattern": true,
      "fallback": "gpt-4o-mini",
      "never_use": ["gpt-4o"]
    }
  },
  
  "cost_limits": {
    "per_customer_daily": 1.00,
    "per_customer_monthly": 20.00,
    "alert_threshold": 0.80
  },
  
  "quality_checks": {
    "enabled": true,
    "sample_rate": 0.1,
    "compare_models": true
  }
}
```

---

## Environment Configuration

### **.env File:**

```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic (optional)
ANTHROPIC_API_KEY=sk-ant-...

# LLM Router Config
DEFAULT_MODEL=gpt-4o-mini
EXPENSIVE_MODEL=gpt-4o
ENABLE_PATTERN_MATCHING=true
ENABLE_COMPLEXITY_ANALYSIS=true

# Cost Controls
MAX_DAILY_COST_PER_CUSTOMER=1.00
MAX_MONTHLY_COST_PER_CUSTOMER=20.00
ALERT_ON_HIGH_COST=true

# Logging
LOG_LLM_USAGE=true
LOG_COSTS=true
```

---

## Monitoring & Cost Control

### **Usage Dashboard:**

```javascript
// Get router stats
const stats = router.getStats();

console.log(`
LLM Usage Stats:
- Pattern matching: ${stats.usage.pattern} (FREE)
- gpt-4o-mini: ${stats.usage['gpt-4o-mini']} ($${(stats.usage['gpt-4o-mini'] * 0.0003).toFixed(4)})
- gpt-4o: ${stats.usage['gpt-4o']} ($${(stats.usage['gpt-4o'] * 0.025).toFixed(4)})

Total cost: $${stats.total_cost.toFixed(4)}
Cost savings vs all-gpt-4o: ${((1 - stats.total_cost / (stats.usage.total * 0.025)) * 100).toFixed(1)}%
`);
```

---

### **Cost Alerts:**

```javascript
// Monitor costs per customer
async function checkCostLimits(customer_id) {
  const dailyCost = await getDailyCost(customer_id);
  const monthlyCost = await getMonthlyCost(customer_id);
  
  const limits = {
    daily: parseFloat(process.env.MAX_DAILY_COST_PER_CUSTOMER),
    monthly: parseFloat(process.env.MAX_MONTHLY_COST_PER_CUSTOMER)
  };
  
  if (dailyCost > limits.daily * 0.8) {
    console.warn(`Customer ${customer_id} approaching daily cost limit: $${dailyCost.toFixed(2)}`);
  }
  
  if (monthlyCost > limits.monthly * 0.8) {
    console.warn(`Customer ${customer_id} approaching monthly cost limit: $${monthlyCost.toFixed(2)}`);
  }
  
  // Optionally: switch to cheaper models if over limit
  if (dailyCost > limits.daily) {
    console.error(`Customer ${customer_id} exceeded daily cost limit. Switching to gpt-4o-mini only.`);
    return 'gpt-4o-mini-only';
  }
  
  return 'normal';
}
```

---

## Quality Assurance

### **Model Comparison (Sampling):**

```javascript
// Randomly compare cheap vs expensive model
async function qualityCheck(task) {
  if (Math.random() > 0.1) return; // 10% sample rate
  
  // Run task with both models
  const cheapResult = await router.callModel('gpt-4o-mini', task.prompt);
  const expensiveResult = await router.callModel('gpt-4o', task.prompt);
  
  // Compare results
  const comparison = {
    task_type: task.type,
    cheap_model: 'gpt-4o-mini',
    expensive_model: 'gpt-4o',
    cheap_result: cheapResult,
    expensive_result: expensiveResult,
    results_match: cheapResult === expensiveResult,
    timestamp: new Date().toISOString()
  };
  
  // Log for analysis
  await logComparison(comparison);
  
  // If results don't match, flag for review
  if (!comparison.results_match) {
    console.warn(`Quality check: Models disagree on ${task.type}`);
  }
}
```

---

## Decision Framework for LLM Selection

### **When to Use Each Model:**

**Pattern Matching (FREE):**
- ✅ Regex can handle it
- ✅ Keyword matching sufficient
- ✅ Rule-based logic works
- ✅ High confidence (0.9+)

**gpt-4o-mini (CHEAP):**
- ✅ Simple extraction
- ✅ Basic categorization
- ✅ Routine responses
- ✅ Complexity analysis
- ✅ Cost-sensitive tasks

**gpt-4o (EXPENSIVE):**
- ✅ Complex analysis
- ✅ Quality-critical tasks (weekly summaries)
- ✅ Nuanced decisions
- ✅ Pattern learning
- ✅ Customer-facing responses (when complex)

**Claude Sonnet 4.5 (EXPENSIVE):**
- ✅ When OpenAI is down (fallback)
- ✅ Specific tasks where Claude excels
- ✅ Customer preference

---

## Bottom Line: Autonomous LLM Orchestration

### **The System Decides:**

**Not you at keyboard:**
```
Task arrives → Router analyzes → Selects model → Executes → Logs
```

**You configure:**
```
Routing rules → Cost limits → Quality thresholds → Monitoring
```

**You monitor:**
```
Usage stats → Cost trends → Quality metrics → Adjust rules
```

---

### **Key Principles:**

1. **Cheapest First:** Pattern → gpt-4o-mini → gpt-4o
2. **Quality Matters:** Use expensive models for critical tasks
3. **Monitor Everything:** Track usage, costs, quality
4. **Adjust Dynamically:** Change rules based on real data
5. **Cost Controls:** Set limits, alert on overages

---

### **Implementation:**

**Week 1:**
- Build LLM Router class
- Define task types
- Set routing rules
- Add cost tracking

**Week 2:**
- Integrate with email gateway
- Integrate with scheduler
- Test with sample data
- Monitor costs

**Week 3:**
- Add quality checks
- Tune routing rules
- Optimize for cost
- Document learnings

---

**The system runs autonomously. You configure and monitor. LLMs are selected intelligently based on task complexity and cost constraints.**

Ready to build the router?
