/**
 * LLOM Router - LLM Orchestration Module
 * 
 * Three-tier intelligent routing for LLM operations:
 * - Tier 0: Pattern Matching (FREE)
 * - Tier 1: Intelligence Layer (gpt-4o-mini - CHEAP)
 * - Tier 2: User Layer (gpt-4o/Claude - EXPENSIVE)
 * 
 * Origin: Project 8825 1.0 (project8825-production.js)
 * Proven: 95% cost reduction in Content Index System (2025-11-11)
 * 
 * @version 1.0.0
 * @date 2025-11-12
 */

const fs = require('fs');
const path = require('path');

class LLOMRouter {
  constructor(configPath = null) {
    // Load configuration
    this.config = this.loadConfig(configPath);
    
    // Cost tracking (per million tokens)
    this.costs = {
      'pattern': 0,
      'gpt-4o-mini': 0.15,
      'gpt-4o': 2.50,
      'claude-sonnet-4.5': 3.00
    };
    
    // Usage tracking
    this.usage = {
      pattern: 0,
      'gpt-4o-mini': 0,
      'gpt-4o': 0,
      'claude-sonnet-4.5': 0
    };
    
    // Decision log for learning
    this.decisions = [];
    
    // Initialize API clients lazily
    this.openaiClient = null;
    this.anthropicClient = null;
  }
  
  /**
   * Load configuration from file or use defaults
   */
  loadConfig(configPath) {
    if (!configPath) {
      configPath = path.join(__dirname, 'llom_config.json');
    }
    
    if (fs.existsSync(configPath)) {
      return JSON.parse(fs.readFileSync(configPath, 'utf8'));
    }
    
    // Default configuration
    return {
      models: {
        cheap: { provider: 'openai', model: 'gpt-4o-mini' },
        expensive: { provider: 'openai', model: 'gpt-4o' },
        fallback: { provider: 'anthropic', model: 'claude-sonnet-4-20250514' }
      },
      routing_rules: {},
      cost_limits: {
        per_task_max: 0.10,
        per_hour_max: 1.00,
        per_day_max: 10.00,
        alert_threshold: 0.80
      },
      quality_checks: {
        enabled: true,
        sample_rate: 0.10
      },
      optimization: {
        enable_caching: true,
        cache_ttl_seconds: 3600,
        enable_learning: true
      }
    };
  }
  
  /**
   * Main routing method - determines which model to use and executes
   * 
   * @param {Object} task - Task object with system, task, content, context
   * @returns {Object} - { model, result, cost, confidence }
   */
  async route(task) {
    const startTime = Date.now();
    
    try {
      // Step 1: Try pattern matching (FREE)
      const patternResult = this.tryPatternMatch(task);
      if (patternResult.success) {
        this.logDecision(task, 'pattern', patternResult, Date.now() - startTime);
        return {
          model: 'pattern',
          result: patternResult.data,
          cost: 0,
          confidence: patternResult.confidence,
          latency_ms: Date.now() - startTime
        };
      }
      
      // Step 2: Check routing rules
      const routingRule = this.getRoutingRule(task);
      
      if (routingRule.never_use_llm) {
        throw new Error(`No pattern match found and LLM disabled for ${task.system}.${task.task}`);
      }
      
      // Step 3: Analyze complexity (if needed)
      let complexity = null;
      if (routingRule.complexity_check) {
        complexity = await this.analyzeComplexity(task);
      }
      
      // Step 4: Select model based on rules and complexity
      const model = this.selectModel(task, routingRule, complexity);
      
      // Step 5: Execute with selected model
      const result = await this.execute(model, task);
      
      // Step 6: Log decision
      this.logDecision(task, model, result, Date.now() - startTime, complexity);
      
      return {
        model: model,
        result: result.data,
        cost: result.cost,
        confidence: result.confidence || (complexity ? complexity.confidence : 0.8),
        latency_ms: Date.now() - startTime
      };
      
    } catch (error) {
      console.error(`LLOM Router error:`, error);
      throw error;
    }
  }
  
