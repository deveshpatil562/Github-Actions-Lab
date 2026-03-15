# 🚀 Docker Build & Push in GitHub Actions (CI/CD Pipeline)

> DevOps Lab Guide – Docker CI/CD using GitHub Actions  
> Repository Documentation for Learning DevOps in Public

---

# 📌 Lab Overview

In modern DevOps environments, **automation is everything**.  
Manually building Docker images and pushing them to registries is inefficient and error-prone.

This lab demonstrates how to create a **fully automated CI/CD pipeline** using **GitHub Actions** that:

1. Builds a Docker image whenever code is pushed.
2. Tags the image automatically.
3. Pushes the image to **Docker Hub**.
4. Shows pipeline status through a **badge in the README**.

Once implemented, the pipeline will perform the entire workflow automatically:

```
Developer Push → GitHub → GitHub Actions Pipeline → Docker Build → Docker Hub Push → Image Ready to Deploy
```

This is **exactly how production pipelines work** in real DevOps environments.

---

# 🧠 Concepts You Must Understand First

---

# 1️⃣ CI/CD Pipeline

CI/CD stands for:

| Term | Meaning |
|-----|------|
| CI | Continuous Integration |
| CD | Continuous Delivery / Deployment |

### Continuous Integration

Developers push code frequently, and every push triggers an automated pipeline that:

- Builds the application
- Runs tests
- Verifies code integrity

### Continuous Delivery

The pipeline prepares deployable artifacts automatically such as:

- Docker images
- Packages
- Build artifacts

---

# 2️⃣ GitHub Actions

**GitHub Actions** is GitHub's native automation platform.

It allows you to create workflows that trigger on events like:

- push
- pull_request
- release
- schedule

Workflows are defined in:

```
.github/workflows/
```

Example workflow file:

```
docker-publish.yml
```

---

# 3️⃣ Docker Image Build Automation

Normally developers build images manually:

[ docker build -t myapp . ]

But with CI/CD:

```
Git Push → Pipeline builds image automatically
```

---

# 4️⃣ Docker Hub as a Container Registry

Docker Hub stores Docker images similar to how GitHub stores code.

Example image:

```
docker.io/<username>/myapp:latest
```

Tags help track versions:

| Tag | Meaning |
|----|----|
| latest | newest version |
| sha-xxxxx | specific commit version |

---

# 5️⃣ GitHub Secrets

Sensitive credentials must never be stored in code.

GitHub provides **Secrets** to securely store credentials.

Example secrets used in this lab:

```
DOCKER_USERNAME
DOCKER_TOKEN
```

These secrets are referenced inside workflows.

---

# 6️⃣ Docker GitHub Actions

GitHub provides official actions for Docker operations.

### Login Action

```
docker/login-action
```

Authenticates GitHub Actions with Docker Hub.

### Build & Push Action

```
docker/build-push-action
```

Builds images and pushes them to a registry.

---

# 🧪 Lab Architecture

```
Git Push
   │
   ▼
GitHub Repository
   │
   ▼
GitHub Actions Workflow
   │
   ├── Checkout Code
   ├── Login to Docker Hub
   ├── Build Docker Image
   ├── Tag Image
   └── Push Image
         │
         ▼
      Docker Hub
         │
         ▼
   Pull & Run Container Anywhere
```

---

# 📂 Repository Structure

```
github-actions-practice
│
├── Dockerfile
├── index.html
│
└── .github
    └── workflows
        └── docker-publish.yml
```

---

# 🧪 Task 1 — Prepare the Repository

We will use the **Dockerized application already present in the repository**.

The repo contains:

```
Dockerfile
index.html
```

The Dockerfile builds a small web application container.

---

## Step 1 — Verify Dockerfile

Example structure:

[ Dockerfile ]

```
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
```

This builds a lightweight **NGINX web server container**.

---

## Step 2 — Confirm index.html Exists

Example:

[ index.html ]

```
<h1>Hello from Docker CI/CD Pipeline 🚀</h1>
```

---

## Step 3 — Verify GitHub Secrets

Go to:

```
Repository Settings → Secrets → Actions
```

Ensure these secrets exist:

```
DOCKER_USERNAME
DOCKER_TOKEN
```

---

### 📸 Screenshot Placeholder

```
[Screenshot: GitHub Secrets Configuration]
```

---

# 🧪 Task 2 — Build Docker Image in CI

We now create the workflow file.

---

## Step 1 — Create Workflow Folder

[ mkdir -p .github/workflows ]

---

## Step 2 — Create Workflow File

```
.github/workflows/docker-publish.yml
```

---

## Step 3 — Add Workflow Code

[ docker-publish.yml ]

```
name: Docker Publish

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:

      - name: Checkout code
        uses: actions/checkout@v4

      - name: Docker Login
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_TOKEN }}

      - name: Extract short sha
        run: echo "sha_short=${GITHUB_SHA::7}" >> $GITHUB_ENV

      - name: Build and Push
        if: github.ref == 'refs/heads/main'
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/myapp:latest
            ${{ secrets.DOCKER_USERNAME }}/myapp:sha-${{ env.sha_short }}
```

