# OpsBeacon AI - Local Development Setup

This document guides you through setting up OpsBeacon AI for local development, formatting checks, and unit testing.

---

## 1. Prerequisites

Ensure you have the following installed:
* **Python 3.12** or higher.
* **Pip** (Python package installer).
* **Git** version control.

---

## 2. Setting Up Virtual Environment

Clone the repository and navigate into the workspace. Then create and activate a Python virtual environment:

### Windows (PowerShell/CMD):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

Install the requirements which include production libraries (`feedparser`, `boto3`, `requests`, `jinja2`) and development tools (`pytest`, `black`, `ruff`):

```bash
pip install -r requirements.txt
```

---

## 4. Local Environment Configuration

Copy the example environment variables file to create a local `.env` file:

```bash
cp .env.example .env
```

Open `.env` and fill in the values:
* Specify your AWS credentials and region (`AWS_REGION=us-east-1`).
* Configure the verified SES sender and recipient emails (`SENDER_EMAIL` and `RECIPIENT_EMAIL`).

---

## 5. Running Code Formatting & Linting

To maintain code quality and ensure the CI/CD checks pass, run formatting and linting tools:

### Run Code Formatting Check (Black)
```bash
black --check src tests
```
To automatically apply formatting updates, run without `--check`:
```bash
black src tests
```

### Run Static Analysis & Linting (Ruff)
```bash
ruff check src tests
```
To auto-fix safe errors, run with `--fix`:
```bash
ruff check src tests --fix
```

---

## 6. Running Unit Tests

Unit tests are written using `pytest` and mock AWS services so they can run offline without real AWS resources.

Run the tests using the following command:

```bash
pytest -v
```

To run with coverage (if coverage packages are installed):
```bash
pytest --cov=src tests/
```

---

## 7. Running the Script Locally

You can run the script locally to fetch feeds and print the resulting console operations. Note that to invoke Bedrock or SES, your local shell environment must have valid AWS credentials configured (e.g. via `aws configure` or environment variables `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`):

```bash
python -m src.app
```
This runs the orchestrator in debug/local mode.
