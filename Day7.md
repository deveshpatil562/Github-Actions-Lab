# GitHub Actions Lab Guide – Jobs, Steps, Environment Variables & Conditionals

This lab focuses on **controlling the execution flow of CI/CD pipelines using GitHub Actions**.  
In real DevOps pipelines, workflows rarely consist of a single job. Instead, they include **multiple jobs, dependencies between jobs, environment variables, outputs sharing, and conditional execution**.

By the end of this lab, you will understand how to design **smarter pipelines that behave dynamically depending on context, results, and workflow events**.

---

# Concepts

## Jobs in GitHub Actions

A **job** is a set of steps that run on the same runner.  
Workflows can contain **multiple jobs**.

By default:

- Jobs run **in parallel**

But we can control execution order using:

[needs: job-name]

Example pipeline order:

```
build → test → deploy
```

This ensures deployment only happens after successful build and test.

---

## Steps

A **step** is an individual task within a job.

Examples of steps:

- Running shell commands
- Running scripts
- Executing actions

Example step:

[steps:
  - name: Run Tests
    run: echo "Running tests"
]

Steps run **sequentially inside a job**.

---

## Environment Variables

Environment variables allow values to be reused inside workflows.

They can be defined at **three levels**.

### Workflow Level

Available to **all jobs and steps**.

Example:

[env:
  APP_NAME: myapp
]

---

### Job Level

Available only to steps inside that job.

Example:

[jobs:
  deploy:
    env:
      ENVIRONMENT: staging
]

---

### Step Level

Available only inside that specific step.

Example:

[steps:
  - name: Example Step
    env:
      VERSION: 1.0.0
]

---

## GitHub Context Variables

GitHub provides built-in context variables containing workflow information.

Common examples:

| Variable | Description |
|--------|--------|
| github.sha | commit SHA |
| github.actor | user who triggered workflow |
| github.ref | branch reference |
| github.event | event payload |

Example:

[echo "Commit SHA: ${{ github.sha }}"]

---

## Job Outputs

Jobs run on separate runners and cannot share variables directly.

To pass data between jobs, we use **job outputs**.

Process:

1. Generate value inside step
2. Store value as job output
3. Read output from dependent job

Example:

[echo "date=$(date)" >> $GITHUB_OUTPUT]

Access output:

[${{ needs.job-name.outputs.variable }}]

Real-world examples:

- Passing Docker image tag
- Passing artifact name
- Passing build version
- Passing generated secrets

---

## Conditionals

Conditionals allow steps or jobs to run only when certain conditions are true.

Example:

Run only on main branch:

[if: github.ref == 'refs/heads/main']

Run only when previous step fails:

[if: failure()]

---

## continue-on-error

Normally if a step fails, the job stops.

But with:

[continue-on-error: true]

The step fails but **the workflow continues execution**.

Useful when failures should **not stop the entire pipeline**.

---

# Lab Tasks

---

# Task 1 – Multi-Job Workflow

Create a workflow with **three jobs**:

- Build
- Test
- Deploy

Execution order:

```
build → test → deploy
```

We control this using **needs**.

---

## Step 1 – Create Workflow File

Create the file:

```
.github/workflows/multi-job.yml
```

Workflow configuration:

[
name: Multi Task Workflow

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: building stage
        run: echo "Building the app"

  test:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Testing Stage
        run: echo "Running tests"

  deploy:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - name: Deployment stage
        run: echo "Deploying"
]

---

## Verification

1. Go to **GitHub → Actions tab**
2. Run the workflow manually
3. Open the **workflow visualization graph**

Expected pipeline structure:

```
build
  ↓
test
  ↓
deploy
```

---

## Screenshot Placeholder

<img width="1902" height="872" alt="task1" src="https://github.com/user-attachments/assets/7e70b968-21ed-4ffb-b1f9-d59c5366b5c0" />


---

# Task 2 – Environment Variables

We will define environment variables at **three levels**:

- Workflow level
- Job level
- Step level

We will also print **GitHub context variables**.

---

## Step 1 – Create Workflow

Create:

```
.github/workflows/env-variables.yml
```

Workflow configuration:

[
name: ENV Variables

on:
  workflow_dispatch:

env:
  APP_NAME: myapp

jobs:
  var:
    runs-on: ubuntu-latest

    env:
      ENVIRONMENT: staging

    steps:
      - name: Print env vars
        env:
          VERSION: 1.0.0
        run: |
          echo "App: $APP_NAME"
          echo "Environment: $ENVIRONMENT"
          echo "Version: $VERSION"
          echo "Commit SHA: ${{ github.sha }}"
          echo "Actor: ${{ github.actor }}"
]

---

## Verification

Run the workflow and inspect logs.

Expected output:

```
App: myapp
Environment: staging
Version: 1.0.0
Commit SHA: <commit-id>
Actor: <username>
```

---

## Screenshot Placeholder

