# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an agentic-chat project focused on creating educational materials for the "How to Build ChatGPT" series from AI Makerspace. The project uses Python and YAML task definitions to generate comprehensive study guides and code walkthroughs.

## Expected Outcomes

- **Study Guide Research** → write to `./outputs/documents/study_guide.md` with sections: Overview & Learning Path, Part 1 — Prompting & Responses API, Part 2 — RAG & Connectors, Part 3 — Agentic Search & Agents SDK, Part 4 — Vibe-Coding & Deployment, Next Steps (Evaluation, Observability, Cost/Performance)
- **Code Walkthrough & Commentary** → write to `./outputs/documents/code_walkthrough.md` with sections: Architecture at a Glance, Part 1 — Prompting & Responses API, Part 2 — RAG & Connectors, Part 3 — Agentic Search & Agents SDK, Part 4 — Frontend & Deployment, Gaps & Enhancements

## Inputs to Use

**Videos**:
- playlist: https://www.youtube.com/playlist?list=PLrSHiQgy4VjG1B5TXPn99eKf52zSnEUZz
- part1: https://www.youtube.com/live/OkqnAk1eH4M?si=9XJ0KcqMjR2ft6Fo
- part2: https://www.youtube.com/live/BAtY88cw3rw?si=YBen_HcAfx89s3aE
- part3: https://www.youtube.com/live/qQ6nCN6ynXo
- part4: https://www.youtube.com/watch?v=t13Y5Igh66U

**Code Repos**:
- main: https://github.com/AI-Maker-Space/How-to-Build-ChatGPT
- branch[0]: https://github.com/AI-Maker-Space/How-to-Build-ChatGPT/tree/feature/agents-sdk-research-agent
- branch[1]: https://github.com/AI-Maker-Space/How-to-Build-ChatGPT/tree/feat/chatgpt-frontend

## Guardrails (Must Follow)

- Cite every non-obvious claim to the series videos or specific repo files/lines.
- Prefer minimal, runnable code fragments; avoid long monoliths.
- Flag gaps explicitly; do not fabricate paths/APIs.

---

## Procedure: Study Guide Research (`build-chatgpt-study-guide`)

**Role:** Expert AI curriculum designer

### Steps

1. **Gather Sources**
   - Collect **videos**:
     - https://www.youtube.com/playlist?list=PLrSHiQgy4VjG1B5TXPn99eKf52zSnEUZz
     - https://www.youtube.com/live/OkqnAk1eH4M?si=9XJ0KcqMjR2ft6Fo
     - https://www.youtube.com/live/BAtY88cw3rw?si=YBen_HcAfx89s3aE
     - https://www.youtube.com/live/qQ6nCN6ynXo
     - https://www.youtube.com/live/t13Y5Igh66U?si=fZSLA-Ty8hP4ugd6
   - Collect **code**:
     - https://github.com/AI-Maker-Space/How-to-Build-ChatGPT
     - https://github.com/AI-Maker-Space/How-to-Build-ChatGPT/tree/feature/agents-sdk-research-agent
     - https://github.com/AI-Maker-Space/How-to-Build-ChatGPT/tree/feat/chatgpt-frontend
   - companion: Uploaded expert study guide (local).
2. **Plan the Draft**
   - Create an outline matching the required **Sections**.
   - Identify where each **Diagram** fits.
3. **Write & Cite**
   - Write concise, technically accurate content. Minimize boilerplate.
   - Cite non-obvious claims to the appropriate video timestamps or repo files/lines.
4. **Produce Diagrams**
   - Generate the following Mermaid diagrams (one file per item):
     - `outputs/diagrams/study_guide_concept.md` — **Study Guide Concept Map** (id: `study-guide-map`)
   - Use Mermaid code blocks (```mermaid ... ```).
   - Ensure these files exist and are checked-in:
     - `outputs/diagrams/study_guide_concept.md`
5. **Assemble Deliverable**
   - Write the final Markdown to `./outputs/documents/study_guide.md` with the specified **Sections** in order.
