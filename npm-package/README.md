# ai-config-gen (npm)

Auto-generate AI coding assistant configuration files for any project.

## What it does

Scans your codebase and generates optimized documentation for AI coding assistants:
- `.claude.md` — Claude / Claude Desktop
- `.cursorrules` — Cursor IDE
- `.github/copilot-instructions.md` — GitHub Copilot
- `.windsurfrules` — Windsurf IDE

Supports 55+ frameworks across 8 languages.

## Install

```bash
npm install -g ai-config-gen
```

## Usage

```bash
# Analyze current directory
ai-config-gen .

# Analyze specific path
ai-config-gen /path/to/project

# Analyze and list only (no files written)
ai-config-gen . --dry-run
```

## Examples

```bash
# Inside a Next.js project
$ cd my-next-app
$ ai-config-gen .

🔍 Analyzing: my-next-app
📦 Language: TypeScript
⚙️  Frameworks: React, Next.js, Tailwind CSS
📦 Package Manager: npm/yarn/pnpm
🧪 Test Frameworks: Jest

Generated:
  ✓ .claude.md
  ✓ .cursorrules
  ✓ .github/copilot-instructions.md
  ✓ .windsurfrules
```

## Requirements

- Node.js 18+
- Python 3.9+ (for the underlying analysis engine)
- `ai-config-gen` pip package must be installed: `pip install ai-config-gen`

## GitHub

https://github.com/marcinkuk/ai-config-gen

## License

MIT