---

# 🧪 Task 3 — Push Image to Docker Hub

This step happens automatically after:

```
docker login
docker build
docker push
```

But inside GitHub Actions.

Two tags are pushed:

```
latest
sha-<commit>
```

Example:

```
deveshpatil/myapp:latest
deveshpatil/myapp:sha-a1b2c3d
```

---

## Verification

Go to:

```
https://hub.docker.com
```

Check your repository.

---

### 📸 Screenshot Placeholder

```
[Screenshot: Docker Hub Repository with Tags]
```

---

# 🧪 Task 4 — Push Only From Main Branch

The workflow includes a condition:

```
if: github.ref == 'refs/heads/main'
```

This ensures:

| Branch | Image Push |
|------|------|
main | ✅ Yes
feature | ❌ No
PR | ❌ No

---

## Test This Behavior

Create a feature branch:

[ git checkout -b test-branch ]

Push changes:

[ git push origin test-branch ]

Pipeline result:

```
Image builds
But push step is skipped
```

---

### 📸 Screenshot Placeholder

```
[Screenshot: GitHub Actions showing skipped push step]
```

---

# 🧪 Task 5 — Add Workflow Status Badge

Badges show pipeline health directly in the README.

---

## Step 1 — Get Badge URL

Format:

```
https://github.com/<user>/<repo>/actions/workflows/docker-publish.yml/badge.svg
```

Example:

```
https://github.com/deveshpatil/github-actions-practice/actions/workflows/docker-publish.yml/badge.svg
```

---

## Step 2 — Add to README

[ README.md ]

```
![Docker Pipeline](https://github.com/<user>/<repo>/actions/workflows/docker-publish.yml/badge.svg)
```

Push changes.

If the pipeline succeeds the badge becomes:

```
🟢 passing
```

---

### 📸 Screenshot Placeholder

```
[Screenshot: Green pipeline badge in README]
```

---

# 🧪 Task 6 — Pull and Run the Image

Now verify the pushed image works.

---

## Step 1 — Pull Image

[ docker pull <docker-username>/myapp:latest ]

Example:

[ docker pull deveshpatil/myapp:latest ]

---

## Step 2 — Run Container

[ docker run -d -p 8080:80 <docker-username>/myapp:latest ]

---

## Step 3 — Verify Application

Open browser:

```
http://localhost:8080
```

You should see:

```
Hello from Docker CI/CD Pipeline
```

---

### 📸 Screenshot Placeholder

```
[Screenshot: Application running from Docker container]
```

---

# 🔎 Full Journey Explained (From Push to Running Container)

Understanding this workflow is critical for DevOps engineers.

### Step 1 — Developer Push

A developer pushes code:

```
git push origin main
```

---

### Step 2 — GitHub Trigger

GitHub detects:

```
push event
```

Workflow starts.

---

### Step 3 — GitHub Runner Starts

GitHub launches a temporary server:

```
ubuntu-latest runner
```

---

### Step 4 — Code Checkout

Pipeline downloads repository code.

---

### Step 5 — Docker Login

GitHub Actions authenticates with Docker Hub using stored secrets.

---

### Step 6 — Docker Build

Docker image is built from:

```
Dockerfile
```

---

### Step 7 — Tagging

Image is tagged:

```
latest
sha-commit
```

---

### Step 8 — Push to Docker Hub

Image is uploaded to:

```
Docker Hub registry
```

---

### Step 9 — Deployment Anywhere

Any machine can now run:

```
docker pull <image>
docker run <image>
```

This completes the CI/CD pipeline.

---

# 📂 Final Documentation File

Create the file:

```
2026/day-45/day-45-docker-cicd.md
```

Include:

- Workflow YAML
- Docker Hub image link
- Screenshots
- Explanation of the pipeline

---

# 📸 Required Screenshots

```
Pipeline run
Docker Hub image
Workflow logs
Skipped push on feature branch
Green badge in README
Running container
```

---

# 🎯 Expected Outcome

At the end of this lab you will have:

✅ Automated Docker build pipeline  
✅ Docker Hub image published automatically  
✅ Branch protection for pushes  
✅ CI/CD badge in README  
✅ Production-style workflow experience  

---

# 🚀 DevOps Skills Practiced

```
Docker
CI/CD pipelines
GitHub Actions
Container registries
Branch based automation
DevOps documentation
```

---

# 🌍 Learn in Public

Share your progress on LinkedIn:

Include:

- Docker Hub image link
- GitHub repo
- CI/CD badge screenshot

Use hashtags:

```
#90DaysOfDevOps
#DevOpsKaJosh
#TrainWithShubham
#Docker
#GitHubActions
#DevOps
```

---

# 🎉 Lab Complete

You have now built a **real-world Docker CI/CD pipeline** using GitHub Actions.

This is the same workflow used by:

- Startups
- DevOps teams
- Cloud-native platforms
- Kubernetes deployments

Keep building. The next step is **automated deployment**.

🚀
