#!/usr/bin/env python3
"""Helper: Create realistic test projects for ai-config-gen validation."""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/test_projects"


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def create_fastapi_project():
    base = os.path.join(BASE, "python_fastapi")
    write(os.path.join(base, "pyproject.toml"), """[project]
name = "fastapi-service"
version = "1.0.0"
requires-python = ">=3.12"
dependencies = ["fastapi>=0.115", "uvicorn", "sqlalchemy", "alembic", "httpx", "pytest-asyncio"]
""")
    write(os.path.join(base, "README.md"), "# FastAPI Service\n\nREST API built with FastAPI + SQLAlchemy\n")
    write(os.path.join(base, "app/__init__.py"), "from fastapi import FastAPI\napp = FastAPI(title=\"My API\", version=\"1.0.0\")\n")
    write(os.path.join(base, "app/main.py"), """from app import app
from app.routers import users

app.include_router(users.router)

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
""")
    write(os.path.join(base, "app/routers/__init__.py"), "")
    write(os.path.join(base, "app/routers/users.py", ), """from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter(prefix="/users")

@router.get("/", response_model=List[dict])
async def get_users() -> List[dict]:
    return [{"id": 1, "name": "Alice"}]

@router.get("/{user_id}")
async def get_user(user_id: int) -> dict:
    if user_id != 1:
        raise HTTPException(status_code=404)
    return {"id": 1, "name": "Alice"}

@router.post("/")
async def create_user(name: str) -> dict:
    return {"id": 2, "name": name}
""")
    write(os.path.join(base, "tests/__init__.py"), "")
    write(os.path.join(base, "tests/test_users.py"), """import pytest
from httpx import AsyncClient
from app import app

@pytest.mark.anyio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as client:
        resp = await client.get("/health")
        assert resp.status_code == 200
""")
    write(os.path.join(base, ".github/workflows/ci.yml"), """name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest
""")
    write(os.path.join(base, "Dockerfile"), "FROM python:3.12-slim\nCMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\"]\n")
    write(os.path.join(base, "LICENSE"), "MIT License\nCopyright (c) 2025\n")
    print("  [OK] python_fastapi")


def create_node_react_project():
    base = os.path.join(BASE, "node_react")
    write(os.path.join(base, "package.json"), json.dumps({
        "name": "my-react-app",
        "version": "1.0.0",
        "dependencies": {"react": "^18.2.0", "react-dom": "^18.2.0"},
        "devDependencies": {"typescript": "^5.3.0", "tailwindcss": "^3.4.0"}
    }, indent=2))
    write(os.path.join(base, "tsconfig.json"), json.dumps({
        "compilerOptions": {"target": "ES2020", "jsx": "react-jsx", "strict": True}
    }, indent=2))
    write(os.path.join(base, "src/App.tsx"), """import React from 'react';

export default function App() {
  return <div>Hello World</div>;
}
""")
    write(os.path.join(base, "src/components/Button.tsx"), """export function Button({ children, onClick }: { children: React.ReactNode; onClick: () => void }) {
  return <button onClick={onClick}>{children}</button>;
}
""")
    write(os.path.join(base, ".gitignore"), "node_modules/\ndist/\n")
    write(os.path.join(base, "README.md"), "# My React App\n\nBuilt with React + TypeScript + Tailwind\n")
    print("  [OK] node_react")


def create_rust_lib():
    base = os.path.join(BASE, "rust_lib")
    write(os.path.join(base, "Cargo.toml"), """[package]
name = "my-lib"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
""")
    write(os.path.join(base, "src/lib.rs"), """use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
pub struct Config {
    pub host: String,
    pub port: u16,
}

impl Config {
    pub fn new(host: &str, port: u16) -> Self {
        Self { host: host.to_string(), port }
    }
}

#[tokio::test]
async fn test_config() {
    let cfg = Config::new("localhost", 8080);
    assert_eq!(cfg.port, 8080);
}
""")
    write(os.path.join(base, "LICENSE"), "Apache License\nVersion 2.0\n")
    print("  [OK] rust_lib")


def create_django_project():
    base = os.path.join(BASE, "django_app")
    write(os.path.join(base, "manage.py"), """#!/usr/bin/env python
import os
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
execute_from_command_line(sys.argv)
""")
    write(os.path.join(base, "requirements.txt"), "django>=4.2\ndjangorestframework\npsycopg2-binary\n")
    write(os.path.join(base, "myproject/settings.py"), """from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
INSTALLED_APPS = ['django.contrib.admin', 'myapp']
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
""")
    write(os.path.join(base, "myapp/views.py"), """from django.http import JsonResponse

def index(request):
    return JsonResponse({"message": "Hello Django"})
""")
    write(os.path.join(base, "myapp/models.py"), """from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
""")
    write(os.path.join(base, "tests/test_views.py"), """from django.test import TestCase, Client
from django.urls import reverse

class IndexTest(TestCase):
    def test_index(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
""")
    write(os.path.join(base, "Dockerfile"), "FROM python:3.12\nRUN pip install -r requirements.txt\nCMD [\"gunicorn\", \"myproject.wsgi:application\"]\n")
    write(os.path.join(base, "README.md"), "# Django App\n\nBlog application built with Django + DRF\n")
    print("  [OK] django_app")


if __name__ == "__main__":
    print("Creating test projects...")
    create_fastapi_project()
    create_node_react_project()
    create_rust_lib()
    create_django_project()
    print("Done!")