  /**
   * Try to match task using pattern matching (FREE tier)
   */
  tryPatternMatch(task) {
    // Pattern matching rules
    const patterns = {
      extract_date: /\d{4}-\d{2}-\d{2}/,
      extract_email: /[\w.-]+@[\w.-]+\.\w+/,
      detect_lab_result: /\b(cholesterol|blood pressure|glucose|hemoglobin)\b/i,
      detect_prescription: /\b(prescription|medication|mg|daily|dosage)\b/i,
      detect_meeting: /\b(meeting|sync|standup|1:1|one-on-one)\b/i,
      detect_action_item: /\b(TODO|ACTION|TASK|FOLLOW.?UP)\b/i
    };
    
    // Check if task type has a pattern
    const taskKey = `${task.system}_${task.task}`.replace(/[^a-z0-9_]/gi, '_');
    
    for (const [name, pattern] of Object.entries(patterns)) {
      if (taskKey.includes(name.replace('detect_', '').replace('extract_', ''))) {
        const match = task.content.match(pattern);
        if (match) {
          this.usage.pattern++;
          return {
            success: true,
            data: match[0] || match,
            confidence: 1.0,
            pattern: name
          };
        }
      }
    }
    
    return { success: false };
  }
  
  /**
   * Get routing rule for task
   */
  getRoutingRule(task) {
    const rules = this.config.routing_rules;
    
    // Check for system.task specific rule
    if (rules[task.system] && rules[task.system][task.task]) {
      return rules[task.system][task.task];
    }
    
    // Check for system-level default
    if (rules[task.system] && rules[task.system].default) {
      return rules[task.system].default;
    }
    
    // Global default
    return {
      try_pattern: true,
      complexity_check: true,
      simple: 'cheap',
      complex: 'expensive',
      never_use_llm: false
    };
  }
  
  /**
   * Analyze task complexity using cheap model
   */
  async analyzeComplexity(task) {
    const prompt = `Analyze this task's complexity:

Task type: ${task.system}.${task.task}
Content preview: ${task.content.substring(0, 500)}

Respond with JSON only:
{
  "complexity": "simple" | "medium" | "complex",
  "reasoning": "brief explanation",
  "confidence": 0.0-1.0
}`;
    
    try {
      const response = await this.callModel('gpt-4o-mini', prompt, { temperature: 0.3 });
      const analysis = JSON.parse(response);
      return analysis;
    } catch (error) {
      console.error('Complexity analysis failed:', error);
      // Default to medium complexity if analysis fails
      return {
        complexity: 'medium',
        reasoning: 'Analysis failed, defaulting to medium',
        confidence: 0.5
      };
    }
  }
  
  /**
   * Select model based on routing rules and complexity
   */
  selectModel(task, routingRule, complexity) {
    // Check for always_use rule
    if (routingRule.always_use) {
      return routingRule.always_use === 'cheap' ? 'gpt-4o-mini' : 'gpt-4o';
    }
    
    // Check for never_use rule
    if (routingRule.never_use && routingRule.never_use.includes('expensive')) {
      return 'gpt-4o-mini';
    }
    
    // Complexity-based routing
    if (complexity) {
      if (complexity.complexity === 'simple') {
        return routingRule.simple === 'cheap' ? 'gpt-4o-mini' : 'gpt-4o';
      } else if (complexity.complexity === 'complex') {
        return routingRule.complex === 'expensive' ? 'gpt-4o' : 'gpt-4o-mini';
      }
    }
    
    // Default to cheap model
    return 'gpt-4o-mini';
  }
  
  /**
   * Execute task with selected model
   */
  async execute(model, task) {
    if (model === 'pattern') {
      throw new Error('Pattern matching should be handled before execute()');
    }
    
    const prompt = task.prompt || this.buildPrompt(task);
    const response = await this.callModel(model, prompt, task.options || {});
    
    const tokens = this.estimateTokens(prompt + response);
    const cost = this.calculateCost(model, tokens);
    
    this.usage[model]++;
    
    return {
      data: response,
      tokens: tokens,
      cost: cost
    };
  }
  
  /**
   * Build prompt from task
   */
  buildPrompt(task) {
    let prompt = '';
    
    // Add context if provided
    if (task.context) {
      prompt += `CONTEXT:\n${JSON.stringify(task.context, null, 2)}\n\n`;
    }
    
    // Add task description
    prompt += `TASK: ${task.system}.${task.task}\n\n`;
    
    // Add content
    prompt += `CONTENT:\n${task.content}\n\n`;
    
    // Add instructions if provided
    if (task.instructions) {
      prompt += `INSTRUCTIONS:\n${task.instructions}\n`;
    }
    
    return prompt;
  }
  
