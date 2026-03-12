# DevOps Lab Guide  
# Secrets, Artifacts & Running Real Tests in CI

This lab introduces **secure data handling, artifact management, caching, and running real tests in CI pipelines**.

In real DevOps environments, pipelines don't just run simple commands — they:

- Use **secure credentials**
- Produce **build artifacts**
- Share files between pipeline stages
- **Run automated tests**
- **Cache dependencies** to speed up builds

This lab demonstrates how to implement these capabilities using **GitHub Actions**.

---

# Learning Objectives

After completing this lab, you will understand:

- How **GitHub Secrets** securely store sensitive information
- How to use secrets **without exposing them in logs**
- How to **generate and upload artifacts**
- How to **share artifacts between jobs**
- How to **run real scripts/tests in CI**
- How **dependency caching** speeds up pipelines

---

# Repository Structure

Example structure for your repo:

```
github-actions-practice
│
├── .github/workflows/
│   ├── secret-test.yml
│   ├── secret-env.yml
│   ├── upload-artifact.yml
│   ├── artifact-sharing.yml
│   ├── python-ci-test.yml
│   └── cache-demo.yml
│
├── test_script.py
├── requirements.txt
│
└── docs/
    └── day-44-secrets-artifacts.md
```

---

# DevOps Concept 1 — GitHub Secrets

CI pipelines often require **sensitive values** such as:

- API keys
- Docker credentials
- Cloud tokens
- Database passwords

Hardcoding these values in code is **extremely dangerous**.

GitHub provides **encrypted secrets storage**.

Secrets are:

- Encrypted at rest
- Only accessible inside workflows
- Automatically **masked in logs**

Example usage:

```
${{ secrets.SECRET_NAME }}
```

GitHub automatically replaces secret values with:

```
***
```

This prevents credential leaks.

---

# DevOps Concept 2 — Environment Variables

Secrets should be injected as **environment variables**, allowing scripts to use them without exposing the values.

Example:

```
env:
  TOKEN: ${{ secrets.API_TOKEN }}
```

Your scripts can then access it as:

```
$TOKEN
```

This avoids hardcoding credentials.

---

# DevOps Concept 3 — Artifacts

Artifacts are **files generated during a pipeline run**.

Examples:

- Build packages
- Test reports
- Log files
- Compiled binaries

Artifacts allow:

- Downloading files after CI finishes
- Sharing files between pipeline stages

GitHub provides:

```
actions/upload-artifact
actions/download-artifact
```

Artifacts are stored temporarily in GitHub's storage.

---

# DevOps Concept 4 — Running Tests in CI

A CI pipeline should **run tests automatically** whenever code is pushed.

Typical pipeline flow:

```
Checkout code
Install dependencies
Run tests
Fail pipeline if tests fail
```

If a test script returns a **non-zero exit code**, the pipeline fails.

This ensures broken code **never reaches production**.

---

# DevOps Concept 5 — Dependency Caching

Installing dependencies repeatedly slows pipelines.

Caching allows workflows to **reuse previous dependency downloads**.

Example:

- Python packages
- Node modules
- Maven dependencies

Benefits:

- Faster builds
- Less network usage
- Reduced CI time

GitHub caching uses:

```
actions/cache
```

---

# Task 1 — GitHub Secrets

## Goal

Store and safely access a secret value.

---

## Step 1 — Create a Secret

Navigate to:

```
Repository → Settings → Secrets and Variables → Actions
```

Create secret:

```
MY_SECRET_MESSAGE
```

---

## Step 2 — Create Workflow

File:

```
.github/workflows/secret-test.yml
```

```
[name: Secret Test

on:
  workflow_dispatch:

jobs:
  check_secret:
    runs-on: ubuntu-latest
    steps:
      - name: Printe secret key existance
        run: 'echo "The secret is set: true"'
        
        
      - name: Printing secret key directly
        run: 'echo "Secret value: ${{ secrets.MY_SECRET_MESSAGE }}"']
```

---

## Step 3 — Run Workflow

Go to:

```
Actions → Secret Test → Run workflow
```

---

## Verification

Observe the logs.

Expected behavior:

```
Secret value: ***
```

GitHub automatically **masks secret values**.

---

## Screenshot Placeholder

```
[Insert Screenshot — Secret masked in logs]
```

---

## Mentor Notes

Never print secrets in CI logs because:

- Logs are visible to anyone with repo access
- Secrets could leak to attackers
- Compromised credentials can lead to system breaches

Always **mask and securely reference secrets**.

---

# Task 2 — Use Secrets as Environment Variables

## Goal