6. **Quality Pass**
   - Verify links open, code blocks run (if applicable), and diagrams render.
   - Confirm adherence to Guardrails and flag any gaps.

---

## Procedure: Code Walkthrough & Commentary (`build-chatgpt-code-walkthrough`)

**Role:** Senior AI engineer -> code reviewer

### Steps

1. **Gather Sources**
   - Collect **repos**:
     - https://github.com/AI-Maker-Space/How-to-Build-ChatGPT
     - https://github.com/AI-Maker-Space/How-to-Build-ChatGPT/tree/feature/agents-sdk-research-agent
     - https://github.com/AI-Maker-Space/How-to-Build-ChatGPT/tree/feat/chatgpt-frontend
   - Collect **videos**:
     - https://www.youtube.com/live/OkqnAk1eH4M?si=9XJ0KcqMjR2ft6Fo
     - https://www.youtube.com/live/BAtY88cw3rw?si=YBen_HcAfx89s3aE
     - https://www.youtube.com/live/qQ6nCN6ynXo
     - https://www.youtube.com/live/t13Y5Igh66U?si=fZSLA-Ty8hP4ugd6
2. **Plan the Draft**
   - Create an outline matching the required **Sections**.
   - Identify where each **Diagram** fits.
3. **Write & Cite**
   - Write concise, technically accurate content. Minimize boilerplate.
   - Cite non-obvious claims to the appropriate video timestamps or repo files/lines.
4. **Produce Diagrams**
   - Generate the following Mermaid diagrams (one file per item):
     - `outputs/diagrams/code_walkthrough_arch.md` — **Repo Architecture (Code Walkthrough)** (id: `code-walkthrough-arch`)
     - `outputs/diagrams/runner_tasks.md` — **Runner → Tasks → Outputs** (id: `runner-tasks`)
     - `outputs/diagrams/e2e_sequence.md` — **End-to-End Sequence** (id: `e2e-sequence`)
   - Use Mermaid code blocks (```mermaid ... ```).
   - Ensure these files exist and are checked-in:
     - `outputs/diagrams/code_walkthrough_arch.md`
     - `outputs/diagrams/runner_tasks.md`
     - `outputs/diagrams/e2e_sequence.md`
5. **Assemble Deliverable**
   - Write the final Markdown to `./outputs/documents/code_walkthrough.md` with the specified **Sections** in order.
6. **Quality Pass**
   - Verify links open, code blocks run (if applicable), and diagrams render.
   - Confirm adherence to Guardrails and flag any gaps.

---

## Common Development Commands

### Environment Setup
```bash
# Set up development environment
make setup              # Creates virtual environment using uv
make install           # Installs package in development mode

# Manual setup (if make unavailable)
uv venv
source .venv/bin/activate  # Linux/Mac: .venv\Scripts\activate (Windows)
uv pip install -e .
```

### Content Validation
```bash
make check             # Run quality checks on generated content
make docs              # Validate documentation and required files
make transcripts       # Download video transcripts using yt-dlp

# Manual validation commands
wc -l outputs/documents/* outputs/diagrams/*
grep -c "\*(\[Part" outputs/documents/study_guide.md outputs/documents/code_walkthrough.md
```

### Development Workflow
```bash
make lint              # Run ruff linting (optional - requires ruff)
make format            # Run black formatting (optional - requires black)
make clean             # Clean temporary files and caches
make ci                # Run full CI checks (docs + check)
```

## Project Architecture

### Core Design Philosophy
This project is **AI-driven content generation** focused on producing educational materials from video sources. The architecture emphasizes:
- **Task-based execution**: YAML definitions drive content generation
- **Source integration**: Combines video transcripts + GitHub repos + MCP tools
- **Structured output**: Organized deliverables in `outputs/` with proper citations
- **Reproducibility**: Clear procedures for regenerating content

### Task Definition System (`ai-tasks.yaml`)
Central configuration defining two main tasks:
1. **build-chatgpt-study-guide**: Expert AI curriculum designer role
2. **build-chatgpt-code-walkthrough**: Senior AI engineer → code reviewer role

Each task specifies inputs (video URLs, GitHub repos), deliverables (markdown sections), diagrams (Mermaid), and quality guardrails.

