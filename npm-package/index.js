#!/usr/bin/env node
// ai-config-gen npm: Auto-generate AI coding assistant config files
// Usage: npx ai-config-gen <project-path> [options]
// Options:
//   --format <claude|cursor|windsurf>  Generate only one format
//   --formats <claude,cursor,windsurf> Generate multiple formats
//   --verbose                          Show analysis details

const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Parse arguments
let targetDir = '.';
let format = null;
let formats = null;
let verbose = false;

const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--format' && args[i + 1]) {
    format = args[++i];
  } else if (args[i] === '--formats' && args[i + 1]) {
    formats = args[++i];
  } else if (args[i] === '--verbose') {
    verbose = true;
  } else if (!args[i].startsWith('-')) {
    targetDir = args[i];
  }
}

const resolved = path.resolve(targetDir);

if (!fs.existsSync(resolved) || !fs.statSync(resolved).isDirectory()) {
  console.error(`❌ Directory not found: ${resolved}`);
  process.exit(1);
}

console.log(`🔍 ai-config-gen: Analyzing ${resolved}`);

// Build command arguments
const cmdArgs = [resolved];
if (format) cmdArgs.push('--format', format);
if (formats) cmdArgs.push('--formats', formats);
if (verbose) cmdArgs.push('--verbose');

// Run the Python CLI
const result = spawnSync('ai-config-gen', cmdArgs, {
  stdio: 'inherit',
  shell: process.platform === 'win32' ? 'cmd.exe' : '/bin/sh',
});

if (result.status !== 0) {
  console.error(
    '\n❌ Python CLI "ai-config-gen" not found or failed.\n' +
    '   Install it first: pip install ai-config-gen\n' +
    '   Then retry: npx ai-config-gen <path>'
  );
  process.exit(result.status || 1);
}