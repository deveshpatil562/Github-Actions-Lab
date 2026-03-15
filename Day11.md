# Advanced GitHub Actions Triggers  
## PR Events, Cron Schedules & Event-Driven Pipelines

Author: Devesh Patil  
Repository: https://github.com/deveshpatil562/Github-Actions-Lab  

---

# Introduction

Modern **CI/CD pipelines** are not only triggered by `push` events.  
Real-world DevOps pipelines react to **events happening in the software lifecycle** such as:

- Pull request lifecycle events
- Scheduled maintenance jobs
- File or branch changes
- Workflow completion
- External system triggers

GitHub Actions supports **dozens of triggers**, enabling powerful **event-driven automation pipelines**.

In this lab you will implement:

- Pull Request lifecycle automation
- Automated PR validation gates
- Scheduled cron jobs
- Smart path-based triggers
- Workflow chaining
- External system triggers

These patterns are heavily used in **enterprise DevOps pipelines**.

---

# Repository Structure

```
.github/workflows/
│
├── pr-lifecycle.yml
├── pr-checks.yml
├── scheduled-tasks.yml
├── smart-triggers.yml
├── tests.yml
├── deploy-after-tests.yml
└── external-trigger.yml

2026/day-47/
└── day-47-advanced-triggers.md
```

---

# Task 1 — Pull Request Lifecycle Events

## Concept

Pull requests go through multiple lifecycle stages:

| Event | Description |
|-----|-----|
| opened | PR created |
| synchronize | New commits pushed |
| reopened | PR reopened |
| closed | PR closed or merged |

GitHub exposes this through:

```
${{ github.event.action }}
```

Other useful metadata:

```
${{ github.event.pull_request.title }}
${{ github.event.pull_request.user.login }}
${{ github.event.pull_request.head.ref }}
${{ github.event.pull_request.base.ref }}
```

---

## Workflow File

`.github/workflows/pr-lifecycle.yml`

```
[name: PR Lifecycle Events

on:
  pull_request:
    types: [opened, synchronize, reopened, closed]

jobs:
  pr-events:
    runs-on: ubuntu-latest

    steps:
      - name: Print Event Type
        run: echo "Event type -> ${{ github.event.action }}"

      - name: Print PR Title
        run: echo "PR title -> ${{ github.event.pull_request.title }}"

      - name: Print PR Author
        run: echo "PR author -> ${{ github.event.pull_request.user.login }}"

      - name: Print Branch Info
        run: |
          echo "Source branch -> ${{ github.event.pull_request.head.ref }}"
          echo "Target branch -> ${{ github.event.pull_request.base.ref }}"

      - name: Run only if PR merged
        if: github.event.pull_request.merged == true
        run: echo "PR was merged successfully"]
```

---

## Testing

1. Create a new branch

```
[git checkout -b feature/pr-test]
```

2. Push branch

```
[git push origin feature/pr-test]
```

3. Create a pull request.

4. Push additional commits to trigger **synchronize**.

5. Merge PR.

---

## Verification

Go to repository:

```
Actions → PR Lifecycle Events
```

Expected runs:

- PR opened
- PR synchronized
- PR closed/merged

---

### Screenshot Placeholder

```
[ Screenshot: PR Lifecycle workflow triggered multiple times ]
```

---

## Mentor Insight

In real production pipelines:

- PR opened → run **code quality checks**
- PR synchronized → run **tests again**
- PR merged → trigger **deployment**

---

# Task 2 — PR Validation Workflow

## Concept

Before merging code into `main`, organizations enforce **PR gates**.

Typical checks include:

- File size validation
- Branch naming policy
- Mandatory PR descriptions

---

## Workflow File

`.github/workflows/pr-checks.yml`

