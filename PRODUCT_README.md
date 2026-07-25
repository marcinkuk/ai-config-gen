# ai-config-gen

> **Analyze any codebase → Generate optimized AI coding assistant config files**

One command. Three config formats. Zero guesswork.

```bash
pip install ai-config-gen
ai-config-gen .
```

Generates `.claude.md`, `.cursorrules`, `.windsurfrules` tailored to your codebase's actual architecture, frameworks, and conventions.

## Why?

AI coding assistants (Claude Code, Cursor, Windsurf) need configuration files to understand your project. Writing these manually is tedious. `ai-config-gen` does it automatically by analyzing:

- **Language** & tech stack (Python, TypeScript, Rust, Go, etc.)
- **Frameworks** (Django, React, FastAPI, Next.js, Rails, etc.)
- **Architecture** (MVC, Clean Architecture, Modular, Monorepo, etc.)
- **Conventions** (type hints, async/await, class vs function-oriented)
- **Package managers** (pip, npm, cargo, composer, etc.)
- **CI/CD** (GitHub Actions, GitLab CI, etc.)
- **Docker**, **testing**, **license**

## Installation

```bash
pip install ai-config-gen
```

## Usage

```bash
# Auto-detect & generate all configs for current directory
ai-config-gen .

# Generate for a specific project
ai-config-gen /path/to/project

# Only generate .claude.md
ai-config-gen --format claude

# Generate multiple formats
ai-config-gen --formats claude,cursor

# Preview without writing files
ai-config-gen --dry-run

# See detailed analysis
ai-config-gen --verbose

# Save to custom directory
ai-config-gen -o ./output-dir
```

## Output Formats

| Format | File | Target |
|--------|------|--------|
| `claude` | `.claude.md` | Claude Code / Anthropic |
| `cursor` | `.cursorrules` | Cursor IDE |
| `windsurf` | `.windsurfrules` | Windsurf IDE |

## Example

```bash
$ ai-config-gen /path/to/my-python-app --verbose

============================================================
Project Analysis: my-python-app
============================================================
  Language:    Python
  Files:       42
  Lines:       3,847
  Frameworks:  FastAPI, pytest
  Package Mgr: pip/uv/poetry
  Has Git:     True
  Has Docker:  True
  Has CI/CD:   True (GitHub Actions)
  License:     MIT
  Patterns:    Modular structure (src), API/REST structure
  Conventions: Python with type hints, Heavy async/await usage
============================================================

Generated: /path/to/my-python-app/.claude.md
Generated: /path/to/my-python-app/.cursorrules
Generated: /path/to/my-python-app/.windsurfrules
```

## What Gets Generated

The tool creates config files that tell AI assistants:
- What language and frameworks you use
- How to run your tests and build
- What architectural patterns to respect
- What coding conventions to follow
- Where to find entry points and key files
- How to run Docker, CI/CD, etc.

## Supported Languages

Python, JavaScript, TypeScript, Rust, Go, Java, Kotlin, Ruby, PHP, C#, C++, Swift

## License

MIT

## Support

Find this useful? [Become a Sponsor](https://github.com/sponsors/ai-config-gen) ❤️