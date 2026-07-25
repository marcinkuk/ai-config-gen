# ai-config-gen (npm wrapper)

This is the **Node.js CLI wrapper** for [ai-config-gen](https://github.com/marcinkuk/ai-config-gen). It calls the Python `ai-config-gen` tool to auto-generate AI coding assistant configuration files for any project.

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

# Preview without writing files
ai-config-gen . --dry-run

# Generate only one format
ai-config-gen . --format claude

# Generate multiple formats
ai-config-gen . --formats claude,cursor

# Save to custom output directory
ai-config-gen . --output ./generated

# Show analysis details
ai-config-gen . --verbose
```

## Examples

```bash
# Inside a Next.js project
$ cd my-next-app
$ ai-config-gen .

Analyzing project: /home/user/my-next-app
Generated: /home/user/my-next-app/.claude.md
Generated: /home/user/my-next-app/.cursorrules
Generated: /home/user/my-next-app/.windsurfrules

Done! Generated 3 config file(s).
```

## Requirements

- **Node.js 18+** (for the npm wrapper)
- **Python 3.9+** (for the underlying analysis engine)
- **`ai-config-gen` pip package** must be installed first:

```bash
pip install ai-config-gen
```

## Develop

```bash
npm test       # Run wrapper tests
npm start      # Run CLI from source
```

## GitHub

https://github.com/marcinkuk/ai-config-gen

## License

MIT