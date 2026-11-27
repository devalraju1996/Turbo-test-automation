
import os
import subprocess
import sys
import tempfile
import threading
import xml.etree.ElementTree as ET

from datetime import datetime, timezone
from uuid import uuid4
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


app = FastAPI(
    title="Turbo Test Automation Platform",
    description="Practice API for managing automated test executions",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://localhost:80",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEST_CASES = [
    {
        "id": "TC-001",
        "name": "Dashboard loads",
        "suite": "Dashboard",
    },
]

EXECUTIONS = []
EXECUTION_LOCK = threading.Lock()

PROJECT_DIR = Path("/app")
TEST_PATH = (
    PROJECT_DIR / "automation" / "tests" / "test_dashboard.py"
)


class ExecutionRequest(BaseModel):
    suite: str = Field(default="Dashboard", min_length=1)


def run_dashboard_tests(execution_id: str):
    with EXECUTION_LOCK:
        execution = next(
            (item for item in EXECUTIONS if item["id"] == execution_id),
            None,
        )
        if execution is None:
            return

        execution["status"] = "running"

    try:
        if not TEST_PATH.exists():
            raise FileNotFoundError(f"Test file not found: {TEST_PATH}")

        with tempfile.NamedTemporaryFile(
            suffix=".xml", delete=False
        ) as report:
            report_path = report.name

        environment = os.environ.copy()
        environment["PYTHONPATH"] = (
            f"{PROJECT_DIR / 'automation'}"
            + os.pathsep
            + environment.get("PYTHONPATH", "")
        )

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                str(TEST_PATH) + "::test_dashboard_loads",
                f"--junitxml={report_path}",
            ],
            cwd=str(PROJECT_DIR),
            env=environment,
            capture_output=True,
            text=True,
            timeout=300,
        )

        passed = 0
        failed = 0

        try:
            root = ET.parse(report_path).getroot()
            passed = int(root.attrib.get("tests", 0)) - int(
                root.attrib.get("failures", 0)
            ) - int(root.attrib.get("errors", 0)) - int(
                root.attrib.get("skipped", 0)
            )
            failed = int(root.attrib.get("failures", 0)) + int(
                root.attrib.get("errors", 0)
            )
        finally:
            Path(report_path).unlink(missing_ok=True)

        with EXECUTION_LOCK:
            execution = next(
                item for item in EXECUTIONS
                if item["id"] == execution_id
            )

            execution["passed"] = passed
            execution["failed"] = failed
            execution["total"] = passed + failed
            execution["status"] = (
                "completed" if result.returncode == 0 else "failed"
            )
            execution["output"] = (
                result.stdout[-5000:] + result.stderr[-5000:]
            )
            execution["completed_at"] = datetime.now(
                timezone.utc
            ).isoformat()

    except Exception as exc:
        with EXECUTION_LOCK:
            execution = next(
                (item for item in EXECUTIONS if item["id"] == execution_id),
                None,
            )
            if execution:
                execution["status"] = "failed"
                execution["error"] = str(exc)
                execution["completed_at"] = datetime.now(
                    timezone.utc
                ).isoformat()


@app.get("/")
def home():
    return {"message": "Welcome to Turbo Test Automation Platform"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": "turbo-test-automation",
    }


@app.get("/api/tests")
def list_tests():
    return {"items": TEST_CASES, "total": len(TEST_CASES)}


@app.get("/api/executions")
def list_executions():
    with EXECUTION_LOCK:
        return {
            "items": [dict(item) for item in EXECUTIONS],
            "total": len(EXECUTIONS),
        }


@app.post("/api/executions", status_code=201)
def create_execution(
    request: ExecutionRequest,
    background_tasks: BackgroundTasks,
):
    if request.suite != "Dashboard":
        raise HTTPException(
            status_code=400,
            detail="Only the Dashboard suite is currently implemented",
        )

    execution = {
        "id": str(uuid4()),
        "suite": request.suite,
        "status": "queued",
        "total": 1,
        "passed": 0,
        "failed": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    with EXECUTION_LOCK:
        EXECUTIONS.insert(0, execution)

    background_tasks.add_task(
        run_dashboard_tests,
        execution["id"],
    )

    return execution
