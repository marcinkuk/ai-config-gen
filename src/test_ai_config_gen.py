"""Tests for ai-config-gen: ProjectAnalyzer and ConfigGenerator."""
import json
import os
import tempfile
from pathlib import Path

import pytest

from src.ai_config_gen import ProjectAnalyzer, ConfigGenerator, ProjectInfo


def make_project(tmp_path, structure):
    """Helper to create test project structures."""
    for path, content in structure.items():
        fpath = tmp_path / path
        fpath.parent.mkdir(parents=True, exist_ok=True)
        if content is None:
            fpath.mkdir(exist_ok=True)
        else:
            fpath.write_text(content)
    return tmp_path


class TestProjectAnalyzer:
    """Tests for ProjectAnalyzer."""

    def test_basic_python_project(self, tmp_path):
        """Test basic Python project detection."""
        make_project(tmp_path, {
            "pyproject.toml": '[project]\nname = "myproj"\n',
            "main.py": "def hello(): print('hi')",
            "test_main.py": "def test_hello(): pass",
            "tests": None,
        })
        analyzer = ProjectAnalyzer(str(tmp_path))
        info = analyzer.analyze()

        assert info.name == "myproj"
        assert info.language == "Python"
        assert info.package_manager == "pip/uv/poetry"
        assert info.has_dependencies

    def test_detect_package_json(self, tmp_path):
        """Test Node.js project detection."""
        make_project(tmp_path, {
            "package.json": json.dumps({"name": "my-app", "dependencies": {"react": "^18.0.0"}}),
            "index.js": "console.log('hello')",
        })
        analyzer = ProjectAnalyzer(str(tmp_path))
        info = analyzer.analyze()

        assert info.name == "my-app"
        assert info.language == "JavaScript"
        assert "React" in info.frameworks

    def test_detect_typescript(self, tmp_path):
        """Test TypeScript detection."""
        make_project(tmp_path, {
            "package.json": json.dumps({"name": "ts-app", "dependencies": {"react": "^18.0.0"}}),
            "index.ts": "const x: string = 'hello'",
        })
        analyzer = ProjectAnalyzer(str(tmp_path))
        info = analyzer.analyze()

        assert info.name == "ts-app"
        assert info.language == "TypeScript"

    def test_detect_docker(self, tmp_path):
        """Test Docker file detection."""
        make_project(tmp_path, {
            "Dockerfile": "FROM python:3.13\n",
            "main.py": "pass",
        })
        analyzer = ProjectAnalyzer(str(tmp_path))
        info = analyzer.analyze()

        assert info.has_docker
        assert "Dockerfile" in info.key_files

    def test_detect_git(self, tmp_path):
        """Test git repo detection."""
        (tmp_path / ".git").mkdir()
        make_project(tmp_path, {
            "main.py": "pass",
        })
        analyzer = ProjectAnalyzer(str(tmp_path))
        info = analyzer.analyze()

        assert info.has_git

    def test_detect_license(self, tmp_path):
        """Test license detection."""
        make_project(tmp_path, {
            "LICENSE": "MIT License\nCopyright (c) 2024\n",
            "main.py": "pass",
        })
        analyzer = ProjectAnalyzer(str(tmp_path))
        info = analyzer.analyze()

        assert info.license_type == "MIT"

    def test_detect_django(self, tmp_path):
        """Test Django framework detection."""
        make_project(tmp_path, {
            "manage.py": "from django.core.management import execute_from_command_line",
            "requirements.txt": "django>=4.0\n",
            "main.py": "pass",
        })
        analyzer = ProjectAnalyzer(str(tmp_path))
        info = analyzer.analyze()

        assert "Django" in info.frameworks

    def test_detect_rust(self, tmp_path):
        """Test Rust project detection."""
        make_project(tmp_path, {
            "Cargo.toml": '[package]\nname = "myrust"\n',
            "main.rs": 'fn main() { println!("Hello"); }',
        })
        analyzer = ProjectAnalyzer(str(tmp_path))
        info = analyzer.analyze()

        assert info.name == "myrust"
        assert info.language == "Rust"

    def test_ignore_hidden_dirs(self, tmp_path):
        """Test that node_modules, __pycache__ etc are ignored."""
        make_project(tmp_path, {
            "main.py": "# real file",
            "node_modules/fake.js": "this should be ignored",
            "__pycache__/cached.pyc": "also ignored",
        })
        analyzer = ProjectAnalyzer(str(tmp_path))
        info = analyzer.analyze()

        assert info.language == "Python"
        # No JavaScript detected since node_modules is ignored
        assert "JavaScript" not in info.languages

    def test_modular_structure_detection(self, tmp_path):
        """Test modular architecture pattern detection."""
        make_project(tmp_path, {
            "src/main.py": "pass",
            "main.py": "pass",
        })
        analyzer = ProjectAnalyzer(str(tmp_path))
        info = analyzer.analyze()

        assert any("Modular" in p for p in info.patterns)

    def test_mvc_pattern_detection(self, tmp_path):
        """Test MVC architecture pattern detection."""
        make_project(tmp_path, {
            "controllers/main.py": "pass",
            "views/index.html": "<html></html>",
            "main.py": "pass",
        })
        analyzer = ProjectAnalyzer(str(tmp_path))
        info = analyzer.analyze()

        assert any("MVC" in p for p in info.patterns)

    def test_type_hints_detection(self, tmp_path):
        """Test Python type hints convention detection."""
        make_project(tmp_path, {
            "main.py": 'def hello(name: str) -> str:\n    return name',
        })
        analyzer = ProjectAnalyzer(str(tmp_path))
        info = analyzer.analyze()

        assert any("type hints" in c for c in info.conventions)

    def test_fallback_to_dir_name(self, tmp_path):
        """Test that project name falls back to directory name."""
        make_project(tmp_path, {
            "main.py": "pass",
        })
        analyzer = ProjectAnalyzer(str(tmp_path))
        info = analyzer.analyze()

        assert info.name == tmp_path.name


