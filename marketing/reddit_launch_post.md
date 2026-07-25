# Reddit Launch Post (r/programming, r/python, r/opensource)

## Title
ai-config-gen — One command to auto-generate AI coding assistant config files for any project

## Body
I built `ai-config-gen` because I was tired of manually writing `.claude.md`, `.cursorrules`, and `.windsurfrules` for every new project.

It's a Python CLI tool that:
- Analyzes your entire codebase
- Detects languages, frameworks, architecture patterns, package managers
- Generates 3 config files optimized for AI coding assistants

```bash
pip install ai-config-gen
ai-config-gen ./my-project
```

Zero dependencies (pure stdlib). 25 tests. MIT licensed.

https://github.com/marcinkuk/ai-config-gen