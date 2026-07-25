#!/usr/bin/env node
// Test script for ai-config-gen npm wrapper
const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

let passed = 0;
let failed = 0;
const testDir = path.join(__dirname, '..', 'test_projects', 'python_fastapi');

// Helper to run index.js with given args
function run(args) {
  return spawnSync('node', [path.join(__dirname, 'index.js'), ...args], {
    stdio: ['pipe', 'pipe', 'pipe'],
    shell: process.platform === 'win32' ? 'cmd.exe' : false,
  });
}

function assert(condition, msg) {
  if (condition) {
    passed++;
    console.log(`  ✓ ${msg}`);
  } else {
    failed++;
    console.error(`  ✗ ${msg}`);
  }
}

// Test 1: dry-run on a valid project directory
console.log('\nTest 1: dry-run on valid project');
if (fs.existsSync(testDir)) {
  const r = run([testDir, '--dry-run']);
  assert(r.status === 0, 'exit code 0');
  const out = r.stdout ? r.stdout.toString() : '';
  assert(out.length > 0, 'has stdout output');
} else {
  console.log('  ⊘ skipped (no test directory)');
}

// Test 2: non-existent directory should fail
console.log('\nTest 2: non-existent directory');
const r2 = run(['/nonexistent/path/12345']);
assert(r2.status === 1, 'exit code 1');
const err = r2.stderr.toString();
assert(err.includes('not found') || err.includes('Error'), 'shows error message');

// Test 3: current directory as default (uses .)
console.log('\nTest 3: default directory (current dir)');
const r3 = run(['--dry-run']);
// Should succeed or fail gracefully with exit code 0 or 1
assert(r3.status !== undefined && r3.status !== null, 'returns some exit code');

// Test 4: --format flag
console.log('\nTest 4: --format flag');
if (fs.existsSync(testDir)) {
  const r4 = run([testDir, '--format', 'claude', '--dry-run']);
  assert(r4.status === 0, 'exit code 0 with --format');
}

// Test 5: --formats flag
console.log('\nTest 5: --formats flag');
if (fs.existsSync(testDir)) {
  const r5 = run([testDir, '--formats', 'claude,cursor', '--dry-run']);
  assert(r5.status === 0, 'exit code 0 with --formats');
}

// Test 6: --output flag
console.log('\nTest 6: --output flag');
if (fs.existsSync(testDir)) {
  const r6 = run([testDir, '--output', '/tmp/ai-config-test-out', '--dry-run']);
  assert(r6.status === 0, 'exit code 0 with --output');
}

// Summary
console.log(`\n${'─'.repeat(40)}`);
console.log(`Results: ${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);