Use secrets **without exposing them**.

---

## Create Workflow

File:

```
.github/workflows/secret-env.yml
```

```
[name: Secret Environment Variable

on:
  workflow_dispatch

jobs:
  docker-login:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Use Secrets as environment varaibles
        env:
          DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
          DOCKER_TOKEN: ${{ secrets.DOCKER_TOKEN }}
        run: |
          echo "Logging in with Docker username: $DOCKER_USERNAME"
          echo "Token length: ${#Docker_TOKEN}"]
```

---

## Verification

Pipeline logs should show:

```
Logging in with Docker username: yourusername
Token length: 32
```

Actual token value **will not appear**.

---

## Screenshot Placeholder

```
[Insert Screenshot — Secret environment variables used safely]
```

---

# Task 3 — Upload Artifacts

## Goal

Generate and upload a file from the pipeline.

---

## Create Workflow

File:

```
.github/workflows/upload-artifact.yml
```

```
[name: Upload artifact demo

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: checkout code
        uses: actions/checkout@v4

      - name: Generate Tesr report
        run: |
          echo "Test Completed successfully..." > test-report.txt
          echo "Timestamp: $(date)" >> test-report.txt

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: test-report
          path: test-report.txt]
```

---

## Verification

After workflow finishes:

```
Actions → Workflow Run → Artifacts
```

Download:

```
test-report.zip
```

---

## Screenshot Placeholder

```
[Insert Screenshot — Artifact available for download]
```

---

# Task 4 — Download Artifacts Between Jobs

## Goal

Share files between jobs.

---

## Create Workflow

File:

```
.github/workflows/artifact-sharing.yml
```

```
[name: Upload & sharing artifact demo

on:
  workflow_dispatch:

jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
      - name: checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate Tesr report
        run: |
          echo "Hello From Job1!!" > output.txt
          

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: shared-output
          path: output.txt

  job2:
    runs-on: ubuntu-latest
    needs: job1
    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: shared-output
      
      - name: Print file contents
        run: cat output.txt]
```

---

## Verification

Job2 logs should display:

```
Hello From Job1!!
```

---

## Screenshot Placeholder

```
[Insert Screenshot — Artifact shared between jobs]
```

---

## Mentor Notes

Artifacts are used in real pipelines for:

- Passing build outputs
- Test reports
- Docker build layers
- Deployment packages

---

# Task 5 — Run Real Tests in CI

## Goal

Run a script in CI and fail pipeline if errors occur.

---

## Example Script

Create:

```
test_script.py
```

```
[print("Running CI test...")

x = 5
y = 10

assert x + y == 15

print("Test Passed")]
```

---

## requirements.txt

```
[]
```

---

## Workflow

File:

```
.github/workflows/python-ci-test.yml
```

```
[name: Python CI test

on:
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run the test
        run: python test_script.py]
```

---

## Verification

If the test passes:

```
Test Passed
```

Pipeline status:

```
✔ Success
```

---

## Break the Script

Modify:

```
assert x + y == 20
```

Run workflow again.

Expected result:

```
AssertionError
```

Pipeline becomes **red**.

---

## Screenshot Placeholder

```
[Insert Screenshot — CI failure]
```

```
[Insert Screenshot — CI success after fixing]
```

---

# Task 6 — Dependency Caching

## Goal

Speed up dependency installation.

---

## Workflow

File:

```
.github/workflows/cache-demo.yml
```

```
[name: Dependency Cache Demo

on:
  workflow_dispatch:

jobs:
  cache-demo:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

      - name: Install dependencies
        run: pip install -r requirements.txt]
```

---

## Verification

First run:

```
Cache not found
```

Second run:

```
Cache restored successfully
```

Pipeline becomes **faster**.

---

## Screenshot Placeholder

```
[Insert Screenshot — Cache hit in logs]
```

---

# What I Learned

Key DevOps lessons from this lab:

### Secrets Management

- Secrets should never be hardcoded
- GitHub masks secret values in logs
- Secrets must be accessed securely

### Artifacts

Artifacts allow pipelines to:

- Store build outputs
- Share files between jobs
- Provide downloadable outputs

### Running Tests in CI

Automated testing ensures:

- Broken code is caught early
- CI pipelines enforce quality checks

### Dependency Caching

Caching reduces pipeline execution time by reusing downloaded dependencies.

---

# Final Result

After completing this lab you now have:

- Secure secrets handling
- Artifact upload and sharing
- Real test execution in CI
- Dependency caching
- Production-style CI pipeline behavior

These are **core DevOps skills used in real-world CI/CD systems**.

---

End of Lab
