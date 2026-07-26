# Changelog

## [v0.5.0] — 2025-07-25

### 🎉 New Features
- **Copilot support**: Generate `.github/copilot-instructions.md` — now covers ALL major AI assistants
- **VSCode extension**: One-click config generation from command palette (`.vsix` ready)
- **npm package**: Node.js CLI wrapper with full flag support + 8 passing tests
- **55+ framework detection**: Python, JS/TS, Java, PHP, Ruby, Rust, Go, CSS frameworks
- **Pro pricing page**: Free / $9/mo Pro / Enterprise tiers defined

### 🔧 Improvements
- Fixed CodeIgniter false-positive detection (`"ci"` → `"application/config"`)
- Added Maven/pom.xml support for Spring Boot detection
- Entry point fix in `pyproject.toml`
- Conversion-optimized README with pricing table + distribution links
- Full CLI flag support: `--format`, `--formats`, `--verbose`, `--dry-run`, `--output`

### 📦 Distribution
- PyPI: `pip install ai-config-gen`
- npm: `npm install -g ai-config-gen`
- VSCode: Download `.vsix` from this release
- Docker: `docker build -t ai-config-gen .`

## [v0.3.0] — 2025-07-25
- Sponsorship banners integrated in CLI output
- Attribution headers on generated config files
- GitHub Pages deployment workflow

## [v0.2.0] — 2025-07-25
- Full metadata, GitHub links, MIT license, keywords
- Language detection fix (TOML → Python for pyproject.toml projects)

## [v0.1.0] — 2025-07-25
- MVP: CLI with ProjectAnalyzer + ConfigGenerator
- 25-test suite, zero external dependencies