  /**
   * Call LLM model
   */
  async callModel(model, prompt, options = {}) {
    switch (model) {
      case 'gpt-4o-mini':
      case 'gpt-4o':
        return await this.callOpenAI(model, prompt, options);
      case 'claude-sonnet-4.5':
        return await this.callClaude('claude-sonnet-4-20250514', prompt, options);
      default:
        throw new Error(`Unknown model: ${model}`);
    }
  }
  
  /**
   * Call OpenAI API
   */
  async callOpenAI(model, prompt, options = {}) {
    if (!this.openaiClient) {
      const OpenAI = require('openai');
      this.openaiClient = new OpenAI({
        apiKey: process.env.OPENAI_API_KEY
      });
    }
    
    const response = await this.openaiClient.chat.completions.create({
      model: model,
      messages: [{ role: 'user', content: prompt }],
      temperature: options.temperature || 0.7,
      max_tokens: options.max_tokens || 4096
    });
    
    return response.choices[0].message.content;
  }
  
  /**
   * Call Anthropic API
   */
  async callClaude(model, prompt, options = {}) {
    if (!this.anthropicClient) {
      const Anthropic = require('@anthropic-ai/sdk');
      this.anthropicClient = new Anthropic({
        apiKey: process.env.ANTHROPIC_API_KEY
      });
    }
    
    const response = await this.anthropicClient.messages.create({
      model: model,
      max_tokens: options.max_tokens || 4096,
      messages: [{ role: 'user', content: prompt }]
    });
    
    return response.content[0].text;
  }
  
  /**
   * Estimate token count (rough approximation)
   */
  estimateTokens(text) {
    // Rough estimate: 1 token ≈ 4 characters
    return Math.ceil(text.length / 4);
  }
  
  /**
   * Calculate cost for tokens
   */
  calculateCost(model, tokens) {
    const costPerMillion = this.costs[model] || 0;
    return (tokens / 1_000_000) * costPerMillion;
  }
  
  /**
   * Log routing decision for analysis
   */
  logDecision(task, model, result, latency_ms, complexity = null) {
    const decision = {
      timestamp: new Date().toISOString(),
      system: task.system,
      task: task.task,
      model: model,
      cost: result.cost || 0,
      latency_ms: latency_ms,
      complexity: complexity,
      confidence: result.confidence || (complexity ? complexity.confidence : null)
    };
    
    this.decisions.push(decision);
    
    // Keep only last 1000 decisions in memory
    if (this.decisions.length > 1000) {
      this.decisions = this.decisions.slice(-1000);
    }
    
    // Log to console
    if (process.env.LOG_LLOM_DECISIONS === 'true') {
      console.log(JSON.stringify(decision));
    }
  }
  
  /**
   * Get usage statistics
   */
  getStats() {
    const totalTasks = Object.values(this.usage).reduce((a, b) => a + b, 0);
    const totalCost = this.decisions.reduce((sum, d) => sum + d.cost, 0);
    
    // Calculate by system
    const bySystem = {};
    for (const decision of this.decisions) {
      if (!bySystem[decision.system]) {
        bySystem[decision.system] = { count: 0, cost: 0 };
      }
      bySystem[decision.system].count++;
      bySystem[decision.system].cost += decision.cost;
    }
    
    // Top cost drivers
    const topCosts = this.decisions
      .sort((a, b) => b.cost - a.cost)
      .slice(0, 10)
      .map(d => ({
        system: d.system,
        task: d.task,
        model: d.model,
        cost: d.cost
      }));
    
    return {
      usage: this.usage,
      total_tasks: totalTasks,
      total_cost: totalCost,
      avg_cost_per_task: totalTasks > 0 ? totalCost / totalTasks : 0,
      by_system: bySystem,
      top_costs: topCosts,
      pattern_usage_percent: totalTasks > 0 ? (this.usage.pattern / totalTasks) * 100 : 0
    };
  }
  
  /**
   * Get recent decisions for analysis
   */
  getRecentDecisions(limit = 100) {
    return this.decisions.slice(-limit);
  }
  
  /**
   * Reset statistics
   */
  resetStats() {
    this.usage = {
      pattern: 0,
      'gpt-4o-mini': 0,
      'gpt-4o': 0,
      'claude-sonnet-4.5': 0
    };
    this.decisions = [];
  }
}

module.exports = LLOMRouter;