class TestConfigGenerator:
    """Tests for ConfigGenerator."""

    def _make_info(self, **kwargs):
        """Create a ProjectInfo with defaults overridden."""
        info = ProjectInfo(
            name="test-project",
            language="Python",
            package_manager="pip/uv/poetry",
            frameworks=["FastAPI"],
            build_tools=["uvicorn"],
            test_frameworks=["pytest"],
            has_git=True,
            has_docker=False,
            has_ci=True,
            ci_type="GitHub Actions",
            file_count=15,
            total_lines=500,
            patterns=["Modular structure (src)"],
            conventions=["Python with type hints"],
            tech_stack=["Python", "FastAPI", "uvicorn", "pytest"],
            key_files=["pyproject.toml", "README.md"],
            entry_points=["main.py (Python)"],
        )
        for k, v in kwargs.items():
            setattr(info, k, v)
        return info

    def test_generate_claude_md(self, tmp_path):
        """Test .claude.md generation."""
        info = self._make_info()
        gen = ConfigGenerator(info, tmp_path)
        output = gen.generate_claude_md()

        assert "# Project Overview" in output
        assert "**Project:** test-project" in output
        assert "FastAPI" in output
        assert "## Development Commands" in output
        assert "pytest" in output

    def test_generate_cursor_rules(self, tmp_path):
        """Test .cursorrules generation."""
        info = self._make_info()
        gen = ConfigGenerator(info, tmp_path)
        output = gen.generate_cursor_rules()

        assert "language: Python" in output
        assert "## Code Style" in output
        assert "## Safety Rules" in output
        assert "Never expose secrets" in output

    def test_generate_all_formats(self, tmp_path):
        """Test generating all formats at once."""
        info = self._make_info()
        gen = ConfigGenerator(info, tmp_path)
        configs = gen.generate_all()

        assert ".claude.md" in configs
        assert ".cursorrules" in configs
        assert ".windsurfrules" in configs
        assert all(len(v) > 100 for v in configs.values())

    def test_generate_specific_format(self, tmp_path):
        """Test generating only a specific format."""
        info = self._make_info()
        gen = ConfigGenerator(info, tmp_path)
        configs = gen.generate_all(formats=["claude"])

        assert list(configs.keys()) == [".claude.md"]

    def test_generate_with_docker(self, tmp_path):
        """Test Docker section in generated output."""
        info = self._make_info(has_docker=True)
        gen = ConfigGenerator(info, tmp_path)
        output = gen.generate_claude_md()

        assert "## Docker" in output
        assert "docker build" in output

    def test_generate_with_ci(self, tmp_path):
        """Test CI/CD section in generated output."""
        info = self._make_info(has_ci=True, ci_type="GitHub Actions")
        gen = ConfigGenerator(info, tmp_path)
        output = gen.generate_claude_md()

        assert "GitHub Actions" in output

    def test_generate_with_license(self, tmp_path):
        """Test license section in generated output."""
        info = self._make_info(license_type="MIT")
        gen = ConfigGenerator(info, tmp_path)
        output = gen.generate_claude_md()

        assert "MIT" in output

    def test_rust_project_generation(self, tmp_path):
        """Test generation for Rust projects."""
        info = self._make_info(
            language="Rust",
            package_manager="cargo",
            tech_stack=["Rust"],
        )
        gen = ConfigGenerator(info, tmp_path)
        output = gen.generate_claude_md()

        assert "cargo build" in output
        assert "cargo test" in output

    def test_node_js_generation(self, tmp_path):
        """Test generation for Node.js projects."""
        info = self._make_info(
            language="JavaScript",
            package_manager="npm/yarn/pnpm",
            test_frameworks=["Jest"],
            tech_stack=["JavaScript", "Jest"],
        )
        gen = ConfigGenerator(info, tmp_path)
        output = gen.generate_claude_md()

        assert "npm install" in output
        assert "npm test" in output


class TestEdgeCases:
    """Tests for edge cases."""

    def test_empty_project(self, tmp_path):
        """Test handling of empty project directory."""
        analyzer = ProjectAnalyzer(str(tmp_path))
        info = analyzer.analyze()

        assert info.name == tmp_path.name
        assert info.language == ""
        assert info.file_count == 0

    def test_nonexistent_path(self, tmp_path):
        """Test error handling for nonexistent paths."""
        analyzer = ProjectAnalyzer(str(tmp_path / "nonexistent"))
        info = analyzer.analyze()

        # Should not crash, just return minimal info
        assert info.name == "nonexistent"

    def test_unicode_file_content(self, tmp_path):
        """Test handling of unicode content."""
        make_project(tmp_path, {
            "main.py": "# Projekt z unicode: ąężźć\nprint('Hej! 🚀')",
        })
        analyzer = ProjectAnalyzer(str(tmp_path))
        info = analyzer.analyze()

        assert info.language == "Python"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])