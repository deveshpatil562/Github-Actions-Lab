# CI/CD Concepts – GitHub Actions Lab Documentation

> This document explains CI/CD fundamentals in detail before writing any real pipeline.  
> This is a research + understanding lab focused on concepts, architecture, and real-world workflow exploration.

---

# 🎯 Objective

Before writing pipelines in GitHub Actions, understand:

- Why CI/CD exists
- What problems it solves
- CI vs Continuous Delivery vs Continuous Deployment
- Pipeline anatomy
- Real-world workflow example from an open-source repository

---

# 🧠 Task 1 – The Problem (Why CI/CD Exists)

## 👥 Scenario

A team of 5 developers pushes code to the same repository and manually deploys to production.

---

## ❓ What Can Go Wrong?

Manual deployments create serious risks:

- Developers overwrite each other's changes
- Someone deploys untested or broken code
- Merge conflicts happen during deployment
- Production downtime due to human error
- No consistent testing process
- Configuration mistakes
- No rollback strategy

Manual deployment is:
- Error-prone  
- Inconsistent  
- Slow  
- Stressful  

---

## ❓ What Does "It Works On My Machine" Mean?

"It works on my machine" means:

The code runs perfectly on the developer's local system but fails in production.

This happens because:

- Different operating systems
- Different dependency versions
- Missing environment variables
- Different configuration
- Different database versions

Impact:
- Wasted debugging time
- Team frustration
- Delayed releases

This is one of the biggest real-world engineering problems.

---

## ❓ How Many Times Can a Team Safely Deploy Manually?

Realistically:
- 1–2 times per day

More than that:
- Increases risk
- Causes deployment fatigue
- Leads to production instability

👉 Conclusion: Manual deployments with multiple developers are unreliable, slow, and risky.

---

# 🔁 Task 2 – CI vs CD

---

## 🔹 Continuous Integration (CI)

Definition:

Developers frequently merge code into a shared repository.  
Each push automatically triggers builds and automated tests.

Purpose:
- Catch bugs early
- Detect integration issues quickly
- Keep the main branch stable

How often?
- Multiple times per day

Example:
A team using GitHub Actions runs automated unit tests every time someone pushes code.

---

## 🔹 Continuous Delivery (CD)

Definition:

Builds on CI.  
The application is always kept in a deployable state.

“Delivery” means:
The software is ready for production anytime, but deployment requires manual approval.

Purpose:
- Ensure release readiness
- Reduce deployment risk

Example:
An e-commerce company packages every successful build and keeps it ready for release when the product manager approves.

---

## 🔹 Continuous Deployment

Definition:

Goes beyond Continuous Delivery.  
Every change that passes automated tests is automatically deployed to production without human approval.

Purpose:
- Fast feature delivery
- Rapid iteration

Example:
Companies like Facebook automatically push updates to production multiple times a day after tests pass.

---

## 🔎 Quick Summary

CI = Catch problems early with frequent integration  
Delivery = Always ready to release (manual approval required)  
Deployment = Automatic release to production  

---

# 🏗 Task 3 – Pipeline Anatomy

A CI/CD pipeline contains the following components:

---

## 🔹 Trigger

What it does:
Starts the pipeline automatically.

Examples:
- Code push
- Pull request
- Scheduled time (cron)
- Manual trigger

---

## 🔹 Stage

What it does:
A logical phase in the pipeline.

Common stages:
- Build
- Test
- Deploy

---

## 🔹 Job

What it does:
A unit of work inside a stage.

Examples:
- Running unit tests
- Building a Docker image
- Deploying to server

---

## 🔹 Step

What it does:
A single command or action inside a job.

Examples:
[npm install]  
[pytest]  
[docker build -t myapp .]

---

## 🔹 Runner

What it does:
The machine that executes pipeline jobs.

Types:
- GitHub-hosted runner
- Self-hosted runner

Example:
[runs-on: ubuntu-latest]

---

## 🔹 Artifact

What it does:
The output produced by a job.

Examples:
- Compiled binaries
- Docker images
- Test reports
- Build packages

Artifacts can be reused in later stages.

---

# 📊 Task 4 – CI/CD Pipeline Diagram

Scenario:

A developer pushes code to GitHub.  
The app is tested, built into a Docker image, and deployed to a staging server.

---

## Text-Based Pipeline Diagram

Developer Push  
        ↓  
Trigger (push event)  
        ↓  
Stage 1: Build  
        ↓  
Stage 2: Test  
        ↓  
Stage 3: Docker Build  
        ↓  
Stage 4: Deploy to Staging  

---

## Example Logical Flow

1. Trigger: push to main branch  
2. Job 1: Install dependencies  
3. Job 2: Run tests  
4. Job 3: Build Docker image  
5. Job 4: Deploy to staging server  

This ensures:
- No untested code reaches staging
- Docker image is built consistently
- Deployment is automated

---

# 🌍 Task 5 – Explore in the Wild (Real Workflow Example)

Repository explored: FastAPI (open-source Python framework)

Inside its:
.github/workflows/ folder

Example workflow analyzed:

---

## 📜 Workflow Name

[name: Mark stale issues and pull requests]

Purpose:
Automatically marks inactive issues and pull requests as stale.

---

## ⏰ Trigger

[on:]  
[  schedule:]  
[    - cron: '20 7 * * *']

Meaning:

- Runs daily
- At 07:20 UTC
- Time-based trigger
- Not triggered by push or PR

---

## ⚙️ Jobs

[jobs:]  
[  stale:]  
[    runs-on: ubuntu-latest]

There is:
- 1 job named "stale"
- Runs on GitHub-hosted Ubuntu runner

---

## 🔑 Permissions

[permissions:]  
[  issues: write]  
[  pull-requests: write]

Why?

Because the workflow:
- Adds labels
- Posts comments

It needs write access.

---

## 🛠️ Steps

[steps:]  
[- uses: actions/stale@v5]  
[  with:]  
[    repo-token: \${{ secrets.GITHUB_TOKEN }}]  
[    stale-issue-message: 'Stale issue message']  
[    stale-pr-message: 'Stale pull request message']  
[    stale-issue-label: 'no-issue-activity']  
[    stale-pr-label: 'no-pr-activity']

Explanation:

- Uses official GitHub Action: actions/stale version 5
- Authenticates using built-in GITHUB_TOKEN
- Posts comment on inactive issues
- Adds labels to mark them stale

---

## 📝 Workflow Summary

Trigger: Scheduled daily at 07:20 UTC  
Jobs: 1 job (stale)  
Purpose: Automatically marks inactive issues and PRs with a label and message  

This shows:
CI/CD is not only about building and deploying apps —  
It also automates repository maintenance.

---

# 💡 Important Learnings

- CI/CD is a practice, not just a tool
- GitHub Actions is one implementation of CI/CD
- A failing pipeline is NOT a problem
- A failing pipeline means the system caught an issue early
- Automation increases reliability and speed

---

# 📂 Final Output Summary

This document includes:

✔ The problem manual deployments create  
✔ CI vs Delivery vs Deployment definitions  
✔ Pipeline anatomy explanation  
✔ CI/CD diagram  
✔ Real GitHub Actions workflow breakdown  

---

# 🚀 Next Step

Now that concepts are clear:

Next phase → Start writing actual GitHub Actions workflows.

Understanding first. Automation second.
