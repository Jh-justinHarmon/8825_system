/**
 * LLOM Router Test Suite
 * 
 * Basic tests to verify router functionality
 */

const LLOMRouter = require('./llom_router');

async function runTests() {
  console.log('🧪 LLOM Router Test Suite\n');
  
  const router = new LLOMRouter();
  let passed = 0;
  let failed = 0;
  
  // Test 1: Pattern Matching (Date Extraction)
  console.log('Test 1: Pattern Matching (Date Extraction)');
  try {
    const result = await router.route({
      system: 'test',
      task: 'extract_date',
      content: 'Meeting scheduled for 2025-11-12 at 2pm'
    });
    
    if (result.model === 'pattern' && result.cost === 0) {
      console.log('✅ PASS - Pattern match successful, cost = $0');
      console.log(`   Result: ${result.result}`);
      passed++;
    } else {
      console.log(`❌ FAIL - Expected pattern match, got ${result.model}`);
      failed++;
    }
  } catch (error) {
    console.log(`❌ FAIL - Error: ${error.message}`);
    failed++;
  }
  console.log('');
  
  // Test 2: Pattern Matching (Email Extraction)
  console.log('Test 2: Pattern Matching (Email Extraction)');
  try {
    const result = await router.route({
      system: 'test',
      task: 'extract_email',
      content: 'Contact me at justin@example.com for more info'
    });
    
    if (result.model === 'pattern' && result.cost === 0) {
      console.log('✅ PASS - Pattern match successful, cost = $0');
      console.log(`   Result: ${result.result}`);
      passed++;
    } else {
      console.log(`❌ FAIL - Expected pattern match, got ${result.model}`);
      failed++;
    }
  } catch (error) {
    console.log(`❌ FAIL - Error: ${error.message}`);
    failed++;
  }
  console.log('');
  
  // Test 3: Configuration Loading
  console.log('Test 3: Configuration Loading');
  try {
    const config = router.config;
    if (config.models && config.routing_rules && config.cost_limits) {
      console.log('✅ PASS - Configuration loaded successfully');
      console.log(`   Models: ${Object.keys(config.models).join(', ')}`);
      console.log(`   Systems: ${Object.keys(config.routing_rules).join(', ')}`);
      passed++;
    } else {
      console.log('❌ FAIL - Configuration incomplete');
      failed++;
    }
  } catch (error) {
    console.log(`❌ FAIL - Error: ${error.message}`);
    failed++;
  }
  console.log('');
  
  // Test 4: Routing Rule Lookup
  console.log('Test 4: Routing Rule Lookup');
  try {
    const rule = router.getRoutingRule({
      system: 'ingestion',
      task: 'file_naming'
    });
    
    if (rule && rule.complexity_check !== undefined) {
      console.log('✅ PASS - Routing rule found');
      console.log(`   Rule: ${JSON.stringify(rule, null, 2)}`);
      passed++;
    } else {
      console.log('❌ FAIL - Routing rule not found or invalid');
      failed++;
    }
  } catch (error) {
    console.log(`❌ FAIL - Error: ${error.message}`);
    failed++;
  }
  console.log('');
  
  // Test 5: Cost Calculation
  console.log('Test 5: Cost Calculation');
  try {
    const tokens = 1000;
    const cost = router.calculateCost('gpt-4o-mini', tokens);
    const expectedCost = (tokens / 1_000_000) * 0.15;
    
    if (Math.abs(cost - expectedCost) < 0.000001) {
      console.log('✅ PASS - Cost calculation correct');
      console.log(`   1000 tokens with gpt-4o-mini = $${cost.toFixed(6)}`);
      passed++;
    } else {
      console.log(`❌ FAIL - Cost calculation incorrect: ${cost} vs ${expectedCost}`);
      failed++;
    }
  } catch (error) {
    console.log(`❌ FAIL - Error: ${error.message}`);
    failed++;
  }
  console.log('');
  
  // Test 6: Statistics Tracking
  console.log('Test 6: Statistics Tracking');
  try {
    const stats = router.getStats();
    
    if (stats.usage && stats.total_tasks >= 0 && stats.total_cost >= 0) {
      console.log('✅ PASS - Statistics tracking working');
      console.log(`   Total tasks: ${stats.total_tasks}`);
      console.log(`   Total cost: $${stats.total_cost.toFixed(6)}`);
      console.log(`   Pattern usage: ${stats.pattern_usage_percent.toFixed(1)}%`);
      passed++;
    } else {
      console.log('❌ FAIL - Statistics incomplete');
      failed++;
    }
  } catch (error) {
    console.log(`❌ FAIL - Error: ${error.message}`);
    failed++;
  }
  console.log('');
  
  // Test 7: Model Selection Logic
  console.log('Test 7: Model Selection Logic');
  try {
    const task = { system: 'analysis', task: 'weekly_summary' };
    const rule = router.getRoutingRule(task);
    const model = router.selectModel(task, rule, null);
    
    if (model === 'gpt-4o') {
      console.log('✅ PASS - Model selection correct (quality-critical → expensive)');
      console.log(`   Selected: ${model}`);
      passed++;
    } else {
      console.log(`❌ FAIL - Expected gpt-4o, got ${model}`);
      failed++;
    }
  } catch (error) {
    console.log(`❌ FAIL - Error: ${error.message}`);
    failed++;
  }
  console.log('');
  
  // Summary
  console.log('═'.repeat(60));
  console.log(`Test Results: ${passed} passed, ${failed} failed`);
  console.log('═'.repeat(60));
  
  if (failed === 0) {
    console.log('\n✅ All tests passed! LLOM Router is working correctly.\n');
    
    // Show final stats
    const finalStats = router.getStats();
    console.log('Final Statistics:');
    console.log(`- Pattern matches: ${finalStats.usage.pattern}`);
    console.log(`- Total cost: $${finalStats.total_cost.toFixed(6)}`);
    console.log(`- Pattern usage: ${finalStats.pattern_usage_percent.toFixed(1)}%`);
    
    return 0;
  } else {
    console.log(`\n❌ ${failed} test(s) failed. Please review errors above.\n`);
    return 1;
  }
}

// Run tests
if (require.main === module) {
  runTests()
    .then(exitCode => process.exit(exitCode))
    .catch(error => {
      console.error('Test suite error:', error);
      process.exit(1);
    });
}

module.exports = { runTests };
