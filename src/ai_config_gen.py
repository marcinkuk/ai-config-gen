#!/usr/bin/env python3
"""
ai-config-gen: Analyze any codebase and generate optimized config files
for AI coding assistants (.claude.md, .cursorrules, .windsurfrules, etc.)

Usage:
    ai-config-gen .                          # Auto-detect & generate for current directory
    ai-config-gen /path/to/project           # Generate for specific path
    ai-config-gen --format claude            # Only generate .claude.md
    ai-config-gen --formats claude,cursor    # Generate multiple formats
    ai-config-gen --verbose                  # Show analysis details
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class ProjectInfo:
    """Extracted information about a codebase."""
    name: str = ""
    language: str = ""
    languages: dict = field(default_factory=dict)
    frameworks: List[str] = field(default_factory=list)
    package_manager: str = ""
    build_tools: List[str] = field(default_factory=list)
    test_frameworks: List[str] = field(default_factory=list)
    has_git: bool = False
    has_docker: bool = False
    has_ci: bool = False
    ci_type: str = ""
    file_count: int = 0
    total_lines: int = 0
    has_dependencies: bool = False
    license_type: str = ""
    has_readme: bool = False
    entry_points: List[str] = field(default_factory=list)
    key_files: List[str] = field(default_factory=list)
    patterns: List[str] = field(default_factory=list)
    conventions: List[str] = field(default_factory=list)
    tech_stack: List[str] = field(default_factory=list)


# File patterns for detection
CODE_LANGUAGES = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".kt": "Kotlin",
    ".rs": "Rust",
    ".go": "Go",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".cpp": "C++",
    ".c": "C",
    ".swift": "Swift",
    ".vue": "Vue.js",
    ".svelte": "Svelte",
}

CONFIG_FORMATS = {
    ".css": "CSS",
    ".scss": "SCSS",
    ".html": "HTML",
    ".sql": "SQL",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".json": "JSON",
    ".toml": "TOML",
    ".xml": "XML",
}

LANGUAGE_EXTENSIONS = {**CODE_LANGUAGES, **CONFIG_FORMATS}

FRAMEWORK_INDICATORS = {
    # Python web frameworks
    "Django": ["django", "wsgi.py", "manage.py", "settings.py"],
    "Flask": ["flask", "app.py", "app/__init__.py"],
    "FastAPI": ["fastapi", "uvicorn"],
    "Django REST": ["djangorestframework", "rest_framework"],
    "Tornado": ["tornado"],
    "Starlette": ["starlette"],
    "Sanic": ["sanic"],
    "Pyramid": ["pyramid", "pylons"],
    "Bottle": ["bottle"],
    # Python testing
    "pytest": ["pytest", "test_", "conftest.py"],
    "unittest": ["unittest", "test_"],
    "nose": ["nose", "nose2"],
    "hypothesis": ["hypothesis"],
    # Python data/ML
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Scikit-learn": ["sklearn", "scikit-learn"],
    "TensorFlow": ["tensorflow", "tf."],
    "PyTorch": ["torch", "pytorch"],
    "MLflow": ["mlflow"],
    "Jupyter": ["jupyter", ".ipynb"],
    # JavaScript/TypeScript frontend
    "React": ["react", "react-dom", ".jsx", ".tsx"],
    "Next.js": ["next", "next.config"],
    "Vue.js": ["vue", "vue-cli-service"],
    "Angular": ["angular", "@angular"],
    "Svelte": ["svelte", "sveltekit"],
    "Remix": ["remix", "@remix-run"],
    "Astro": ["astro"],
    "Nuxt": ["nuxt", "nuxt.config"],
    "Gatsby": ["gatsby", "gatsby-node"],
    "Ember.js": ["ember", "@ember"],
    # JavaScript/TypeScript backend
    "Node.js": ["node", "express", "koa", "fastify"],
    "Express.js": ["express"],
    "Koa.js": ["koa"],
    "NestJS": ["@nestjs", "nest"],
    "Hapi": ["hapi", "@hapi"],
    "Socket.io": ["socket.io"],
    # CSS/Styling
    "Tailwind CSS": ["tailwindcss", "tailwind.config"],
    "Sass/SCSS": ["sass", "scss"],
    "Stylus": ["stylus"],
    "LESS": ["less"],
    "Styled Components": ["styled-components"],
    # Java/Kotlin
    "Spring Boot": ["spring-boot", "Application.java"],
    "Spring MVC": ["spring-webmvc", "spring-mvc"],
    "Jakarta EE": ["jakarta", "javax.servlet"],
    "Gradle": ["gradle", "build.gradle"],
    "Maven": ["maven", "pom.xml"],
    # PHP
    "Laravel": ["laravel", "artisan", "composer.json"],
    "Symfony": ["symfony"],
    "CodeIgniter": ["codeigniter", "application/config"],
    "WordPress": ["wordpress", "wp-content"],
    # Ruby
    "Rails": ["rails", "Gemfile", "config/routes.rb"],
    "Sinatra": ["sinatra"],
    # Rust
    "Cargo": ["cargo", "Cargo.toml"],
    "Actix": ["actix"],
    "Rocket": ["rocket"],
    "Tokio": ["tokio"],
    # Go
    "Gin": ["gin-gonic", "gin"],
    "Echo": ["labstack", "echo"],
    "Fiber": ["gofiber", "fiber"],
    # Testing (JS)
    "Jest": ["jest", "@testing-library"],
    "Mocha": ["mocha"],
    "Cypress": ["cypress"],
    "Playwright": ["playwright", "@playwright"],
    # Python packaging
    "Poetry": ["poetry", "poetry.lock"],
    "Pipenv": ["pipenv", "Pipfile"],
    "Setuptools": ["setuptools", "setup.py"],
}

PACKAGE_MANAGERS = {
    "package.json": "npm/yarn/pnpm",
    "requirements.txt": "pip",
    "pyproject.toml": "pip/uv/poetry",
    "Cargo.toml": "cargo",
    "go.mod": "go mod",
    "Gemfile": "bundler",
    "composer.json": "composer",
    "pubspec.yaml": "pub",
    "pom.xml": "maven",
}

IGNORE_DIRS = {
    "__pycache__", ".git", "node_modules", ".venv", "venv", ".tox",
    ".eggs", "dist", "build", ".next", ".svelte-kit", ".output",
    ".cache", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "target", ".cargo", ".nyc_output", "coverage", ".coverage",
}


class ProjectAnalyzer:
    """Analyzes a codebase to extract structured project information."""

    def __init__(self, project_path: str, verbose: bool = False):
        self.project_path = Path(project_path).resolve()
        self.verbose = verbose
        self.info = ProjectInfo(name=self.project_path.name)

    def analyze(self) -> ProjectInfo:
        """Run full analysis pipeline."""
        self._analyze_name()
        self._analyze_languages()
        self._analyze_packages_and_frameworks()
        self._analyze_git()
        self._analyze_docker()
        self._analyze_ci()
        self._analyze_file_structure()
        self._analyze_patterns()
        self._analyze_conventions()

        if self.verbose:
            self._print_summary()

        return self.info

    def _analyze_name(self):
        """Extract project name from config files."""
        # Check pyproject.toml
        pyproject = self.project_path / "pyproject.toml"
        if pyproject.exists():
            for line in pyproject.read_text().splitlines():
                if line.strip().startswith("name ="):
                    self.info.name = line.split("=", 1)[1].strip().strip('"\'')
                    break

        # Check package.json
        package = self.project_path / "package.json"
        if package.exists():
            try:
                data = json.loads(package.read_text())
                if "name" in data:
                    self.info.name = data["name"]
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass

        # Check Cargo.toml
        cargo = self.project_path / "Cargo.toml"
        if cargo.exists():
            for line in cargo.read_text().splitlines():
                if line.strip().startswith("name ="):
                    self.info.name = line.split("=", 1)[1].strip().strip('"\'')
                    break

        # Fallback to directory name
        if not self.info.name:
            self.info.name = self.project_path.name

    def _analyze_languages(self):
        """Detect primary language and count all languages."""
        ext_counts = Counter()
        for root, dirs, files in os.walk(self.project_path):
            # Skip ignored dirs
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in LANGUAGE_EXTENSIONS:
                    ext_counts[ext] += 1
                # Count all files
                filepath = os.path.join(root, f)
                try:
                    if os.path.getsize(filepath) < 100000:  # Skip huge files
                        with open(filepath, "r", errors="replace") as fh:
                            lines = sum(1 for _ in fh)
                            self.info.total_lines += lines
                except (OSError, PermissionError):
                    pass

        # Map extensions to languages
        for ext, lang in LANGUAGE_EXTENSIONS.items():
            count = ext_counts.get(ext, 0)
            if count:
                self.info.languages[lang] = self.info.languages.get(lang, 0) + count

        # Determine primary language
        if self.info.languages:
            self.info.language = max(self.info.languages, key=self.info.languages.get)

    def _analyze_packages_and_frameworks(self):
        """Detect package managers, frameworks, and build tools."""
        config_files = {}
        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for f in files:
                if f in PACKAGE_MANAGERS:
                    config_files[f] = os.path.join(root, f)

        # Detect package manager
        for fname, manager in PACKAGE_MANAGERS.items():
            if fname in config_files:
                self.info.package_manager = manager
                self.info.has_dependencies = True
                self.info.key_files.append(fname)

        # Detect frameworks
        dependency_content = ""
        for fname, fpath in config_files.items():
            try:
                content = Path(fpath).read_text(errors="replace").lower()
                dependency_content += content
            except (OSError, UnicodeDecodeError):
                pass

        for framework, indicators in FRAMEWORK_INDICATORS.items():
            for indicator in indicators:
                if indicator.lower() in dependency_content:
                    if framework not in self.info.frameworks:
                        self.info.frameworks.append(framework)
                    break

        # Detect test frameworks
        for fname in config_files:
            fpath = config_files[fname]
            try:
                content = Path(fpath).read_text(errors="replace").lower()
                if "pytest" in content or "unittest" in content:
                    self.info.test_frameworks.append("pytest")
                if "jest" in content:
                    self.info.test_frameworks.append("Jest")
                if "mocha" in content or "chai" in content:
                    self.info.test_frameworks.append("Mocha/Chai")
            except (OSError, UnicodeDecodeError):
                pass

        # Check for test directories
        if (self.project_path / "tests").exists() or (self.project_path / "test").exists():
            if not self.info.test_frameworks:
                self.info.test_frameworks.append("unknown")

        # Detect build tools
        if (self.project_path / "Makefile").exists():
            self.info.build_tools.append("make")
        if (self.project_path / "webpack.config.js").exists() or (self.project_path / "webpack.config.ts").exists():
            self.info.build_tools.append("webpack")
        if (self.project_path / "vite.config.js").exists() or (self.project_path / "vite.config.ts").exists():
            self.info.build_tools.append("vite")
        if (self.project_path / "rollup.config.js").exists():
            self.info.build_tools.append("rollup")

        # Collect tech stack
        self.info.tech_stack = (
            [self.info.language] + self.info.frameworks + self.info.build_tools + self.info.test_frameworks
        )
        self.info.tech_stack = [x for x in self.info.tech_stack if x]

    def _analyze_git(self):
        """Check for git repository and extract info."""
        git_dir = self.project_path / ".git"
        self.info.has_git = git_dir.exists()

        # Check for LICENSE
        for license_file in ["LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE"]:
            if (self.project_path / license_file).exists():
                try:
                    content = (self.project_path / license_file).read_text(errors="replace").lower()
                    if "mit" in content:
                        self.info.license_type = "MIT"
                    elif "apache" in content:
                        self.info.license_type = "Apache-2.0"
                    elif "gpl" in content:
                        self.info.license_type = "GPL"
                    elif "bsd" in content:
                        self.info.license_type = "BSD"
                    elif "mpl" in content:
                        self.info.license_type = "MPL-2.0"
                    elif "isc" in content:
                        self.info.license_type = "ISC"
                    else:
                        self.info.license_type = "Custom"
                    self.info.key_files.append(license_file)
                    break
                except (OSError, UnicodeDecodeError):
                    pass

        # Check for .gitignore
        if (self.project_path / ".gitignore").exists():
            self.info.key_files.append(".gitignore")

    def _analyze_docker(self):
        """Check for Docker files."""
        dockerfiles = ["Dockerfile", "Dockerfile.dev", "docker-compose.yml", "docker-compose.yaml"]
        for df in dockerfiles:
            if (self.project_path / df).exists():
                self.info.has_docker = True
                self.info.key_files.append(df)
                break

    def _analyze_ci(self):
        """Check for CI/CD configuration."""
        ci_configs = {
            ".github/workflows": "GitHub Actions",
            ".gitlab-ci.yml": "GitLab CI",
            ".circleci/config.yml": "CircleCI",
            "Jenkinsfile": "Jenkins",
            ".travis.yml": "Travis CI",
            ".github/actions": "GitHub Actions",
        }
        for pattern, ci_name in ci_configs.items():
            if pattern.startswith(".github"):
                ci_dir = self.project_path / pattern
                if ci_dir.exists():
                    self.info.has_ci = True
                    self.info.ci_type = ci_name
                    self.info.key_files.append(pattern)
                    break
            elif pattern.startswith(".gitlab"):
                if (self.project_path / pattern).exists():
                    self.info.has_ci = True
                    self.info.ci_type = ci_name
                    self.info.key_files.append(pattern)
                    break
            else:
                if (self.project_path / pattern).exists():
                    self.info.has_ci = True
                    self.info.ci_type = ci_name
                    self.info.key_files.append(pattern)
                    break

    def _analyze_file_structure(self):
        """Count files and identify entry points."""
        total = 0
        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            total += len(files)
        self.info.file_count = total

        # Detect entry points
        entry_patterns = {
            "main.py": "Python",
            "__main__.py": "Python",
            "app.py": "Python/Flask",
            "manage.py": "Django",
            "main.rs": "Rust",
            "main.go": "Go",
            "index.js": "Node.js",
            "index.ts": "Node.js/TypeScript",
            "index.html": "Static/Web",
            "Cargo.toml": "Rust/Cargo",
            "package.json": "Node.js/npm",
            "Gemfile": "Ruby/Rails",
            "composer.json": "PHP/Laravel",
            "go.mod": "Go",
            "pyproject.toml": "Python",
        }
        for entry, lang in entry_patterns.items():
            if (self.project_path / entry).exists():
                self.info.entry_points.append(f"{entry} ({lang})")

        # Check for README
        for readme_name in ["README.md", "README", "README.rst", "README.txt"]:
            if (self.project_path / readme_name).exists():
                self.info.has_readme = True
                self.info.key_files.append(readme_name)
                break

    def _analyze_patterns(self):
        """Detect architectural patterns from file structure."""
        patterns = []

        # MVC / Controller pattern
        if any((self.project_path / d).exists() for d in ["controllers", "views", "models", "routes"]):
            patterns.append("MVC architecture")

        # Layered / Clean architecture
        if any((self.project_path / d).exists() for d in ["domain", "infrastructure", "application", "presentation"]):
            patterns.append("Clean Architecture")

        # Modular / Package-based
        src_dirs = [d for d in ["src", "lib", "core", "pkg"] if (self.project_path / d).exists()]
        if src_dirs:
            patterns.append(f"Modular structure ({', '.join(src_dirs)})")

        # Monorepo detection
        if (self.project_path / "packages").exists() or (self.project_path / "apps").exists():
            patterns.append("Monorepo structure")

        # Plugin/Extension architecture
        if any((self.project_path / d).exists() for d in ["plugins", "extensions", "extensions"]):
            patterns.append("Plugin architecture")

        # API-first / REST
        if any((self.project_path / d).exists() for d in ["api", "routes", "controllers", "endpoints"]):
            patterns.append("API/REST structure")

        # Frontend framework patterns
        if (self.project_path / "components").exists():
            patterns.append("Component-based UI")
        if (self.project_path / "pages").exists():
            patterns.append("Page-based routing")

        self.info.patterns = patterns

    def _analyze_conventions(self):
        """Detect coding conventions by sampling source files."""
        conventions = []
        source_files = []

        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in (".py", ".js", ".ts", ".tsx", ".jsx", ".rs", ".go", ".java"):
                    source_files.append(os.path.join(root, f))

        # Sample up to 20 files for convention detection
        sample = source_files[:20]
        total_imports = 0
        total_class_definitions = 0
        total_function_definitions = 0
        has_type_hints = False
        has_ts_types = False

        for filepath in sample:
            try:
                rel = os.path.relpath(filepath, self.project_path)
                content = Path(filepath).read_text(errors="replace")
                lines = content.split("\n")
                ext = os.path.splitext(filepath)[1].lower()

                # Count imports
                if ext == ".py":
                    total_imports += sum(1 for l in lines if l.strip().startswith(("import ", "from ")))
                    total_function_definitions += sum(1 for l in lines if re.match(r"\s*def\s+", l))
                    total_class_definitions += sum(1 for l in lines if re.match(r"\s*class\s+", l))
                    if re.search(r"def\s+\w+\([^)]*\) ->", content) or re.search(r":\s*\w+\[", content):
                        has_type_hints = True
                elif ext in (".js", ".ts", ".tsx", ".jsx"):
                    total_imports += sum(1 for l in lines if l.strip().startswith(("import ", "require(")))
                    total_function_definitions += sum(1 for l in lines if re.match(r"\s*(async\s+)?(function\s+|const\s+\w+\s*=\s*(async\s+)?(\([^)]*\)|\w+)\s*(=>|))", l))
                    total_class_definitions += sum(1 for l in lines if re.match(r"\s*class\s+", l))
                    if ext in (".ts", ".tsx") and re.search(r":\s*(string|number|boolean|any|void|Array|Promise|interface|type)", content):
                        has_ts_types = True
                elif ext == ".rs":
                    total_imports += sum(1 for l in lines if l.strip().startswith("use "))
                    total_function_definitions += sum(1 for l in lines if re.match(r"\s*(pub\s+)?fn\s+", l))
                    total_class_definitions += sum(1 for l in lines if re.match(r"\s*(pub\s+)?struct\s+", l))
                elif ext == ".go":
                    total_imports += sum(1 for l in lines if l.strip().startswith("import"))
                    total_function_definitions += sum(1 for l in lines if re.match(r"\s*func\s+", l))

            except (OSError, UnicodeDecodeError):
                pass

        if has_type_hints and self.info.language == "Python":
            conventions.append("Python with type hints")
        if has_ts_types:
            conventions.append("TypeScript with explicit types")

        if total_class_definitions > total_function_definitions:
            conventions.append("Class-oriented codebase")
        elif total_function_definitions > total_class_definitions:
            conventions.append("Function-oriented / procedural codebase")

        if total_imports > 50:
            conventions.append("Heavy external dependency usage")

        # Check for async patterns
        async_count = 0
        for filepath in sample:
            try:
                content = Path(filepath).read_text(errors="replace")
                async_count += content.count("async ") + content.count("await ")
            except (OSError, UnicodeDecodeError):
                pass
        if async_count > 5:
            conventions.append("Heavy async/await usage")

        self.info.conventions = conventions

    def _print_summary(self):
        """Print analysis summary for verbose mode."""
        print(f"\n{'='*60}")
        print(f"Project Analysis: {self.info.name}")
        print(f"{'='*60}")
        print(f"  Language:    {self.info.language}")
        print(f"  Files:       {self.info.file_count}")
        print(f"  Lines:       {self.info.total_lines:,}")
        print(f"  Frameworks:  {', '.join(self.info.frameworks) or 'None detected'}")
        print(f"  Package Mgr: {self.info.package_manager or 'None'}")
        print(f"  Build Tools: {', '.join(self.info.build_tools) or 'None'}")
        print(f"  Test Frames: {', '.join(self.info.test_frameworks) or 'None'}")
        print(f"  Has Git:     {self.info.has_git}")
        print(f"  Has Docker:  {self.info.has_docker}")
        print(f"  Has CI/CD:   {self.info.has_ci} ({self.info.ci_type})")
        print(f"  License:     {self.info.license_type or 'Unknown'}")
        print(f"  Entry Pts:   {', '.join(self.info.entry_points) or 'None'}")
        print(f"  Patterns:    {', '.join(self.info.patterns) or 'None'}")
        print(f"  Conventions: {', '.join(self.info.conventions) or 'None'}")
        print(f"{'='*60}\n")


class ConfigGenerator:
    """Generates AI coding assistant config files from project analysis."""

    def __init__(self, info: ProjectInfo, project_path: Path):
        self.info = info
        self.project_path = project_path

    def generate_claude_md(self) -> str:
        """Generate .claude.md configuration file."""
        sections = []

        # Project overview
        sections.append("# Project Overview")
        sections.append(f"**Project:** {self.info.name}")
        sections.append(f"**Primary Language:** {self.info.language}")
        sections.append(f"**Tech Stack:** {', '.join(self.info.tech_stack) or 'Standard ' + self.info.language}")

        if self.info.package_manager:
            sections.append(f"**Package Manager:** {self.info.package_manager}")

        sections.append("")

        # Architecture
        if self.info.patterns:
            sections.append("## Architecture")
            for pattern in self.info.patterns:
                sections.append(f"- {pattern}")
            sections.append("")

        # Frameworks
        if self.info.frameworks:
            sections.append("## Frameworks & Libraries")
            for fw in self.info.frameworks:
                sections.append(f"- {fw}")
            sections.append("")

        # Coding Conventions
        if self.info.conventions:
            sections.append("## Coding Conventions")
            for conv in self.info.conventions:
                sections.append(f"- {conv}")
            sections.append("")

        # Key Files
        if self.info.key_files:
            sections.append("## Important Files")
            for kf in self.info.key_files:
                sections.append(f"- `{kf}`")
            sections.append("")

        # Entry Points
        if self.info.entry_points:
            sections.append("## Entry Points")
            for ep in self.info.entry_points:
                sections.append(f"- {ep}")
            sections.append("")

        # Running the project
        sections.append("## Development Commands")
        if self.info.language == "Python":
            if self.info.package_manager == "pip/uv/poetry":
                sections.append("```bash")
                sections.append("# Install dependencies")
                if (self.project_path / "pyproject.toml").exists():
                    sections.append("uv sync  # or: poetry install")
                else:
                    sections.append("pip install -r requirements.txt")
                sections.append("```")
            if self.info.test_frameworks:
                sections.append("```bash")
                sections.append("# Run tests")
                if "pytest" in [f.lower() for f in self.info.test_frameworks]:
                    sections.append("pytest")
                else:
                    sections.append("pytest tests/")
                sections.append("```")
        elif self.info.language in ("JavaScript", "TypeScript"):
            sections.append("```bash")
            sections.append("# Install dependencies")
            sections.append("npm install")
            sections.append("```")
            if self.info.test_frameworks:
                sections.append("```bash")
                sections.append("# Run tests")
                if "Jest" in self.info.test_frameworks:
                    sections.append("npm test  # Jest")
                else:
                    sections.append("npm test")
                sections.append("```")
        elif self.info.language == "Rust":
            sections.append("```bash")
            sections.append("# Build")
            sections.append("cargo build")
            sections.append("# Run tests")
            sections.append("cargo test")
            sections.append("```")
        elif self.info.language == "Go":
            sections.append("```bash")
            sections.append("# Run tests")
            sections.append("go test ./...")
            sections.append("```")

        sections.append("")

        # Docker
        if self.info.has_docker:
            sections.append("## Docker")
            sections.append("```bash")
            sections.append("# Build and run with Docker")
            sections.append("docker build -t " + self.info.name + " .")
            sections.append("docker run -p 8080:8080 " + self.info.name)
            sections.append("```")
            if (self.project_path / "docker-compose.yml").exists():
                sections.append("```bash")
                sections.append("# Or use docker-compose")
                sections.append("docker-compose up")
                sections.append("```")
            sections.append("")

        # CI/CD
        if self.info.has_ci:
            sections.append("## CI/CD")
            sections.append(f"Uses **{self.info.ci_type}** for continuous integration.")
            sections.append("")

        # License
        if self.info.license_type:
            sections.append("## License")
            sections.append(f"This project is licensed under the **{self.info.license_type}** license.")
            sections.append("")

        # AI Assistant Instructions
        sections.append("## AI Assistant Guidelines")
        sections.append("When assisting with this codebase:")
        sections.append("- Follow the existing code style and conventions")
        if self.info.patterns:
            sections.append(f"- Respect the {'; '.join(self.info.patterns)}")
        if self.info.test_frameworks:
            sections.append("- Always include tests for new features")
        sections.append("- Prefer minimal, focused changes over large refactors")
        sections.append("- Add docstrings/comments for complex logic")
        sections.append("- Ensure type hints are used consistently" if self.info.language == "Python" else "")
        sections.append("- Follow the project's dependency management" if self.info.package_manager else "")

        # Remove empty strings from the last section
        sections = [s for s in sections if s]

        return "\n".join(sections) + "\n"

    def generate_cursor_rules(self) -> str:
        """Generate .cursorrules configuration file."""
        lines = []
        lines.append("# AI Coding Assistant Rules for " + self.info.name)
        lines.append("")

        if self.info.language:
            lines.append(f"language: {self.info.language}")
        if self.info.package_manager:
            lines.append(f"package_manager: {self.info.package_manager}")
        if self.info.frameworks:
            lines.append(f"frameworks: [{', '.join(self.info.frameworks)}]")
        lines.append("")

        lines.append("## Code Style")
        if self.info.conventions:
            for conv in self.info.conventions:
                lines.append(f"- {conv}")
        else:
            lines.append("- Follow language-standard conventions")
        lines.append("- Use descriptive variable and function names")
        lines.append("- Keep functions focused and under 50 lines")
        lines.append("- Add comments only for non-obvious logic")
        lines.append("")

        lines.append("## Architecture")
        if self.info.patterns:
            for p in self.info.patterns:
                lines.append(f"- {p}")
        else:
            lines.append("- Maintain clean separation of concerns")
        lines.append("")

        lines.append("## Testing")
        if self.info.test_frameworks:
            lines.append(f"Test framework: {', '.join(self.info.test_frameworks)}")
        lines.append("- Write tests for all new features")
        lines.append("- Ensure existing tests pass before submitting changes")
        lines.append("")

        lines.append("## Safety Rules")
        lines.append("- Never expose secrets or API keys in code")
        lines.append("- Validate all user inputs")
        lines.append("- Use parameterized queries for database operations")
        lines.append("- Handle errors gracefully with proper logging")
        lines.append("")

        lines.append("## Git Workflow")
        lines.append("- Write clear, descriptive commit messages")
        lines.append("- One logical change per commit")
        lines.append("- Use conventional commit format when applicable")

        return "\n".join(lines) + "\n"

    def generate_windsurf_rules(self) -> str:
        """Generate .windsurfrules configuration file."""
        md = self.generate_claude_md()
        # Windsurf uses similar format to Claude
        return md

    def generate_all(self, formats: Optional[List[str]] = None) -> dict:
        """Generate all or specified config formats."""
        generators = {
            "claude": (".claude.md", self.generate_claude_md),
            "cursor": (".cursorrules", self.generate_cursor_rules),
            "windsurf": (".windsurfrules", self.generate_windsurf_rules),
        }

        if not formats:
            formats = list(generators.keys())

        results = {}
        for fmt in formats:
            if fmt in generators:
                filename, gen_func = generators[fmt]
                results[filename] = gen_func()
        return results


def main():
    parser = argparse.ArgumentParser(
        description="Analyze a codebase and generate AI coding assistant config files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ai-config-gen .                          # Auto-detect & generate all configs
  ai-config-gen /path/to/project           # Analyze specific project
  ai-config-gen --format claude            # Only generate .claude.md
  ai-config-gen --formats claude,cursor    # Generate multiple formats
  ai-config-gen --verbose                  # Show analysis details
  ai-config-gen --output ./generated       # Save to custom directory
        """,
    )
    parser.add_argument("project", nargs="?", default=".", help="Path to project directory (default: current)")
    parser.add_argument("--format", choices=["claude", "cursor", "windsurf"], help="Generate only this format")
    parser.add_argument("--formats", help="Comma-separated list of formats to generate")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed analysis output")
    parser.add_argument("--output", "-o", default=None, help="Output directory (default: project root)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated without writing files")

    args = parser.parse_args()

    # Validate project path
    project_path = Path(args.project).resolve()
    if not project_path.is_dir():
        print(f"Error: '{args.project}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    # Determine formats
    if args.format:
        formats = [args.format]
    elif args.formats:
        formats = [f.strip() for f in args.formats.split(",")]
    else:
        formats = ["claude", "cursor", "windsurf"]

    # Analyze
    print(f"Analyzing project: {project_path}")
    analyzer = ProjectAnalyzer(str(project_path), verbose=args.verbose)
    info = analyzer.analyze()

    # Generate
    generator = ConfigGenerator(info, project_path)
    configs = generator.generate_all(formats)

    # Output
    output_dir = Path(args.output) if args.output else project_path
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        for filename, content in configs.items():
            print(f"\n--- Would generate: {filename} ---")
            print(content[:500] + ("..." if len(content) > 500 else ""))
    else:
        generated = []
        for filename, content in configs.items():
            outpath = output_dir / filename
            outpath.write_text(content)
            generated.append(str(outpath))
            print(f"Generated: {outpath}")

        print(f"\nDone! Generated {len(generated)} config file(s).")
        print(f"Files: {', '.join(generated)}")
        print("\n❤️ Like ai-config-gen? Sponsor the developer: https://github.com/sponsors/marcinkuk")
        print("📦 Star the repo: https://github.com/marcinkuk/ai-config-gen")

if __name__ == "__main__":
    main()