```
[name: PR Validation Checks

on:
  pull_request:
    branches:
      - main

jobs:

  file-size-check:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Check file sizes
        run: |
          for file in $(git diff --name-only origin/main); do
            size=$(stat -c%s "$file")
            if [ $size -gt 1048576 ]; then
              echo "File $file is larger than 1MB"
              exit 1
            fi
          done

  branch-name-check:
    runs-on: ubuntu-latest

    steps:
      - name: Validate branch name
        run: |
          branch=${{ github.head_ref }}
          echo "Branch name -> $branch"

          if [[ ! "$branch" =~ ^(feature|fix|docs)/.* ]]; then
            echo "Invalid branch name"
            exit 1
          fi

  pr-body-check:
    runs-on: ubuntu-latest

    steps:
      - name: Check PR body
        run: |
          body="${{ github.event.pull_request.body }}"

          if [ -z "$body" ]; then
            echo "Warning: PR description is empty"
          else
            echo "PR description present"
          fi]
```

---

## Testing

Create branch with invalid name:

```
[git checkout -b randombranch]
```

Push and open PR.

---

## Verification

Expected result:

- Branch name check **fails**
- PR cannot be merged until checks pass

---

### Screenshot Placeholder

```
[ Screenshot: PR checks failing on pull request ]
```

---

## Mentor Insight

These validations act as **automated code governance**.

Large organizations enforce:

- branch naming conventions
- ticket references
- PR templates

---

# Task 3 — Scheduled Workflows (Cron)

## Concept

GitHub Actions supports **cron scheduling**.

Format:

```
minute hour day-of-month month day-of-week
```

Example:

```
30 2 * * 1
```

Meaning:

```
Every Monday at 2:30 AM UTC
```

---

## Workflow File

`.github/workflows/scheduled-tasks.yml`

```
[name: Scheduled Maintenance Tasks

on:
  schedule:
    - cron: '30 2 * * 1'
    - cron: '0 */6 * * *'
  workflow_dispatch:

jobs:
  scheduled-job:
    runs-on: ubuntu-latest

    steps:
      - name: Print schedule
        run: echo "Triggered by schedule -> ${{ github.event.schedule }}"

      - name: Health check
        run: |
          status=$(curl -o /dev/null -s -w "%{http_code}" https://github.com)
          echo "HTTP status -> $status"

          if [ "$status" != "200" ]; then
            echo "Health check failed"
            exit 1
          fi]
```

---

## Testing

Manually run workflow:

```
Actions → Scheduled Maintenance Tasks → Run workflow
```

---

### Screenshot Placeholder

```
[ Screenshot: Scheduled workflow manual trigger ]
```

---

## Cron Expressions (Lab Notes)

Every weekday at **9 AM IST**

```
30 3 * * 1-5
```

Explanation:

```
9:00 AM IST = 3:30 AM UTC
```

First day of every month at midnight

```
0 0 1 * *
```

---

## Why Scheduled Workflows May Be Delayed

GitHub warns that cron jobs may be skipped because:

- repositories are inactive
- runner availability issues
- platform load balancing

Scheduled workflows run **only on the default branch**.

---

# Task 4 — Path & Branch Filters

## Concept

GitHub workflows can run **only when specific files change**.

Useful when:

- only backend changes trigger builds
- documentation updates skip CI

---

## Workflow File

`.github/workflows/smart-triggers.yml`

```
[name: Smart Path Trigger

on:
  push:
    branches:
      - main
      - release/*
    paths:
      - 'src/**'
      - 'app/**'

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Print message
        run: echo "Source code changed — running pipeline"]
```

---

## Second Workflow Example

```
[name: Ignore Documentation Changes

on:
  push:
    paths-ignore:
      - '*.md'
      - 'docs/**'

jobs:
  skip-docs:
    runs-on: ubuntu-latest

    steps:
      - name: Message
        run: echo "Skipping docs-only change"]
```

---

## Testing

Push markdown file:

```
[echo "update docs" >> README.md]
[git commit -am "docs update"]
[git push]
```

Expected:

