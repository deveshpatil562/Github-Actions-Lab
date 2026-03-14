# Reusable Workflows & Composite Actions – DevOps Lab Guide

This lab focuses on **code reusability in CI/CD pipelines using GitHub Actions**.  
In real production environments, DevOps teams avoid duplicating workflow logic across repositories. Instead, they create **reusable workflows** and **composite actions** to standardize pipelines and reduce maintenance overhead.

By completing this lab, you will learn how to design **modular CI/CD components** that can be reused across workflows and repositories.

---

# Learning Objectives

After completing this lab you will understand:

- What **Reusable Workflows** are in GitHub Actions
- How the **workflow_call** trigger works
- How to create a **caller workflow**
- How to pass **inputs, secrets, and outputs**
- How to build a **Composite Action**
- The difference between **Reusable Workflows and Composite Actions**

---

# Concepts

## 1. What is a Reusable Workflow?

A **Reusable Workflow** is a GitHub Actions workflow that can be called by another workflow.

Instead of rewriting the same CI/CD logic multiple times, you can define the workflow once and **call it like a function**.

Example real-world usage:

- Standardized Docker build pipelines
- Terraform deployment pipelines
- Security scanning pipelines
- Build pipelines shared across repositories

Benefits:

- Reduces duplicated YAML
- Improves maintainability
- Enables standard DevOps practices across teams

---

## 2. What is the workflow_call Trigger?

`workflow_call` allows one workflow to **trigger another workflow**.

It enables the reusable workflow to accept:

- Inputs
- Secrets
- Outputs

Example trigger:

[ on:
  workflow_call: ]

A workflow using this trigger **cannot run independently**.  
It must be invoked by another workflow.

---

## 3. Reusable Workflow vs Action

| Feature | Reusable Workflow | Regular Action |
|------|------|------|
| Usage | Called as a workflow | Used inside a step |
| Contains | Jobs | Steps |
| Trigger | workflow_call | uses: |
| Location | .github/workflows | separate action directory |

---

## 4. Where Must a Reusable Workflow Live?

Reusable workflows **must be stored in:**

[ .github/workflows/ ]

GitHub automatically recognizes workflows from this directory.

---

# Lab Tasks

---

# Task 1 – Research Summary

### What is a reusable workflow?

A reusable workflow is a GitHub Actions workflow designed to be **called by another workflow** to reuse CI/CD logic.

---

### What is workflow_call?

`workflow_call` is a trigger that allows workflows to be **invoked by other workflows**.

---

### Difference between reusable workflow and action?

Reusable workflows contain **jobs** while actions contain **steps**.

---

### Where must reusable workflows live?

[ .github/workflows/ ]

---

# Task 2 – Create Your First Reusable Workflow

Create the workflow file:

[ .github/workflows/reusable-build.yml ]

---

## Reusable Workflow YAML

