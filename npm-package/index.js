#!/usr/bin/env node
// ai-config-gen: Node.js wrapper around the Python CLI
// Usage: npx ai-config-gen <project-path>
// or:    ai-config-gen <project-path>

const { execSync } = require('child_process');
const path = require('path');

const targetDir = process.argv[2] || '.';
const resolved = path.resolve(targetDir);

console.log(`🔍 ai-config-gen: Analyzing ${resolved}`);

try {
  // Try to invoke the Python CLI (requires pip install ai-config-gen)
  const output = execSync(`ai-config-gen "${resolved}"`, {
    stdio: 'inherit',
    shell: process.platform === 'win32' ? 'cmd.exe' : '/bin/sh',
  });
  console.log(output.toString());
} catch (e) {
  // Fallback: warn user to install Python version
  console.error(
    '❌ Python CLI "ai-config-gen" not found.\n' +
    '   Install it first: pip install ai-config-gen\n' +
    '   Then retry: ai-config-gen <path>'
  );
  process.exit(1);
}