### Content Generation Workflow
1. **Source Gathering**: MCP tools access YouTube transcripts + GitHub repositories
2. **Analysis**: AI processes videos/code with specific roles and expertise
3. **Structured Output**: Generated content follows defined sections and citation requirements
4. **Validation**: Quality checks ensure completeness and accuracy

### MCP Integration Architecture
- **Primary**: `mcp__youtube-transcripts__download_youtube_url` for video content
- **Fallback**: Local VTT files in `transcripts/` directory
- **GitHub Access**: Repository analysis through MCP GitHub tools
- **Content Processing**: Insights integrated with proper video timestamp citations

### Generated Deliverables Structure
```
outputs/
├── documents/              # Main deliverables
│   ├── study_guide.md          # Complete study guide (464 lines)
│   └── code_walkthrough.md     # Technical analysis (497 lines)
├── diagrams/               # Mermaid diagrams
│   ├── study_guide_concept.md  # Study guide concept map
│   ├── code_walkthrough_arch.md # Repository architecture
│   ├── runner_tasks.md         # Runner workflow diagram
│   └── e2e_sequence.md         # End-to-end sequence diagram
└── documentation/          # Supporting documentation
    └── mcp-setup.md            # MCP configuration guide

transcripts/                # Local backup transcripts (gitignored)
├── part1_OkqnAk1eH4M.en.vtt  # Part 1 video transcript (VTT format)
├── part2_BAtY88cw3rw.en.vtt  # Part 2 video transcript (VTT format)
└── part3_qQ6nCN6ynXo.en.vtt  # Part 3 video transcript (VTT format)
```

### Key Implementation Details
- **Task Execution**: Follow procedures in CLAUDE.md sections, not scripted automation
- **Citation Requirements**: Every non-obvious claim must link to video timestamps or repo files/lines
- **Diagram Generation**: Mermaid diagrams created as separate files in `outputs/diagrams/`
- **Content Quality**: Minimal runnable code fragments, explicit gap identification
- **Source Attribution**: Comprehensive citations maintaining academic standards

## Ready‑Made Prompts for Claude

### Study Guide Research

```
You are an **Expert AI curriculum designer**. Execute task **Study Guide Research** (`build-chatgpt-study-guide`).
Follow the Guardrails strictly. Cite non-obvious claims to specific video timestamps or repo files/lines.
Produce `./outputs/documents/study_guide.md` in Markdown with these sections:
- Overview & Learning Path
- Part 1 — Prompting & Responses API
- Part 2 — RAG & Connectors
- Part 3 — Agentic Search & Agents SDK
- Part 4 — Vibe-Coding & Deployment
- Next Steps (Evaluation, Observability, Cost/Performance)
Create Mermaid diagrams as separate files:
- outputs/diagrams/study_guide_concept.md: Study Guide Concept Map (id: study-guide-map)
If a required asset is missing, create a stub with TODOs and list the gap in a 'Gaps' section.
```

### Code Walkthrough & Commentary

```
You are a **Senior AI engineer -> code reviewer**. Execute task **Code Walkthrough & Commentary** (`build-chatgpt-code-walkthrough`).
Follow the Guardrails strictly. Cite non-obvious claims to specific video timestamps or repo files/lines.
Produce `./outputs/documents/code_walkthrough.md` in Markdown with these sections:
- Architecture at a Glance
- Part 1 — Prompting & Responses API
- Part 2 — RAG & Connectors
- Part 3 — Agentic Search & Agents SDK
- Part 4 — Frontend & Deployment
- Gaps & Enhancements
Create Mermaid diagrams as separate files:
- outputs/diagrams/code_walkthrough_arch.md: Repo Architecture (Code Walkthrough) (id: code-walkthrough-arch)
- outputs/diagrams/runner_tasks.md: Runner → Tasks → Outputs (id: runner-tasks)
- outputs/diagrams/e2e_sequence.md: End-to-End Sequence (id: e2e-sequence)
If a required asset is missing, create a stub with TODOs and list the gap in a 'Gaps' section.
```
