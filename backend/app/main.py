from datetime import datetime, timezone
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Turbo Test Automation Platform",
    description="Practice API for managing automated test executions",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# In-memory storage keeps the first version easy to run.
# A later learning phase can replace this with MongoDB persistence.
TEST_CASES = [
    {"id": "TC-001", "name": "Valid login", "suite": "Authentication"},
    {"id": "TC-002", "name": "Invalid login", "suite": "Authentication"},
]
EXECUTIONS = []


class ExecutionRequest(BaseModel):
    suite: str = Field(default="Authentication", min_length=1)


@app.get("/")
def home():
    return {"message": "Welcome to Turbo Test Automation Platform"}


@app.get("/health")
def health():
    return {"status": "healthy", "application": "turbo-test-automation"}


@app.get("/api/tests")
def list_tests():
    return {"items": TEST_CASES, "total": len(TEST_CASES)}


@app.get("/api/executions")
def list_executions():
    return {"items": EXECUTIONS, "total": len(EXECUTIONS)}


@app.post("/api/executions", status_code=201)
def create_execution(request: ExecutionRequest):
    matching = [case for case in TEST_CASES if case["suite"] == request.suite]
    if not matching:
        raise HTTPException(status_code=404, detail="Test suite not found")

    execution = {
        "id": str(uuid4()),
        "suite": request.suite,
        "status": "queued",
        "total": len(matching),
        "passed": 0,
        "failed": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    EXECUTIONS.insert(0, execution)
    return execution
