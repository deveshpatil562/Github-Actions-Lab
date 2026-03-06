# GitHub Actions Lab – Triggers & Matrix Builds

This lab focuses on **how workflows start (triggers)** and **how to run the same job across multiple environments using matrix builds**.

In real DevOps pipelines, workflows do not run only on `push`.  
They can run on:

- Pull Requests
- Schedules (cron jobs)
- Manual triggers
- Multiple environments simultaneously

Understanding these triggers is critical for **CI/CD automation in production pipelines**.

---

# Learning Objectives

After completing this lab you will understand:

• Different ways to trigger GitHub Actions workflows  
• How Pull Request validation pipelines work  
• How scheduled pipelines run automatically  
• How to manually trigger workflows with inputs  
• How to use matrix builds for multi-environment testing  
• How to exclude matrix combinations  
• How fail-fast behavior works in parallel jobs  

---

# GitHub Actions Triggers

GitHub Actions workflows are controlled using the **`on:`** keyword.

Examples:

| Trigger | Description |
|------|------|
| push | Runs workflow when code is pushed |
| pull_request | Runs workflow during PR activity |
| schedule | Runs workflow using cron timing |
| workflow_dispatch | Allows manual triggering |
| release | Runs when release is published |

Example:

[

on:
  push:
    branches: [main]

]

---

# TASK 1 — Trigger Workflow on Pull Request

In professional teams, code is reviewed using Pull Requests.

CI pipelines automatically run when a PR is opened to verify:

• Tests pass  
• Code builds successfully  
• Quality checks pass  

---

## Create Workflow

Create the file:

.github/workflows/pr-check.yml

Workflow configuration:

[

name: PR Check Workflow

on:
  pull_request:
    branches: [main]

jobs:
  pr-validation:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Print PR branch name
        run: echo "PR check running for branch: ${{ github.head_ref }}"

]

---

## Test the Workflow

Step 1 — Create new branch

[

git checkout -b feature-pr-test

]

Step 2 — Make a change

[

echo "Testing PR workflow" >> test.txt

]

Step 3 — Commit changes

[

git add .
git commit -m "Testing PR workflow trigger"

]

Step 4 — Push branch

[

git push origin feature-pr-test

]

Step 5 — Open Pull Request

Go to GitHub → **Create Pull Request to `main`**

The workflow should automatically run.

---

## Verification

Check:

• Actions tab → workflow should run  
• PR page → workflow status appears  

---

## Screenshot

PR workflow execution

<img width="983" height="872" alt="task-1" src="https://github.com/user-attachments/assets/f52be93a-6c07-44c5-9257-adcc25c290a7" />


---

# TASK 2 — Scheduled Workflow (Cron)

Sometimes workflows must run **automatically without code changes**.

Common use cases:

• Nightly builds  
• Security scans  
• Backup jobs  
• Dependency updates  

This is done using **cron syntax**.

---

## Cron Format

Cron syntax format:

minute hour day-of-month month day-of-week

Example:

[

0 0 * * *

]

Meaning:

Run every day at **00:00 UTC**

---

## Add Scheduled Trigger

You can add schedule to any workflow.

Example:

[

on:
  schedule:
    - cron: '0 0 * * *'

]

---

## Full Workflow Example

[

name: Nightly Workflow

on:
  schedule:
    - cron: '0 0 * * *'

jobs:
  nightly-job:
    runs-on: ubuntu-latest

    steps:
      - name: Print message
        run: echo "Nightly scheduled workflow executed"

]

---

## Important Note

GitHub schedules run in **UTC time**.

---

## Question

What is the cron expression for **every Monday at 9 AM?**

Answer:

[

0 9 * * 1

]

Explanation:

0 → minute  
9 → hour  
* → every day  
* → every month  
1 → Monday  

---

# TASK 3 — Manual Workflow Trigger

Sometimes we want to run pipelines manually.

Example:

• Deploy staging environment  
• Run database migrations  
• Trigger emergency pipeline  

GitHub provides **workflow_dispatch** trigger.

---

## Create Workflow

File:

.github/workflows/manual.yml

---

## Workflow Configuration

