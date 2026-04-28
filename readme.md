

# Trainbase

**Trainbase turns a GitHub repo or local folder into an interactive course inside Colab/Jupyter.**

Trainbase is a lightweight Python library for building markdown-first interactive learning experiences. Course authors write lessons as Markdown files, embed videos, quizzes, and reflection prompts, then learners run the course inside a notebook.

```python
!pip install trainbase

from trainbase import learn

course = learn("https://github.com/yourname/startup-course")

course.agenda
course.play("chapter1")
course.progress()
course.certificate("Your Name")
```

## Why Trainbase?

Most course platforms are heavy. Trainbase is designed for people who want:

- Markdown-based course content
- Interactive quizzes inside Jupyter/Colab
- GitHub-based course distribution
- Lightweight progress tracking
- Simple completion certificates
- No LMS setup

Trainbase is not designed to be a secure exam system. It is designed for self-paced learners who want structure, interactivity, and feedback.

---

## Installation

```bash
pip install trainbase
```

For local development:

```bash
git clone https://github.com/YOUR_USERNAME/trainbase.git
cd trainbase
pip install -e .
```

---

## Quick Start

```python
from trainbase import learn

course = learn("https://github.com/yourname/startup-course")

course.agenda
```

Start a chapter:

```python
course.play("chapter1")
```

Show progress:

```python
course.progress()
```

Generate a completion certificate:

```python
course.certificate("Your Name")
```

---

## Course Repository Structure

A Trainbase course is just a folder or Git repo.

```text
startup-course/
├── course.yaml
├── chapter1/
│   └── README.md
├── chapter2/
│   └── README.md
└── assets/
    └── image.png
```

---

## `course.yaml`

Every course needs a `course.yaml` file at the root.

```yaml
id: startup_foundations
title: Startup Foundations
description: Learn startup basics through videos, quizzes, and reflections.
version: 0.1

chapters:
  - id: chapter1
    title: Founder Sales
    description: Learn why founders should talk to customers directly.
    path: chapter1/README.md

  - id: chapter2
    title: Startup Terms
    description: Learn key startup concepts and vocabulary.
    path: chapter2/README.md
    unlock_after:
      - chapter1
```

Each chapter has:

| Field | Required | Description |
|---|---:|---|
| `id` | Yes | Unique chapter ID used in `course.play("chapter1")` |
| `title` | Yes | Human-readable chapter title |
| `description` | No | One-line chapter description shown in the agenda |
| `path` | Yes | Path to the Markdown file |
| `unlock_after` | No | List of chapter IDs that must be completed first |

---

## Writing a Chapter

Each chapter is a Markdown file. You can write normal Markdown and add interactive blocks.

Example `chapter1/README.md`:

````markdown
# Chapter 1: Founder Sales

In early-stage startups, founders should talk directly to customers.

```video
url: https://youtu.be/DH7REvnQ1y4
```

## Key Idea

Founder-led sales helps the team learn what customers actually want.

```quiz
type: mcq
question: Why should founders do sales themselves early on?
options:
  - Because hiring salespeople is always illegal
  - Because founders need direct customer feedback
  - Because investors require it
answer: Because founders need direct customer feedback
points: 1
```

```reflect
question: In 3-5 sentences, explain how founder-led sales could help your own startup idea.
min_words: 25
points: 1
```
`````

---

## Supported Blocks

### 1. Video

````markdown
```video
url: https://youtu.be/DH7REvnQ1y4
````



Trainbase will render the video inside the notebook.

---

### 2. Multiple-choice Quiz

```markdown
```quiz
type: mcq
question: What is the main purpose of founder-led sales?
options:
  - To avoid talking to customers
  - To learn directly from customers
  - To replace product development
answer: To learn directly from customers
points: 1
````


The learner must answer correctly before moving forward.

---

### 3. Short Text Quiz

```markdown
```quiz
type: text
question: What keyword defines a function in Python?
answer: def
case_sensitive: false
points: 1
````

---

### 4. Reflection Prompt

```markdown
```reflect
question: Describe one thing you would test with customers this week.
min_words: 20
points: 1
````

Reflection prompts are checked by word count, not by correctness.

---

## Using a Local Course Folder

Trainbase can also load a course from your machine.

```python
from trainbase import learn

course = learn("D:/courses/startup-course")
````

On Mac/Linux/Colab:

```python
course = learn("/content/startup-course")
```

This is useful when developing a course before uploading it to GitHub.

---

## Using GitHub

For a public GitHub course repo:

```python
course = learn("https://github.com/yourname/startup-course")
```

Trainbase will read:

```text
https://raw.githubusercontent.com/yourname/startup-course/main/course.yaml
```

and then load chapter Markdown files from the same repo.

---

## GitLab and Internal Git

Trainbase aims to support GitLab and internal Git repositories.

Planned usage:

```python
course = learn("https://gitlab.company.com/team/startup-course")
```

For private GitLab repositories:

```python
course = learn(
    "https://gitlab.company.com/team/startup-course",
    token="YOUR_ACCESS_TOKEN"
)
```

GitLab support is planned after GitHub public and local folder support.

---

## Progress Tracking

Trainbase saves learner progress locally.

Default:

```text
trainbase_progress.json
```

You can customize the progress path:

```python
course = learn(
    "https://github.com/yourname/startup-course",
    progress_path="my_progress.json"
)
```

In Colab, you can save progress to Google Drive:

```python
course = learn(
    "https://github.com/yourname/startup-course",
    progress_path="/content/drive/MyDrive/trainbase_progress.json"
)
```

---

## Philosophy

Trainbase is intentionally lightweight.

It is for:

* self-paced learning
* workshops
* founder training
* internal bootcamps
* classroom demos
* AI-generated learning modules

It is not for:

* secure exams
* anti-cheating systems
* high-stakes certification
* full LMS replacement

---

## Development Roadmap

### v0.1

* Load course from public GitHub repo
* Load course from local folder
* Render Markdown
* Render YouTube videos
* Render multiple-choice quiz
* Render text quiz
* Render reflection prompts
* Save local progress
* Generate simple certificate

### v0.2

* GitLab support
* Private repo token support
* Google Drive progress helper
* Score summary
* Better agenda UI
* Multiple-answer quiz

### v0.3

* PDF block
* Code exercise block
* Image/audio blocks
* Export certificate as HTML/PDF

---

## License

MIT License.

````

---
