import os
import sys
import json
from pathlib import Path

AIOS_ROOT = Path("E:/anti/aios")
sys.path.insert(0, str(AIOS_ROOT / "databases"))

from db import get_connection, log_audit

class SaaSFactory:
    def __init__(self, root_dir: str = "E:/anti/aios/projects/scaffolded"):
        self.root_dir = Path(root_dir)
        self.root_dir.mkdir(parents=True, exist_ok=True)

    def scaffold_project(self, name: str, stack: str, features: list) -> str:
        project_path = self.root_dir / name
        project_path.mkdir(parents=True, exist_ok=True)

        if stack == 'nextjs-fastapi':
            self._scaffold_nextjs_fastapi(project_path)
        elif stack == 'nextjs-flask':
            self._scaffold_nextjs_flask(project_path)
        elif stack == 'static-api':
            self._scaffold_static_api(project_path)
        elif stack == 'python-cli':
            self._scaffold_python_cli(project_path)
        else:
            raise ValueError(f"Unknown stack: {stack}")

        # Common files
        with open(project_path / ".gitignore", "w") as f:
            f.write("node_modules/\n__pycache__/\n.env\n*.pyc\n")
        
        with open(project_path / "README.md", "w") as f:
            f.write(f"# {name}\n\nStack: {stack}\n\n## Setup\nFollow the instructions for {stack}.")
            
        with open(project_path / ".env.example", "w") as f:
            f.write("DB_URL=sqlite:///data.db\nPORT=8000\n")
            
        with open(project_path / "Makefile", "w") as f:
            f.write("dev:\n\techo 'Running dev'\ntest:\n\techo 'Running tests'\nbuild:\n\techo 'Building'\ndeploy:\n\techo 'Deploying'\n")

        # Features
        if 'auth' in features:
            (project_path / "auth_stub.py").write_text("# JWT middleware stub\n")
        if 'db' in features:
            (project_path / "db_setup.py").write_text("# SQLite schema + migration script\n")
        if 'stripe' in features:
            (project_path / "stripe_stub.py").write_text("# Payment integration stub\n")
        if 'analytics' in features:
            (project_path / "analytics_stub.py").write_text("# Event tracking stub\n")

        # Record in DB
        with get_connection() as con:
            con.execute(
                "INSERT INTO saas_projects (name, stack, features, path) VALUES (?, ?, ?, ?)",
                (name, stack, json.dumps(features), str(project_path))
            )
            con.commit()
            
        log_audit("SaaSFactory", "SCAFFOLD", "PROJECT", f"Scaffolded {name} with stack {stack}", "INFO")

        return str(project_path)

    def _scaffold_nextjs_fastapi(self, project_path: Path):
        frontend = project_path / "frontend"
        backend = project_path / "backend"
        frontend.mkdir(exist_ok=True)
        backend.mkdir(exist_ok=True)
        (frontend / "package.json").write_text('{"name": "frontend"}')
        (frontend / "pages").mkdir(exist_ok=True)
        (frontend / "pages/index.tsx").write_text("export default function Home() { return <div>Home</div>; }")
        (frontend / ".env.local").write_text("NEXT_PUBLIC_API_URL=http://localhost:8000")
        (backend / "main.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n")
        (backend / "requirements.txt").write_text("fastapi\nuvicorn")
        (backend / ".env").write_text("DEBUG=1")
        (project_path / "docker-compose.yml").write_text("version: '3'\nservices:\n  api:\n    build: ./backend\n")
        
    def _scaffold_nextjs_flask(self, project_path: Path):
        frontend = project_path / "frontend"
        backend = project_path / "backend"
        frontend.mkdir(exist_ok=True)
        backend.mkdir(exist_ok=True)
        (frontend / "package.json").write_text('{"name": "frontend"}')
        (frontend / "pages").mkdir(exist_ok=True)
        (frontend / "pages/index.tsx").write_text("export default function Home() { return <div>Home</div>; }")
        (frontend / ".env.local").write_text("NEXT_PUBLIC_API_URL=http://localhost:5000")
        (backend / "main.py").write_text("from flask import Flask\napp = Flask(__name__)\n")
        (backend / "requirements.txt").write_text("flask")
        (backend / ".env").write_text("DEBUG=1")
        (project_path / "docker-compose.yml").write_text("version: '3'\nservices:\n  api:\n    build: ./backend\n")

    def _scaffold_static_api(self, project_path: Path):
        static = project_path / "static"
        api = project_path / "api"
        static.mkdir(exist_ok=True)
        api.mkdir(exist_ok=True)
        (static / "index.html").write_text("<html><body>Hello</body></html>")
        (api / "app.py").write_text("print('API stub')")

    def _scaffold_python_cli(self, project_path: Path):
        src = project_path / "src"
        tests = project_path / "tests"
        src.mkdir(exist_ok=True)
        tests.mkdir(exist_ok=True)
        (project_path / "setup.py").write_text("from setuptools import setup\nsetup(name='cli')\n")
        (src / "__init__.py").write_text("")
        (tests / "test_main.py").write_text("def test_dummy(): pass\n")

    def list_projects(self) -> list:
        with get_connection() as con:
            cur = con.execute("SELECT * FROM saas_projects")
            return [dict(row) for row in cur.fetchall()]
