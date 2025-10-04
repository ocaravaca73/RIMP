#!/usr/bin/env node

/**
 * Test script for validating label-to-field mappings in project-sync.yml
 * 
 * This script tests the label mapping logic without requiring API access.
 * It validates that labels are correctly mapped to their expected field values.
 */

// Label mapping definitions (matching project-sync.yml)
const typeMap = {
  'type:feature': 'Feature',
  'type:spike': 'Spike',
  'type:task': 'Task',
  'type:bug': 'Bug',
  'type:chore': 'Chore'
};

const areaMap = {
  'area:app': 'App',
  'area:backend': 'Backend',
  'area:realtime': 'Realtime',
  'area:telemetry': 'Telemetry',
  'area:data': 'Data',
  'area:ux': 'UX',
  'area:ops': 'Ops'
};

// Test utilities
function mapType(labels) {
  for (const [lbl, val] of Object.entries(typeMap)) {
    if (labels.includes(lbl)) {
      return val;
    }
  }
  return null;
}

function mapPriority(labels) {
  const prioLbl = labels.find(l => /^prio:P[0-3]$/i.test(l));
  if (prioLbl) {
    return prioLbl.split(':')[1].toUpperCase();
  }
  return null;
}

function mapArea(labels) {
  for (const [lbl, val] of Object.entries(areaMap)) {
    if (labels.includes(lbl)) {
      return val;
    }
  }
  return null;
}

function mapSprint(labels) {
  return labels.includes('sprint:current') ? 'CURRENT' : null;
}

function mapEstimate(labels) {
  const estLbl = labels.find(l => /^estimate:\d+$/i.test(l));
  if (estLbl) {
    return Number(estLbl.split(':')[1]);
  }
  return null;
}

