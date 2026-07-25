# Show HN Launch Post for Hacker News

## Title
Show HN: ai-config-gen – Auto-generate AI coding assistant configs from any codebase

## Body
I built a tool that analyzes any codebase and generates optimized configuration files for AI coding assistants (.claude.md, .cursorrules, .windsurfrules).

**The problem:** Every time you start a new project, you need to write config files that tell Claude Code / Cursor / Windsurf how your project is structured. Nobody wants to do this manually.

**What it does:** One command (`ai-config-gen .`) scans your codebase and generates configs that include:
- Language detection (Python, TypeScript, Rust, Go, Java, etc.)
- Framework identification (Django, FastAPI, React, Next.js, Rails...)
- Architecture patterns (MVC, Clean Architecture, Modular, Monorepo)
- Package managers (pip, npm, cargo, composer...)
- CI/CD, Docker, license detection
- Coding conventions (type hints, async/await, etc.)

**How to use:**
```bash
pip install ai-config-gen
ai-config-gen .
```
It generates .claude.md, .cursorrules, and .windsurfrules in your project root.

It's open source (MIT), has zero dependencies (pure stdlib), and I wrote 25 tests covering every detection path.

https://github.com/marcinkuk/ai-config-gen