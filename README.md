# Turbo Test Automation Platform (Practice Project)

A learning project combining a React dashboard, FastAPI API, Pytest, Playwright, Jenkins, Docker Compose, and a starter Kubernetes/Kustomize layout.

## Prerequisites
- Windows 10/11
- Python 3.11+
- Node.js LTS
- Git
- Docker Desktop (for Compose)
- Jenkins LTS (already installed)

## 1. Backend (PowerShell)
```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Open http://127.0.0.1:8000/docs

In another terminal:
```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -v
```

## 2. Frontend (PowerShell)
```powershell
cd frontend
npm install
npm run dev
```
Open http://localhost:5173

## 3. Browser automation
With the backend and frontend running:
```powershell
cd automation
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe -m pytest -v
```

## 4. Jenkins
Configure a Jenkins Pipeline job using **Pipeline script from SCM**, your Git repository, branch `*/main`, and script path `Jenkinsfile`.
The Jenkins agent must have Git, Python 3.11, Node.js, and (for image builds) Docker available to its Windows service account or agent.

The GitHub webhook URL must point to a publicly reachable HTTPS Jenkins endpoint ending in `/github-webhook/`. `localhost` is not reachable by GitHub. Do not expose Jenkins directly to the public internet without proper access controls and HTTPS.

## 5. Docker Compose
```powershell
docker compose up --build
```
- Frontend: http://localhost:5173
- Backend: http://localhost:8000/docs
- MongoDB: localhost:27017

## Important scope notes
- This is a practice implementation, not your employer's internal Turbo repository.
- The README material describes a Jenkins/Jules build flow and a separate Spinnaker deployment flow. This starter Jenkinsfile does not connect to private Jules, Artifactory, ECR, AWS accounts, or Spinnaker.
- Kubernetes files are a starter example. Review image names, namespaces, secrets, ingress, and cluster policies before deploying anywhere.
- Do not commit credentials, tokens, kubeconfigs, or `.env` files.
