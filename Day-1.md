# YAML Basics (Personal Github Lab)

---

# 📌 Introduction

Before writing any CI/CD pipeline (GitHub Actions, GitLab CI, Kubernetes manifests), you must understand YAML.

Every modern DevOps tool uses YAML.

YAML stands for:

YAML Ain’t Markup Language

It is:

- Human-readable
- Indentation-based
- Strict about spacing
- Used to define configuration declaratively

Today’s goal:
- Understand YAML syntax
- Write YAML files manually
- Validate YAML
- Break YAML intentionally and fix it

This is foundational before writing any CI/CD pipeline.

---

# 🔎 YAML Fundamentals (Detailed Explanation)

## 1️⃣ Key-Value Structure

Basic YAML format:

[key: value]

Example:

[name: Devesh]

Rules:
- A colon separates key and value
- A space must come after colon
- No tabs allowed
- YAML is case-sensitive

---

## 2️⃣ Indentation

Indentation defines hierarchy.

YAML does NOT use:
- {}
- ()
- XML tags

It uses spaces to define structure.

Standard practice:
2 spaces per indentation level.

Wrong indentation = broken YAML.

---

## 3️⃣ Data Types in YAML

String:
[name: Devesh]

Number:
[experience_years: 1]

Boolean:
[learning: true]

Important:
true ≠ "true"

true → Boolean  
"true" → String

---

## 4️⃣ Lists in YAML

Two ways to write lists:

Block style:
[
tools:
  - docker
  - kubernetes
]

Inline style:
[tools: [docker, kubernetes]]

Both are valid.

---

## 5️⃣ Nested Objects

Hierarchy is defined by indentation:

[
server:
  name: prod-server
  ip: 192.168.1.10
]

The keys under server must be indented.

---

## 6️⃣ Multi-line Strings

YAML supports two block styles:

|  → preserves newlines  
>  → folds lines into one

Literal style:
[
script: |
  echo "Hello"
  echo "World"
]

Folded style:
[
script: >
  echo "Hello"
  echo "World"
]

---

# 🛠 Challenge Tasks

---

# 🔹 Task 1: Key-Value Pairs

Create person.yaml describing yourself.

## person.yaml

[
name: Devesh
role: DevOps Learner
experience_years: 0
learning: true
]

Verify using:

[cat person.yaml]

Checklist:
- No tabs
- Clean spacing
- Boolean used correctly

---

# 🔹 Task 2: Lists

Add tools and hobbies.

Updated person.yaml:

[
name: Devesh
role: DevOps Learner
experience_years: 0
learning: true

tools:
  - docker
  - kubernetes
  - linux
  - git
  - github-actions

hobbies: [coding, fitness, tech-learning]
]

Two ways to write lists:
1. Block format (- item)
2. Inline format [item1, item2]

---

# 🔹 Task 3: Nested Objects

Create server.yaml

## server.yaml

[
---
Server:
  name: tosap4321
  ip: 192.168.31.24
  port: 80

Database:
  Host: tosap4321
  Name: mysql-data
  credentials:
    name: MYSQL_USER
    password: MYSQL_PASSWORD
]

Explanation:

Server → Parent key  
name, ip, port → Nested under Server  

Database → Parent key  
credentials → Nested object  
name & password → Nested under credentials  

Indentation controls structure.

---

# 🔹 Task 4: Multi-line Strings

Add startup_script using folded style (>)

[
startup_script: >
  echo "One of the practice YAML file"
  echo "started with writing yaml file"
  echo "Lets see how this will help in github actions"
]

Difference:

| preserves newlines  
> folds into single line  

When to use:

| → scripts, certificates, config blocks  
> → long readable paragraphs  

---

# 🔹 Task 5: YAML Validation

Validate using:

[yamllint.com]

OR install locally:

[sudo apt install yamllint]

Validate:

[yamllint server.yaml]

---

# 📸 Validation Screenshot Explanation

In my screenshot:

- YAML Lint shows green message: "Valid YAML!"
- No indentation errors
- Nested objects correctly aligned
- Folded block (>) properly structured
- No tabs used

This confirms:
Structure and spacing are correct.

---

# 🔴 What Happens If You Use Tabs?

If you insert a TAB instead of spaces:

Common error:

[found character '\t' that cannot start any token]

YAML strictly forbids tabs.

---

# 🔴 Break Indentation Intentionally

If indentation is wrong:

Example error:

[mapping values are not allowed here]

Fix indentation → Validate again → Success.

Lesson:
Indentation is everything in YAML.

---

# 🔹 Task 6: Spot the Difference

Correct Block:

[
name: devops
tools:
  - docker
  - kubernetes
]

Broken Block:

[
name: devops
tools:
- docker
  - kubernetes
]

Problem:

- docker is not properly indented under tools.

List items must align with consistent spacing.

---

# 📌 Important YAML Rules Summary

- Spaces only (never tabs)
- 2 spaces standard indentation
- Colon must have space after it
- YAML is case-sensitive
- true/false are booleans
- Indentation defines hierarchy

---

# 🧠 3 Key Things I Learned

1. YAML is completely indentation-driven.
2. Lists can be written in block or inline format.
3. Multi-line blocks behave differently using | and >.

---

# 📂 Files Created

- person.yaml
- server.yaml
- day-38-yaml.md

---

# 🚀 Final Outcome

Successfully:

- Wrote YAML manually
- Practiced nested objects
- Practiced list formats
- Used multi-line block styles
- Validated using YAML Lint
- Broke indentation and fixed errors

Now fully prepared to move into CI/CD pipeline YAML writing.

This was a strong foundational DevOps practice day.
