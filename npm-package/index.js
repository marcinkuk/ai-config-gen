#!/usr/bin/env node
// ai-config-gen npm: CLI wrapper for the Python ai-config-gen tool
// Usage: npx ai-config-gen <project-path> [options]
// Options:
//   --format <claude|cursor|windsurf>  Generate only one format
//   --formats <claude,cursor,windsurf> Generate multiple formats
//   --verbose                          Show analysis details
//   --dry-run                          Show what would be generated without writing files
//   --output, -o <dir>                 Output directory (default: project root)

const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Parse arguments
let targetDir = '.';
let format = null;
let formats = null;
let verbose = false;
let dryRun = false;
let output = null;

const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--format' && args[i + 1]) {
    format = args[++i];
  } else if (args[i] === '--formats' && args[i + 1]) {
    formats = args[++i];
  } else if (args[i] === '--verbose') {
    verbose = true;
  } else if (args[i] === '--dry-run') {
    dryRun = true;
  } else if ((args[i] === '--output' || args[i] === '-o') && args[i + 1]) {
    output = args[++i];
  } else if (!args[i].startsWith('-')) {
    targetDir = args[i];
  }
}

const resolved = path.resolve(targetDir);

if (!fs.existsSync(resolved) || !fs.statSync(resolved).isDirectory()) {
  console.error(`Error: Directory not found: ${resolved}`);
  process.exit(1);
}

// Build command arguments for the Python CLI
const cmdArgs = [resolved];
if (format) cmdArgs.push('--format', format);
if (formats) cmdArgs.push('--formats', formats);
if (verbose) cmdArgs.push('--verbose');
if (dryRun) cmdArgs.push('--dry-run');
if (output) cmdArgs.push('--output', output);

// Run the Python CLI
const result = spawnSync('ai-config-gen', cmdArgs, {
  stdio: 'inherit',
  shell: process.platform === 'win32' ? 'cmd.exe' : false,
});

// Handle errors
if (result.error) {
  if (result.error.code === 'ENOENT') {
    console.error(
      '\nError: "ai-config-gen" command not found.\n' +
      '  This npm package requires the Python "ai-config-gen" CLI to be installed.\n' +
      '  Install it with: pip install ai-config-gen\n' +
      '  Then retry: npx ai-config-gen <path>'
    );
  } else {
    console.error(`\nError running ai-config-gen: ${result.error.message || result.error.code}`);
  }
  process.exit(result.error.code === 'ENOENT' ? 1 : 2);
}

if (result.status !== 0 && result.signal) {
  console.error(`\nai-config-gen was terminated by signal: ${result.signal}`);
  process.exit(128 + (result.signal.charCodeAt(0) || 1));
}

process.exit(result.status || 0);