Workflow **does not run**.

---

## When to Use

| Use | Scenario |
|----|----|
| paths | Run pipeline only for app code |
| paths-ignore | Skip docs or config updates |

---

# Task 5 — Chaining Workflows

## Concept

Workflows can trigger **after another workflow finishes**.

Trigger:

```
workflow_run
```

This enables **pipeline stages** like:

```
tests → security scan → deployment
```

---

## Test Workflow

`.github/workflows/tests.yml`

```
[name: Run Tests

on:
  push:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Run tests
        run: echo "Running test suite"]
```

---

## Deployment Workflow

`.github/workflows/deploy-after-tests.yml`

```
[name: Deploy After Tests

on:
  workflow_run:
    workflows: ["Run Tests"]
    types: [completed]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Check result
        run: echo "Triggered by workflow conclusion -> ${{ github.event.workflow_run.conclusion }}"

      - name: Deploy
        if: github.event.workflow_run.conclusion == 'success'
        run: echo "Deploying application"

      - name: Warn if failed
        if: github.event.workflow_run.conclusion != 'success'
        run: |
          echo "Tests failed — deployment skipped"
          exit 1]
```

---

## Verification

Push code:

```
[git commit -am "trigger workflows"]
[git push]
```

Expected pipeline order:

```
tests.yml
↓
deploy-after-tests.yml
```

---

### Screenshot Placeholder

```
[ Screenshot: Chained workflows execution order ]
```

---

# Task 6 — External Event Triggers

## Concept

External systems can trigger workflows using:

```
repository_dispatch
```

Used by:

- monitoring systems
- Slack bots
- deployment portals
- external CI pipelines

---

## Workflow File

`.github/workflows/external-trigger.yml`

```
[name: External Deployment Trigger

on:
  repository_dispatch:
    types: [deploy-request]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Print environment
        run: echo "Deploying to -> ${{ github.event.client_payload.environment }}"]
```

---

## Trigger via GitHub CLI

```
[gh api repos/<owner>/<repo>/dispatches \
-f event_type=deploy-request \
-f client_payload='{"environment":"production"}']
```

---

## Verification

Expected output:

```
Deploying to -> production
```

---

## Mentor Insight

External triggers enable **event-driven DevOps automation**.

Example scenarios:

- PagerDuty triggers emergency deployment
- Monitoring detects outage → triggers rollback pipeline
- Slack command `/deploy prod`

---

# workflow_run vs workflow_call

| Feature | workflow_run | workflow_call |
|------|------|------|
| Trigger | Another workflow completion | Called as reusable workflow |
| Use Case | Pipeline chaining | Shared workflow templates |
| Example | Tests → Deploy | Standard build workflow reused across repos |

Simple explanation:

- **workflow_run** = sequential pipeline stages  
- **workflow_call** = reusable workflow module

---

# Final Verification Checklist

Ensure the repository contains:

```
.github/workflows/
```

Workflows:

- pr-lifecycle.yml
- pr-checks.yml
- scheduled-tasks.yml
- smart-triggers.yml
- tests.yml
- deploy-after-tests.yml
- external-trigger.yml

Documentation:

```
2026/day-47/day-47-advanced-triggers.md
```

---

# Expected Outcome

After completing this lab you now understand:

- Advanced GitHub Actions triggers
- Pull request lifecycle automation
- PR validation gates
- Scheduled automation pipelines
- Smart file-based triggers
- Workflow chaining
- External system triggers

These patterns mirror **production-grade CI/CD systems used by DevOps teams**.

---

# Learn in Public

Share your work on LinkedIn:

- PR validation workflows
- Advanced GitHub Actions triggers
- Event-driven pipelines

Suggested hashtags:

```
#90DaysOfDevOps
#DevOpsKaJosh
#TrainWithShubham
#GitHubActions
#DevOpsLearning
```

---

Happy Learning 🚀  
TrainWithShubham