<img width="1917" height="856" alt="task2" src="https://github.com/user-attachments/assets/59772a26-1b76-475e-a0e0-d857730d8c56" />


---

# Task 3 – Job Outputs

This task demonstrates **passing data between jobs**.

---

## Step 1 – Create Workflow

[
name: Jobs Outputs

on:
  workflow_dispatch:

jobs:
  set-date:
    runs-on: ubuntu-latest

    outputs:
      today: ${{ steps.date.outputs.date }}

    steps:
      - id: date
        run: echo "date=$(date)" >> $GITHUB_OUTPUT

  use-date:
    runs-on: ubuntu-latest
    needs: set-date

    steps:
      - name: Print Date
        run: echo "Today's date is ${{ needs.set-date.outputs.today }}"
]

---

## Verification

Run the workflow.

Expected output:

```
Today's date is Tue Mar 11 ...
```

---

## Screenshot Placeholder

<img width="1918" height="878" alt="task-3" src="https://github.com/user-attachments/assets/65e112d1-8d03-4fc0-aec0-b68ddac1b48f" />


---

## Why Pass Outputs Between Jobs?

Jobs run in **isolated environments**.  

Outputs allow us to share important values like:

- Build numbers
- Artifact names
- Image tags
- Dynamic environment values

This makes pipelines **modular and reusable**.

---

# Task 4 – Conditionals

This workflow demonstrates conditional execution.

We will include:

- Step that runs only on main branch
- Step that runs only when previous step fails
- Job that runs only on push events
- Step with continue-on-error

---

## Workflow Configuration

[
name: Conditionals

on:
  push:
  pull_request:

jobs:
  demo:
    if: github.event_name == 'push'
    runs-on: ubuntu-latest

    steps:

      - name: Run only on main
        if: github.ref == 'refs/heads/main'
        run: echo "This runs only on main branch"

      - name: Intentional failure
        run: exit 1

      - name: Run if previous failed
        if: failure()
        run: echo "Previous step failed, so this runs"

      - name: Continue on error
        run: exit 1
        continue-on-error: true
]

---

## Verification

Observe:

- First step runs only on **main**
- Second step fails intentionally
- Third step executes because **failure() is true**
- Fourth step fails but workflow **continues**

---

## Screenshot Placeholder

<img width="1895" height="742" alt="task4" src="https://github.com/user-attachments/assets/02e8f3a4-6f2c-46d8-99cc-48270ff29420" />


---

# Task 5 – Smart Pipeline

Now we combine everything into a **smarter CI pipeline**.

Pipeline design:

```
lint        test
   \        /
     summary
```

Lint and test run **in parallel**.

Summary runs **after both complete**.

---

## Step 1 – Create Workflow

Create:

```
.github/workflows/smart-pipeline.yml
```

Workflow:

[
name: smart pipeline

on:
  push:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Lint code
        run: echo "Running lint checks...."

  test:
    runs-on: ubuntu-latest
    steps:
      - name: Runs Tests
        run: echo "Running tests...."

  summary:
    runs-on: ubuntu-latest
    needs: [lint, test]

    steps:
      - name: Print branch type
        run: |
          if [ "${{ github.ref }}" == "refs/heads/main" ]; then
            echo "This is a main branch push"
          else
            echo "This is a feature branch push"
          fi

          echo "Commit message: ${{ github.event.commits[0].message }}"
]

---

## Verification

Push a commit to the repository.

Expected behavior:

- `lint` and `test` run **simultaneously**
- `summary` runs **after both jobs finish**
- Logs display branch type and commit message

---

## Screenshot Placeholder

<img width="1918" height="872" alt="task5" src="https://github.com/user-attachments/assets/86c5a9c4-c324-4399-85d4-0a96126a7dcf" />

---

# Documentation Notes

Include the following explanation in your documentation file.

### What does `needs:` do?

`needs` defines **job dependencies**.  
It ensures a job starts **only after another job finishes successfully**.

Example:

[needs: build]

This creates a pipeline order.

---

### What does `outputs:` do?

`outputs` allows **sharing data between jobs**.

A job sets an output value and dependent jobs can read it using:

[${{ needs.job-name.outputs.variable }}]

This is essential for **dynamic pipelines**.

---

# Repository Structure

Example repository layout:

```
github-actions-practice
│
├── .github/workflows
│   ├── multi-job.yml
│   ├── env-variables.yml
│   ├── job-outputs.yml
│   ├── conditionals.yml
│   └── smart-pipeline.yml
│
└── 2026
    └── day-43
        └── day-43-jobs-steps.md
```

---

# Submission

Add the documentation file to your repository.

Steps:

[git add .]

[git commit -m "Added GitHub Actions jobs, steps, env variables and conditionals lab"]

[git push origin main]

Once pushed, verify:

- Workflows appear in **GitHub Actions tab**
- Graph shows **correct job dependencies**
- Logs show **environment variables, outputs, and conditional steps**

Great work — mastering these features means you're now capable of designing **real production-grade CI/CD workflows**.