[ name: Reusable Build Workflow

on:
  workflow_call:
    inputs:
      app_name:
        required: true
        type: string
      environment:
        required: true
        type: string
        default: staging
    secrets:
      docker_token:
        required: true
    outputs:
      build_version:
        description: "Generated build version"
        value: ${{ jobs.build.outputs.build_version }}

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      build_version: ${{ steps.version.outputs.build_version }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Print build info
        run: echo "Building ${{ inputs.app_name }} for ${{ inputs.environment }}"

      - name: Verify Docker token
        run: echo "Docker token is set: true"

      - name: Generate version
        id: version
        run: echo "build_version=v1.0-${GITHUB_SHA::7}" >> $GITHUB_OUTPUT ]

---

## Explanation

This workflow:

- Accepts inputs from a caller
- Accepts secrets
- Generates a build version
- Returns that version as an output

This workflow **cannot run by itself** because it uses `workflow_call`.

---

## Verification

Expected console output should show:

- Build message
- Confirmation that Docker token is set
- Generated version value

---

## Screenshot Placeholder

```
[ Screenshot: Reusable workflow job logs ]
```

---

# Task 3 – Create a Caller Workflow

The caller workflow triggers the reusable workflow.

Create:

[ .github/workflows/call-build.yml ]

---

## Caller Workflow YAML

[ name: Call Reusable Build

on:
  push:
    branches:
      - main

jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      app_name: "my-web-app"
      environment: "production"
    secrets:
      docker_token: ${{ secrets.DOCKER_TOKEN }}

  report:
    needs: build
    runs-on: ubuntu-latest

    steps:
      - name: Print build version
        run: echo "Build version: ${{ needs.build.outputs.build_version }}" ]

---

## Explanation

This workflow:

1. Triggers when code is pushed to **main**
2. Calls the reusable workflow
3. Passes inputs and secrets
4. Receives an output
5. Prints the build version

---

## Verification

Navigate to:

GitHub Repository → **Actions**

Expected result:

- Caller workflow starts
- Reusable workflow executes
- Second job prints version

Example output:

```
Building my-web-app for production
Docker token is set: true
Build version: v1.0-a1b2c3d
```

---

## Screenshot Placeholder

```
[ Screenshot: Caller workflow triggering reusable workflow ]
```

---

# Task 4 – Using Outputs From Reusable Workflow

The reusable workflow generated:

[ v1.0-${GITHUB_SHA::7} ]

Example:

```
v1.0-3a9f2b1
```

This output was exposed through:

[ outputs:
  build_version: ]

And consumed using:

[ ${{ needs.build.outputs.build_version }} ]

This pattern is commonly used for:

- Docker image tagging
- Deployment versions
- Artifact versions

---

# Task 5 – Create a Composite Action

Composite actions allow you to package **multiple steps as a reusable action**.

Create the directory:

[ .github/actions/setup-and-greet/action.yml ]

---

## Composite Action YAML

[ name: "Setup and Greet"
description: "A composite action that greets the user"

inputs:
  name:
    description: "Name of the person to greet"
    required: true
  language:
    description: "Greeting language"
    required: false
    default: "en"

outputs:
  greeted:
    description: "Indicates greeting happened"
    value: ${{ steps.set-output.outputs.greeted }}

runs:
  using: "composite"
  steps:

    - name: Print Greeting
      shell: bash
      run: |
        if [ "${{ inputs.language }}" = "en" ]; then
          echo "Hello ${{ inputs.name }} 👋"
        elif [ "${{ inputs.language }}" = "es" ]; then
          echo "Hola ${{ inputs.name }} 👋"
        elif [ "${{ inputs.language }}" = "fr" ]; then
          echo "Bonjour ${{ inputs.name }} 👋"
        else
          echo "Hello ${{ inputs.name }} 👋"
        fi

    - name: Print Date and Runner OS
      shell: bash
      run: |
        echo "Current Date: $(date)"
        echo "Runner OS: $RUNNER_OS"

    - name: Set Output
      id: set-output
      shell: bash
      run: |
        echo "greeted=true" >> $GITHUB_OUTPUT ]

---

# Task 5 Workflow Using Composite Action

Create:

[ .github/workflows/test-composite-action.yml ]

---

## Workflow YAML

[ name: Test Composite Action

on:
  workflow_dispatch:

jobs:
  greet:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repo
        uses: actions/checkout@v4

      - name: Run Custom Composite Action
        id: greet-step
        uses: ./.github/actions/setup-and-greet
        with:
          name: Devesh
          language: en

      - name: Verify Output
        run: echo "Was greeted? ${{ steps.greet-step.outputs.greeted }}" ]

---

# Verification

Trigger workflow manually.

Expected output:

```
Hello Devesh 👋
Current Date: <timestamp>
Runner OS: Linux
Was greeted? true
```

---

## Screenshot Placeholder

```
[ Screenshot: Composite action workflow logs ]
```

---

# Task 6 – Reusable Workflow vs Composite Action

| Feature | Reusable Workflow | Composite Action |
|------|------|------|
| Triggered by | workflow_call | uses: in a step |
| Can contain jobs? | Yes | No |
| Can contain multiple steps? | Yes | Yes |
| Lives where? | .github/workflows/ | .github/actions/ |
| Can accept secrets directly? | Yes | No |
| Best for | Reusing full CI/CD pipelines | Reusing step logic |

---

# Repository Structure

Example repository layout:

```
.github
│
├── workflows
│   ├── reusable-build.yml
│   ├── call-build.yml
│   └── test-composite-action.yml
│
└── actions
    └── setup-and-greet
        └── action.yml
```

---

# Final Deliverables

Your repository should contain:

- Reusable workflow
- Caller workflow
- Composite action
- Documentation markdown file

File path:

[ 2026/day-46/day-46-reusable-workflows.md ]

---

# Key DevOps Takeaways

This lab introduces an **important real-world DevOps concept: DRY pipelines**.

Production teams build **shared CI/CD components** that multiple services can reuse.

Examples in production:

- Shared Docker build workflow
- Standardized Terraform deployment workflow
- Shared security scanning workflow
- Shared Kubernetes deployment workflow

Mastering reusable workflows is a **production-level DevOps skill**.

---

# Suggested Commit

[ git add .
git commit -m "Add reusable workflows and composite action lab"
git push ]

---

# End of Lab
