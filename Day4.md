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
