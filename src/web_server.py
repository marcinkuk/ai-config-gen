#!/usr/bin/env python3
"""
FastAPI web server for ai-config-gen.

Endpoints:
    GET  /health       – Health check
    POST /analyze      – Upload a .tar.gz project archive and get JSON analysis
    POST /generate      – Upload a .tar.gz project archive and get generated markdown
    GET  /formats      – List supported config formats

Run:
    uvicorn src.web_server:app --host 0.0.0.0 --port 8000
"""

import shutil
import tarfile
import tempfile
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.responses import PlainTextResponse
from starlette.requests import Request

from ai_config_gen import ConfigGenerator, ProjectAnalyzer

SUPPORTED_FORMATS = ["claude", "cursor", "windsurf"]
RATE_LIMIT = 10  # max requests per window
RATE_WINDOW = 60  # seconds


# ---------------------------------------------------------------------------
# Rate limiting (simple in-memory dict keyed by IP)
# ---------------------------------------------------------------------------
_rate_store: Dict[str, list] = {}


def _check_rate_limit(client_ip: str) -> None:
    """Raise 429 if *client_ip* exceeded the per-minute quota."""
    now = time.time()
    timestamps = _rate_store.setdefault(client_ip, [])
    # Purge stale entries
    _rate_store[client_ip] = [t for t in timestamps if now - t < RATE_WINDOW]
    if len(_rate_store[client_ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Max 10 requests per minute.",
        )
    _rate_store[client_ip].append(now)


# ---------------------------------------------------------------------------
# Temp-dir lifecycle helper
# ---------------------------------------------------------------------------
def _extract_tar_gz(file_content: bytes, temp_dir: Path) -> Path:
    """Extract a tar.gz archive into *temp_dir*. Returns the top-level project dir."""
    with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tf:
        tf.write(file_content)
        tf_path = tf.name

    try:
        with tarfile.open(tf_path, "r:gz") as tar:
            # Validate: must contain at least one member and not be a directory archive
            members = tar.getmembers()
            if not members:
                raise HTTPException(status_code=400, detail="Archive is empty.")
            tar.extractall(path=temp_dir)  # noqa: S202 – controlled env
    except tarfile.TarError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid archive: {exc}",
        ) from exc
    finally:
        Path(tf_path).unlink(missing_ok=True)

    # Return the first extracted directory (or temp_dir itself if flat files)
    extracted = list(temp_dir.iterdir())
    if len(extracted) == 1 and extracted[0].is_dir():
        return extracted[0]
    return temp_dir


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Could load / warm-up resources here; currently a no-op.
    yield


app = FastAPI(title="ai-config-gen", version="0.1.0", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/formats")
async def formats():
    return {"formats": SUPPORTED_FORMATS}


@app.post("/analyze")
async def analyze(request: Request, file: UploadFile = ...):
    """Accept a .tar.gz project archive and return JSON analysis."""
    _check_rate_limit(request.client.host)

    if not file.filename or not file.filename.endswith(".tar.gz"):
        raise HTTPException(status_code=400, detail="Upload must be a .tar.gz file.")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    with tempfile.TemporaryDirectory() as tmp:
        project_dir = _extract_tar_gz(content, Path(tmp))

        try:
            analyzer = ProjectAnalyzer(str(project_dir))
            info = analyzer.analyze()
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {exc}",
            ) from exc

    return info


@app.post("/generate", response_class=PlainTextResponse)
async def generate(request: Request, file: UploadFile = ..., format: str = Form(None)):
    """Accept a .tar.gz project archive and return generated markdown content."""
    _check_rate_limit(request.client.host)

    if not file.filename or not file.filename.endswith(".tar.gz"):
        raise HTTPException(status_code=400, detail="Upload must be a .tar.gz file.")

    if format not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid format '{format}'. Supported: {', '.join(SUPPORTED_FORMATS)}",
        )

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    with tempfile.TemporaryDirectory() as tmp:
        project_dir = _extract_tar_gz(content, Path(tmp))

        try:
            analyzer = ProjectAnalyzer(str(project_dir))
            info = analyzer.analyze()

            generator = ConfigGenerator(info, str(project_dir))
            gen_func = {
                "claude": generator.generate_claude_md,
                "cursor": generator.generate_cursor_rules,
                "windsurf": generator.generate_windsurf_rules,
            }[format]
            markdown = gen_func()
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Generation failed: {exc}",
            ) from exc

    return markdown


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------
def main():
    """Run the server via: python -m src.web_server  (or similar)."""
    import uvicorn

    uvicorn.run("src.web_server:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()