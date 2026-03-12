# DevOps Lab Guide: GitHub Runners – Hosted & Self-Hosted

This lab helps you understand **GitHub runners**, both hosted by GitHub and self-hosted on your own machine. You will set up workflows to run jobs on different OS runners and configure your own self-hosted runner.

---

## Concepts

### 1. What is a GitHub Runner?
A **runner** is a machine that executes your GitHub Actions jobs.  
- **GitHub-Hosted Runner:** Provided and maintained by GitHub, runs in the cloud.  
- **Self-Hosted Runner:** You provide the machine (local or cloud VM) and manage it.  

**Why it matters:** Every job needs an environment to run in. Runners are that environment.

---

### 2. Why Pre-installed Tools Matter
GitHub-hosted runners come with **pre-installed tools** like Docker, Python, Node, Git, etc.  
- Saves setup time  
- Ensures consistency across runs  
- Reduces workflow complexity  

---

### 3. Labels in Self-Hosted Runners
Labels let you **target specific runners** when you have multiple machines.  
- Example: `my-linux-runner`  
- Allows job routing and efficient resource use

---

## Lab Tasks

### Task 1: GitHub-Hosted Runners

**Objective:** Run jobs on multiple OS runners.

[ 
name: Multi-OS Workflow

on: [workflow_dispatch]

jobs:
  ubuntu-job:
    runs-on: ubuntu-latest
    steps:
      - name: Print system info
        shell: bash
        run: |
          echo "OS: $(uname -s)"
          echo "Hostname: $(hostname)"
          echo "User: $(whoami)"

  windows-job:
    runs-on: windows-latest
    steps:
      - name: Print system info
        run: |
          echo "OS: Windows"
          hostname
          whoami

  macos-job:
    runs-on: macos-latest
    steps:
      - name: Print system info
        shell: bash
        run: |
          echo "OS: $(uname -s)"
          echo "Hostname: $(hostname)"
          echo "User: $(whoami)"
]

**Verification:**  
- Trigger the workflow  
- Watch all 3 jobs run in parallel  
- Check the output for OS, hostname, and user  

**Mentor Notes:**  
- GitHub-hosted runners are **managed by GitHub**, so you don’t worry about maintenance.  
- They are ideal for testing across multiple OS environments quickly.

**Screenshots:**

<img width="1892" height="715" alt="task1" src="https://github.com/user-attachments/assets/00df83e3-2b8a-4da6-81a9-41132c962cc3" />

---

### Task 2: Explore Pre-installed Tools

[ 
name: Multi-OS Workflow

on: [workflow_dispatch]

jobs:
  ubuntu-job:
    runs-on: ubuntu-latest
    steps:
      - name: Print Docker version
        run: docker --version

      - name: Print Python version
        run: python3 --version

      - name: Print Node.js version
        run: node --version

      - name: Print Git version
        run: git --version
]

**Verification:**  
- Trigger workflow  
- Confirm versions of Docker, Python, Node.js, and Git are printed  

**Mentor Notes:**  
- Pre-installed tools save setup time  
- Ensures consistency across GitHub-hosted runs  
- Check [GitHub Docs](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners#supported-runners-and-hardware-resources) for full tool list

**Screenshots:**

<img width="1882" height="865" alt="task2" src="https://github.com/user-attachments/assets/d8c473ae-eb0f-4ba2-ad7b-508b91978bdd" />

---

### Task 3: Set Up a Self-Hosted Runner

**Steps:**  
1. Go to your GitHub repo → **Settings → Actions → Runners → New self-hosted runner**  
2. Choose **Linux**  
3. Copy the generated setup script  

[ 
# Example script from GitHub
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.308.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.308.0/actions-runner-linux-x64-2.308.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.308.0.tar.gz
./config.sh --url https://github.com/your-repo --token YOUR_TOKEN
./run.sh
]

**Optional (persistent service):**  

[ 
sudo ./svc.sh install
sudo ./svc.sh start
]

**Verification:**  
- Check GitHub → Actions → Runners  
- The runner should appear as **Idle** with a green dot  

**Mentor Notes:**  
- Self-hosted runners give **control over hardware** and installed software  
- Ideal for long-running or resource-intensive jobs

**Screenshots:**

<img width="1888" height="870" alt="task3" src="https://github.com/user-attachments/assets/bee09c27-1024-43f3-aa78-aac7359c34ee" />

---

### Task 4: Use Your Self-Hosted Runner

[ 
name: Self Hosted

on:
  workflow_dispatch:

jobs:
  self-hosting:
    runs-on: [self-hosted, my-linux-runner]
    steps:
      - name: Print Hostname
        run: echo "$(hostname)"

      - name: Print working directory
        run: echo "$(pwd)"

      - name: Create a file
        run: echo "Hello from self-hosted runner!!!" > ~/actions-runner/testfile.txt

      - name: Verify file exists
        run: ls -l ~/actions-runner/testfile.txt
]

**Verification:**  
- Trigger workflow  
- Check that `testfile.txt` exists on your runner machine  
- Confirm hostname and working directory match your self-hosted runner  

**Mentor Notes:**  
- Jobs now run on **your machine**, not GitHub servers  
- Great for accessing internal resources, private networks, or custom environments

**Screenshots:**

<img width="1890" height="833" alt="task4" src="https://github.com/user-attachments/assets/4d92411e-3d91-4bfd-baf5-f033172eef45" />

<img width="1402" height="97" alt="task4-1" src="https://github.com/user-attachments/assets/1db48e35-eebb-4f68-bf04-9d97732ccd98" />

---

### Task 5: Labels

**Steps:**  
1. Go to **Runners → Edit → Add Label** (e.g., `my-linux-runner`)  
2. Update workflow:  

[ 
runs-on: [self-hosted, my-linux-runner]
]

**Verification:**  
- Trigger workflow  
- Ensure the job runs on the runner with the specified label  

**Mentor Notes:**  
- Labels help **direct jobs** to specific runners  
- Useful when you have multiple self-hosted machines with different capabilities  

---

### Task 6: GitHub-Hosted vs Self-Hosted Comparison

| Feature | GitHub-Hosted | Self-Hosted |
|---------|---------------|-------------|
| Who manages it? | GitHub | You / your team |
| Cost | Free / included in plan | Hardware + electricity + maintenance |
| Pre-installed tools | Many (Docker, Python, Node, Git, etc.) | Only what you install |
| Good for | Quick, ephemeral, multi-OS testing | Long-running jobs, private networks, custom hardware |
| Security concern | Limited to GitHub environment | You manage security, updates, and isolation |

---

### Deliverables

1. Markdown file: `day-42-runners.md`  
2. Screenshot of **self-hosted runner Idle in GitHub**  
3. Screenshot of **job running on self-hosted runner**  
4. Notes including comparison table  

---

### Mentor Tips

- Always verify each step works on the target runner  
- Use labels to organize multiple self-hosted runners  
- Keep workflows simple and readable  
- Document your results for GitHub learning repo  

---

### Screenshot Placeholders