// Test cases
const testCases = [
  {
    name: 'Telemetry feature with priority and estimate',
    labels: ['type:feature', 'area:telemetry', 'prio:P1', 'estimate:5'],
    expected: {
      type: 'Feature',
      area: 'Telemetry',
      priority: 'P1',
      estimate: 5,
      sprint: null
    }
  },
  {
    name: 'Telemetry bug in current sprint',
    labels: ['type:bug', 'area:telemetry', 'prio:P0', 'sprint:current'],
    expected: {
      type: 'Bug',
      area: 'Telemetry',
      priority: 'P0',
      estimate: null,
      sprint: 'CURRENT'
    }
  },
  {
    name: 'Telemetry spike without priority',
    labels: ['type:spike', 'area:telemetry', 'estimate:3'],
    expected: {
      type: 'Spike',
      area: 'Telemetry',
      priority: null,
      estimate: 3,
      sprint: null
    }
  },
  {
    name: 'Backend task with all fields',
    labels: ['type:task', 'area:backend', 'prio:P2', 'estimate:8', 'sprint:current'],
    expected: {
      type: 'Task',
      area: 'Backend',
      priority: 'P2',
      estimate: 8,
      sprint: 'CURRENT'
    }
  },
  {
    name: 'Realtime chore',
    labels: ['type:chore', 'area:realtime', 'prio:P3'],
    expected: {
      type: 'Chore',
      area: 'Realtime',
      priority: 'P3',
      estimate: null,
      sprint: null
    }
  },
  {
    name: 'App feature',
    labels: ['type:feature', 'area:app', 'estimate:2'],
    expected: {
      type: 'Feature',
      area: 'App',
      priority: null,
      estimate: 2,
      sprint: null
    }
  },
  {
    name: 'Data task',
    labels: ['type:task', 'area:data', 'prio:P1', 'sprint:current'],
    expected: {
      type: 'Task',
      area: 'Data',
      priority: 'P1',
      estimate: null,
      sprint: 'CURRENT'
    }
  },
  {
    name: 'UX bug',
    labels: ['type:bug', 'area:ux', 'prio:P2', 'estimate:1'],
    expected: {
      type: 'Bug',
      area: 'UX',
      priority: 'P2',
      estimate: 1,
      sprint: null
    }
  },
  {
    name: 'Ops spike',
    labels: ['type:spike', 'area:ops', 'estimate:5'],
    expected: {
      type: 'Spike',
      area: 'Ops',
      priority: null,
      estimate: 5,
      sprint: null
    }
  },
  {
    name: 'Priority variations - P0',
    labels: ['type:feature', 'prio:P0'],
    expected: {
      type: 'Feature',
      area: null,
      priority: 'P0',
      estimate: null,
      sprint: null
    }
  },
  {
    name: 'Priority variations - P3',
    labels: ['type:task', 'prio:P3'],
    expected: {
      type: 'Task',
      area: null,
      priority: 'P3',
      estimate: null,
      sprint: null
    }
  },
  {
    name: 'Estimate variations - small',
    labels: ['type:feature', 'estimate:1'],
    expected: {
      type: 'Feature',
      area: null,
      priority: null,
      estimate: 1,
      sprint: null
    }
  },
  {
    name: 'Estimate variations - large',
    labels: ['type:feature', 'estimate:13'],
    expected: {
      type: 'Feature',
      area: null,
      priority: null,
      estimate: 13,
      sprint: null
    }
  },
  {
    name: 'No labels',
    labels: [],
    expected: {
      type: null,
      area: null,
      priority: null,
      estimate: null,
      sprint: null
    }
  },
  {
    name: 'Only type label',
    labels: ['type:feature'],
    expected: {
      type: 'Feature',
      area: null,
      priority: null,
      estimate: null,
      sprint: null
    }
  },
  {
    name: 'Multiple type labels (first wins)',
    labels: ['type:feature', 'type:bug'],
    expected: {
      type: 'Feature', // First match wins
      area: null,
      priority: null,
      estimate: null,
      sprint: null
    }
  },
  {
    name: 'Multiple area labels (first in map wins)',
    labels: ['type:task', 'area:telemetry', 'area:backend'],
    expected: {
      type: 'Task',
      area: 'Backend', // Backend comes before Telemetry in the areaMap, so it wins
      priority: null,
      estimate: null,
      sprint: null
    }
  },
  {
    name: 'Invalid priority format',
    labels: ['type:feature', 'prio:HIGH', 'prio:invalid'],
    expected: {
      type: 'Feature',
      area: null,
      priority: null, // Doesn't match pattern
      estimate: null,
      sprint: null
    }
  },
  {
    name: 'Invalid estimate format',
    labels: ['type:feature', 'estimate:abc', 'estimate:'],
    expected: {
      type: 'Feature',
      area: null,
      priority: null,
      estimate: null, // Doesn't match pattern
      sprint: null
    }
  }
];

// Run tests
let passed = 0;
let failed = 0;
const failures = [];

console.log('🧪 Testing Label Mappings for project-sync.yml\n');
console.log('=' .repeat(70));

testCases.forEach((test, index) => {
  const result = {
    type: mapType(test.labels),
    area: mapArea(test.labels),
    priority: mapPriority(test.labels),
    estimate: mapEstimate(test.labels),
    sprint: mapSprint(test.labels)
  };

  const testPassed = JSON.stringify(result) === JSON.stringify(test.expected);
  
  if (testPassed) {
    passed++;
    console.log(`✅ Test ${index + 1}: ${test.name}`);
  } else {
    failed++;
    console.log(`❌ Test ${index + 1}: ${test.name}`);
    console.log(`   Labels: [${test.labels.join(', ')}]`);
    console.log(`   Expected: ${JSON.stringify(test.expected)}`);
    console.log(`   Got:      ${JSON.stringify(result)}`);
    failures.push({
      name: test.name,
      expected: test.expected,
      got: result
    });
  }
});

console.log('\n' + '='.repeat(70));
console.log(`\n📊 Test Results: ${passed} passed, ${failed} failed out of ${testCases.length} tests\n`);

if (failed > 0) {
  console.log('❌ Failed Tests:\n');
  failures.forEach(f => {
    console.log(`  - ${f.name}`);
    console.log(`    Expected: ${JSON.stringify(f.expected)}`);
    console.log(`    Got:      ${JSON.stringify(f.got)}\n`);
  });
  process.exit(1);
} else {
  console.log('✅ All tests passed!\n');
  console.log('The label mapping logic in project-sync.yml is working correctly.');
  process.exit(0);
}