[

name: Manual Deployment Workflow

on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Enter environment (staging or production)"
        required: true
        default: "staging"

jobs:
  manual-job:
    runs-on: ubuntu-latest

    steps:
      - name: Print environment
        run: echo "Deployment environment is ${{ github.event.inputs.environment }}"

]

---

## Run the Workflow

Go to:

GitHub Repository → **Actions tab**

Steps:

1 Click workflow  
2 Click **Run workflow**  
3 Enter environment name  

Example inputs:

staging  
production  

---

## Verification

Confirm:

• Workflow starts manually  
• Input value prints in logs  

---

# TASK 4 — Matrix Builds

Matrix builds allow the same job to run across multiple environments.

Common usage:

• Test across multiple OS  
• Test across multiple language versions  
• Validate compatibility  

Example:

Testing Python on:

• Python 3.10  
• Python 3.11  
• Python 3.12  

---

## Create Matrix Workflow

File:

.github/workflows/matrix.yml

---

## Workflow Configuration

[

name: Matrix Build Workflow

on:
  push:
    branches: [main]

jobs:
  matrix-test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: [3.10, 3.11, 3.12]

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Print Python version
        run: python --version

]

---

## Result

This creates **3 parallel jobs**:

Python 3.10  
Python 3.11  
Python 3.12  

---

## Screenshot

<img width="981" height="873" alt="task-4" src="https://github.com/user-attachments/assets/13f58fe2-dace-4ec2-a8bc-fd6ca62ded3c" />

---

# Extend Matrix with Multiple Operating Systems

Add operating systems.

Updated matrix:

[

strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    python-version: [3.10, 3.11, 3.12]

]

Update runner:

[

runs-on: ${{ matrix.os }}

]

---

## Total Jobs

2 OS × 3 Python versions = **6 jobs**

These run **in parallel**.

---

## Screenshot

Add screenshot showing 6 parallel jobs.

Example:

<img width="981" height="873" alt="task-4" src="https://github.com/user-attachments/assets/4907466b-940b-4836-9e7b-5a1740a61ffa" />


---

# TASK 5 — Exclude Matrix Combinations

Sometimes specific combinations fail or are unsupported.

Example:

Python 3.10 may not work on Windows.

You can exclude combinations.

---

## Matrix with Exclusion

[

strategy:
  fail-fast: false

  matrix:
    os: [ubuntu-latest, windows-latest]
    python-version: [3.10, 3.11, 3.12]

    exclude:
      - os: windows-latest
        python-version: "3.10"

]

---

## What Happens Now

Instead of 6 jobs:

1 combination removed

Total jobs = **5**

---

# Fail-Fast Behavior

Fail-fast controls what happens when one matrix job fails.

Default behavior:

fail-fast: true

Meaning:

If **one job fails → remaining jobs stop immediately**

---

## Disable Fail Fast

[

fail-fast: false

]

Meaning:

If one job fails → **other jobs continue running**

This is useful when you want to **see failures across all environments**.

---

# Testing Fail-Fast

To test behavior:

Add failing command in one job.

Example:

[

run: exit 1

]

Observe:

With fail-fast true → jobs cancel  
With fail-fast false → jobs continue  

---

# Screenshot

<img width="968" height="818" alt="task5" src="https://github.com/user-attachments/assets/82554af9-132d-468d-95c0-c87ab794122d" />

---

# Final Repository Structure

Example project structure:

[

github-actions-practice
│
├── .github
│   └── workflows
│       ├── pr-check.yml
│       ├── manual.yml
│       ├── matrix.yml
│       └── nightly.yml
│
└── 2026
    └── day-41
        └── day-41-triggers.md

]

---

# Key Takeaways

• Pull Request triggers enforce CI checks before merging  
• Scheduled workflows automate recurring tasks  
• Manual workflows allow controlled execution  
• Matrix builds test across multiple environments  
• Excluding combinations prevents unsupported setups  
• fail-fast controls parallel job behavior  

These techniques are widely used in **production CI/CD pipelines**.

---

# Lab Complete

You have successfully practiced:

• Pull request pipelines  
• Scheduled workflows  
• Manual triggers  
• Matrix builds  
• Exclusion rules  
• Fail-fast behavior  

---

