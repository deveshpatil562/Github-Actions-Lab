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

=======
# GitHub Actions Lab – First Workflow

## Introduction

In this lab, I created my **first GitHub Actions CI workflow** and executed it successfully on GitHub's cloud runner.

GitHub Actions allows developers and DevOps engineers to **automate workflows such as build, test, and deployment** directly inside a GitHub repository.

Instead of running scripts manually, GitHub Actions executes them automatically whenever certain events occur.

Examples of events:
- Push to repository
- Pull request creation
- Scheduled tasks
- Manual triggers

In this lab, I created a simple workflow that runs automatically on **every push** and prints a message in the pipeline logs.

This helped me understand the **core structure of a GitHub Actions workflow file**.

---

# What is CI/CD?

CI/CD stands for:

### Continuous Integration (CI)
Developers frequently push code to a repository and automated pipelines run to verify the code.

### Continuous Delivery / Deployment (CD)
Code is automatically prepared for deployment or deployed to environments.

GitHub Actions is a **CI/CD automation platform** built directly into GitHub.

---

# GitHub Actions Workflow Concepts

Before creating the pipeline, it is important to understand the key components.

### Workflow
A **workflow** is an automated process defined in a YAML file.

Workflow files are stored in:

[.github/workflows/]

Example:

[.github/workflows/hello.yml]

---

### Event (Trigger)

The **event** tells GitHub when to run the workflow.

Example:

[on: push]

This means the workflow runs **every time code is pushed to the repository**.

---

### Job

A **job** is a group of steps executed on the same runner.

Example:

[jobs:
  greet:]

---

### Runner

A **runner** is the machine that executes the job.

GitHub provides cloud runners such as:

- ubuntu
- windows
- macOS

Example:

[runs-on: ubuntu-latest]

---

### Step

Each **step** performs a specific action inside the job.

Example:

- Checkout repository
- Run a command
- Install dependencies

---

### Action

An **Action** is a reusable unit of code.

Example:

[uses: actions/checkout@v4]

This action downloads your repository onto the runner.

---

### Run Command

The **run** keyword executes shell commands.

Example:

[run: echo "Hello From GitHub Actions"]

---

# Lab Task

## Task 1 – Repository Setup

Create a new repository.

Example repository name:

[github-actions-practice]

Clone the repository locally.

Command:

[git clone https://github.com/your-username/github-actions-practice.git]

Navigate into the repository.

[cd github-actions-practice]

---

## Task 2 – Create Workflow Folder

GitHub Actions workflows must be placed in a special directory.

Create the folder structure:

[mkdir -p .github/workflows]

---

## Task 3 – Create First Workflow

Create the workflow file:

[.github/workflows/hello.yml]

Add the following content.

```
[name: Hello Workflow

on: push

jobs:
  greet:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout the repository
        uses: actions/checkout@v4

      - name: Print Greeting
        run: echo "Hello From Github Actions"]
```

---

## Task 4 – Push Code

Add and commit the workflow.

[git add .]

[git commit -m "Add first GitHub Actions workflow"]

Push to GitHub.

[git push origin main]

---

## Task 5 – Observe Pipeline

After pushing the code:

1. Go to your repository
2. Click the **Actions tab**
3. Select the workflow run
4. Open the job named **greet**

GitHub automatically triggers the workflow.

---

# Workflow Anatomy Explained

Below is what each key in the workflow file means.

### name:

Defines the workflow name visible in the GitHub Actions UI.

[name: Hello Workflow]

---

### on:

Defines the **event that triggers the workflow**.

[on: push]

This means the workflow runs **whenever code is pushed**.

---

### jobs:

Defines all the jobs inside the workflow.

[jobs:]

A workflow can contain **multiple jobs**.

---

### runs-on:

Defines the **operating system of the runner**.

[runs-on: ubuntu-latest]

GitHub starts a temporary Ubuntu VM to run the job.

---

### steps:

Defines the sequence of tasks executed in the job.

[steps:]

Steps execute **one after another**.

---

### uses:

Runs a **pre-built GitHub Action**.

Example:

[uses: actions/checkout@v4]

This downloads the repository code into the runner.

---

### run:

Executes shell commands.

Example:

[run: echo "Hello From Github Actions"]

This prints a message in the pipeline logs.

---

### name (inside step)

Provides a **human-readable label** for the step.

Example:

[name: Print Greeting]

---

# Pipeline Execution Result

After pushing the workflow, GitHub automatically started the pipeline.

The job executed successfully and produced the expected output.

The runner executed the command:

[echo "Hello From Github Actions"]

---

# Output Observed in Pipeline Logs

The pipeline logs displayed:

[Hello From Github Actions]

This confirms that the workflow executed correctly.

---

# Screenshot of Successful Pipeline Run

Below is the screenshot of my first successful GitHub Actions run.

<img width="1200" alt="github actions first workflow success" src="SS_PATH_HERE">

---

# Screenshot Explanation

From the screenshot we can observe the following:

### Job Name

The job executed is called:

[greet]

---

### Steps Executed

The pipeline executed the following steps:

1. **Set up job**  
   GitHub prepared the runner environment.

2. **Checkout the code**  
   The action

   [actions/checkout@v4]

   downloaded the repository code to the runner.

3. **Print Greeting**  
   The command

   [echo "Hello From Github Actions"]

   was executed.

---

### Execution Time

The pipeline finished successfully in a few seconds.

This confirms that the workflow ran correctly on the **GitHub-hosted Ubuntu runner**.

---

# Learning Outcome

From this lab I learned:

- How GitHub Actions workflows work
- How to create a workflow YAML file
- Where workflow files must be stored
- How GitHub automatically triggers pipelines
- How to read pipeline logs
- How GitHub runners execute commands

This was my **first working CI pipeline using GitHub Actions**.

---

# Next Improvements

Future workflows can include:

- Running tests
- Building Docker images
- Deploying applications
- Running security scans
- Automating CI/CD pipelines

---

# Repository Structure

Example repository structure after this lab:

[github-actions-practice
 ├── .github
 │   └── workflows
 │        └── hello.yml
 └── README.md]

---

# Conclusion

This lab demonstrated how to create and run a **basic GitHub Actions workflow**.

Even though the workflow was simple, it represents the **foundation of CI/CD automation** used in real-world DevOps pipelines.

This was my **first successful pipeline run on GitHub Actions**.
