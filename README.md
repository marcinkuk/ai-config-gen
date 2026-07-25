# ai-config-gen

[![PyPI](https://img.shields.io/pypi/v/ai-config-gen.svg)](https://pypi.org/project/ai-config-gen/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ai-config-gen.svg)](https://pypi.org/project/ai-config-gen/)
[![Python](https://img.shields.io/pypi/pyversions/ai-config-gen.svg)](https://pypi.org/project/ai-config-gen/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/marcinkuk/ai-config-gen/actions/workflows/ci.yml/badge.svg)](https://github.com/marcinkuk/ai-config-gen/actions)

> **Stop writing AI config files by hand.** Analyze any codebase and generate `.claude.md`, `.cursorrules`, `.windsurfrules` in one command. 55+ frameworks auto-detected. Zero dependencies.

```bash
pip install ai-config-gen
ai-config-gen /path/to/project
# ✨ Generated .claude.md, .cursorrules, .windsurfrules
```

## Why ai-config-gen?

Every project needs config files that tell AI coding assistants (Claude Code, Cursor, Windsurf, GitHub Copilot) about its architecture, frameworks, and conventions. Writing these manually takes **hours per project**. This tool does it in **seconds**.

| Feature | Manual | ai-config-gen |
|---------|--------|---------------|
| Time per project | 30-120 min | < 2 sec |
| Framework coverage | What you remember | 55+ auto-detected |
| Accuracy | Error-prone | 100% file-based analysis |
| Consistency | Varies | Identical every run |

## Installation

```bash
pip install ai-config-gen
```

Zero external dependencies. Pure Python stdlib.

## Usage

```bash
# Analyze current directory
ai-config-gen .

# Analyze specific project
ai-config-gen /path/to/project

# Generate only .claude.md
ai-config-gen . --format claude

# Generate multiple formats
ai-config-gen . --formats claude,cursor

# Verbose output
ai-config-gen . --verbose
```

**Output:** Three config files in your project root:
- `.claude.md` — For Claude Code / Anthropic
- `.cursorrules` — For Cursor IDE
- `.windsurfrules` — For Windsurf IDE

## Features

### Auto-detection (50+ frameworks & tools)

**Python:** Django, Flask, FastAPI, Django REST, Tornado, Starlette, Sanic, Pyramid, Bottle, pytest, unittest, nose, hypothesis, Pandas, NumPy, Scikit-learn, TensorFlow, PyTorch, MLflow, Jupyter, Poetry, Pipenv, Setuptools

**JavaScript/TypeScript:** React, Next.js, Vue.js, Angular, Svelte, Remix, Astro, Nuxt, Gatsby, Ember.js, Node.js, Express.js, Koa.js, NestJS, Hapi, Socket.io

**CSS/Styling:** Tailwind CSS, Sass/SCSS, Stylus, LESS, Styled Components

**Java/Kotlin:** Spring Boot, Spring MVC, Jakarta EE, Gradle, Maven

**PHP:** Laravel, Symfony, CodeIgniter, WordPress

**Ruby:** Rails, Sinatra

**Rust:** Cargo, Actix, Rocket, Tokio

**Go:** Gin, Echo, Fiber

**Testing (JS):** Jest, Mocha, Cypress, Playwright

### What's detected

- ✅ Languages (14+ supported)
- ✅ Frameworks (50+ indicators)
- ✅ Architecture patterns (MVC, Clean Architecture, Modular, Monorepo)
- ✅ Package managers (npm, pip, cargo, composer, bundler, pub, etc.)
- ✅ Build tools (Makefile, webpack, rollup, vite, etc.)
- ✅ CI/CD (GitHub Actions, GitLab CI, Travis, CircleCI, Jenkins)
- ✅ Docker, Docker Compose
- ✅ License detection
- ✅ Coding conventions (type hints, async/await, class-based, functional)

## Examples

### Python FastAPI project

```bash
$ ai-config-gen ./my-api
🔍 Analyzing ./my-api...
📊 Detected: Python + FastAPI + pytest + Docker + MIT
✨ Generated: .claude.md, .cursorrules, .windsurfrules
```

Generated `.claude.md` includes:
- Project name, language, frameworks
- Architecture pattern (Clean Architecture / MVC / etc.)
- Package manager, build tools
- Testing setup, CI/CD pipeline
- Coding conventions specific to this project

### TypeScript Next.js project

```bash
$ ai-config-gen ./my-website
🔍 Analyzing ./my-website...
📊 Detected: TypeScript + Next.js + Tailwind CSS + Jest
✨ Generated: .claude.md, .cursorrules, .windsurfrules
```

## Distribution

### VSCode Extension

Generate configs with one click from the VSCode command palette:

| Marketplace | Install |
|-------------|---------|
| [![VSCode Marketplace](https://img.shields.io/badge/VSCode-Marketplace-blue)](https://marketplace.visualstudio.com/items?itemName=marcinkuk.ai-config-gen-vscode) | Download `.vsix` from [Releases](https://github.com/marcinkuk/ai-config-gen/releases) |

```bash
# Or build from source
cd vscode-extension && npm install && npm run compile
```

### npm Package

Use the npm wrapper for Node.js projects:

```bash
npm install -g ai-config-gen
ai-config-gen /path/to/project
```

### Docker

```bash
docker build -t ai-config-gen .
docker run -p 8011:8011 ai-config-gen
```

### Web API

Self-hosted FastAPI server with rate limiting:

```bash
pip install ai-config-gen
serve-instruct
```

Starts on `http://localhost:8011` with 10 req/min free tier.

## Pricing

| Plan | Price | Best For |
|------|-------|----------|
| **Free** | $0 | Individual developers |
| **Pro** | $9/mo | Teams needing API access |
| **Enterprise** | Custom | Self-hosted + SLA |

[View full pricing →](https://github.com/marcinkuk/ai-config-gen/tree/main/static/pricing.html)

## Support the Project

ai-config-gen is free and open source. If it saves you time, consider supporting the work:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-%245%2Fmonth-orange)](https://github.com/sponsors/marcinkuk)

## Contributing

Issues, PRs, and feature requests welcome. Run the test suite before submitting:

```bash
python -m pytest -v --ignore=test_projects
```

All 25 tests must pass.

## License

MIT — see [LICENSE](LICENSE) for details.