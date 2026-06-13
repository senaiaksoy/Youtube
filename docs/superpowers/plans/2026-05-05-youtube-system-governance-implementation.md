# YouTube System Governance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a tool-agnostic governance layer to this repository by creating the `system/` directory and root `OPERATING_RULES.md` without restructuring the existing YouTube knowledge folders.

**Architecture:** The implementation keeps domain knowledge in `youtube-content/`, `youtube-responses/`, `youtube-api/`, and `data/`, then adds a thin governance layer above them. The new files act as routing and memory-control documents, not replacements for existing operational knowledge.

**Tech Stack:** Markdown, Git, PowerShell, existing repository documentation

---

## File Map

- Create: `D:/A-klasör/Youtube/system/README.md`
- Create: `D:/A-klasör/Youtube/system/source-map.md`
- Create: `D:/A-klasör/Youtube/system/workflows.md`
- Create: `D:/A-klasör/Youtube/system/memory-rules.md`
- Create: `D:/A-klasör/Youtube/OPERATING_RULES.md`
- Reference: `D:/A-klasör/Youtube/youtube-content/README.md`
- Reference: `D:/A-klasör/Youtube/youtube-content/09-production-pipeline.md`
- Reference: `D:/A-klasör/Youtube/youtube-responses/README.md`
- Reference: `D:/A-klasör/Youtube/docs/superpowers/specs/2026-05-05-youtube-system-governance-design.md`

### Task 1: Create The Governance Skeleton

**Files:**
- Create: `D:/A-klasör/Youtube/system/README.md`
- Create: `D:/A-klasör/Youtube/system/source-map.md`
- Create: `D:/A-klasör/Youtube/system/workflows.md`
- Create: `D:/A-klasör/Youtube/system/memory-rules.md`
- Create: `D:/A-klasör/Youtube/OPERATING_RULES.md`

- [ ] **Step 1: Verify the target paths do not already exist**

Run:

```powershell
Get-ChildItem 'D:\A-klasör\Youtube\system'
Get-Item 'D:\A-klasör\Youtube\OPERATING_RULES.md'
```

Expected:
- `system` may be missing
- `OPERATING_RULES.md` should be missing

- [ ] **Step 2: Create the `system/` directory**

Run:

```powershell
New-Item -ItemType Directory -Path 'D:\A-klasör\Youtube\system'
```

Expected:
- PowerShell reports the new directory was created

- [ ] **Step 3: Create `system/README.md` with the entrypoint contract**

Write this file content:

```md
# YouTube System

## Purpose
This directory defines the operating system for the YouTube workspace.
It is tool-agnostic and governs how any agent or human should navigate content production, response handling, and channel operations.

## Scope
This system covers:
- content planning and production
- comment response workflows
- channel operations and maintenance
- memory update rules

## Core Principle
Operational knowledge stays in its native folders.
This `system/` directory does not replace domain content.
It defines how to use it correctly.

## Covered Sources
- `youtube-content/`
- `youtube-responses/`
- `youtube-api/`
- `data/`
- master vault

## Working Rule
Before starting any task:
1. classify the task
2. read `source-map.md`
3. follow the matching workflow in `workflows.md`
4. update memory only through `memory-rules.md`
```

- [ ] **Step 4: Create `system/source-map.md` with source-of-truth routing**

Write this file content:

```md
# Source Map

## Content Tasks
Primary source:
- `youtube-content/`

Secondary source:
- master vault

Typical outputs:
- script package
- title options
- description package
- thumbnail brief
- publish checklist
- post-mortem update

## Response Tasks
Primary source:
- `youtube-responses/`

Secondary source:
- master vault
- `youtube-content/` when context from the video matters

Typical outputs:
- approved response draft
- risk note
- escalation suggestion

## Operations Tasks
Primary source:
- `youtube-api/`
- `data/`
- `youtube-content/`

Secondary source:
- channel audit notes
- master vault if strategic context is needed

Typical outputs:
- ops plan
- execution checklist
- verification summary
- memory update

## Strategy / Deep Knowledge
Primary source:
- master vault

Rule:
Do not treat operational mirrors as the final authority when a master source exists.
```

- [ ] **Step 5: Create `system/workflows.md` with task flows**

Write this file content:

```md
# Workflows

## Content Workflow
1. Confirm topic, channel, language, and audience.
2. Read relevant `youtube-content/` files.
3. Pull deeper medical or strategic context from master vault if needed.
4. Produce content assets:
   - hook direction
   - structure
   - script or outline
   - title set
   - description pack
   - thumbnail brief
5. Run compliance and tone checks.
6. If published, update the relevant production memory.

## Response Workflow
1. Classify the comment:
   - appreciation
   - clarification
   - medical-risk
   - hostile
   - conversion-oriented
2. Read response rules from `youtube-responses/`.
3. Bring in video context only if needed.
4. Draft a response aligned with brand voice and safety.
5. Flag comments that should not receive a normal reply.
6. If a repeated pattern appears, update reusable response memory.

## Operations Workflow
1. Identify the operation type:
   - metadata
   - homepage
   - playlists
   - pinned comments
   - audit
   - bulk update
2. Read the relevant operational notes and scripts.
3. Prefer reversible, verified actions.
4. Record what changed and how it was verified.
5. Update the relevant operational memory if the change matters for future sessions.
```

- [ ] **Step 6: Create `system/memory-rules.md` with durable memory rules**

Write this file content:

```md
# Memory Rules

## Memory Types

### Canonical Memory
Long-lived files that define reusable knowledge and workflow expectations.

Examples:
- `youtube-content/` operational references
- `youtube-responses/` response rules
- master vault knowledge pages

### Working Memory
Task-local notes, temporary exports, one-off summaries, and intermediate artifacts.

Examples:
- temporary analysis notes
- bulk audit scratchpads
- raw exports before synthesis

## Update Rules
Update canonical memory only when:
- the result is reusable
- the finding changes future behavior
- the pattern is likely to recur
- the update has been checked for correctness

Do not update canonical memory when:
- the result is one-off
- the finding is speculative
- the source is incomplete
- the information belongs in raw working notes

## Master vs Mirror
If a master source exists, preserve the distinction:
- master = long-term authority
- mirror = operational convenience
- system = governance and routing

Do not silently promote mirror content into strategy truth.

## Required End-of-Task Check
Before closing a task, ask:
- Did this produce reusable knowledge?
- If yes, where should it live?
- Is this a master update, mirror update, or no memory update?

## Forbidden Behaviors
- inventing source-backed claims without checking source files
- treating temporary notes as permanent guidance
- overwriting structured operational memory with raw dumps
- updating multiple memory layers without a clear reason
```

- [ ] **Step 7: Create `OPERATING_RULES.md` with the root-level contract**

Write this file content:

```md
# Operating Rules

## Start Here
Any human or agent working in this repository should begin by reading:
1. `system/README.md`
2. `system/source-map.md`
3. `system/workflows.md`
4. `system/memory-rules.md`

## Task Classification
Every task must be classified before work begins:
- content
- response
- operations
- strategy

## Source Discipline
Use the source map before reading broadly.
Prefer the smallest correct source set.

## Output Discipline
Every task should produce one of:
- content asset
- response draft
- operational change
- strategic note
- memory update

## Update Discipline
Only update reusable memory when the result is validated and worth carrying forward.

## Escalation
Escalate instead of guessing when:
- medical or compliance risk is present
- source authority is unclear
- action could affect live channel assets
```

- [ ] **Step 8: Review the created files in the terminal**

Run:

```powershell
Get-Content 'D:\A-klasör\Youtube\system\README.md'
Get-Content 'D:\A-klasör\Youtube\system\source-map.md'
Get-Content 'D:\A-klasör\Youtube\system\workflows.md'
Get-Content 'D:\A-klasör\Youtube\system\memory-rules.md'
Get-Content 'D:\A-klasör\Youtube\OPERATING_RULES.md'
```

Expected:
- each file exists
- headings render correctly
- no placeholder text remains

### Task 2: Validate Alignment With Existing Repo Memory

**Files:**
- Modify: `D:/A-klasör/Youtube/system/README.md`
- Modify: `D:/A-klasör/Youtube/system/source-map.md`
- Modify: `D:/A-klasör/Youtube/system/workflows.md`
- Modify: `D:/A-klasör/Youtube/system/memory-rules.md`
- Modify: `D:/A-klasör/Youtube/OPERATING_RULES.md`
- Reference: `D:/A-klasör/Youtube/youtube-content/README.md`
- Reference: `D:/A-klasör/Youtube/youtube-content/09-production-pipeline.md`
- Reference: `D:/A-klasör/Youtube/youtube-responses/README.md`

- [ ] **Step 1: Compare the new governance files against existing repo conventions**

Run:

```powershell
Get-Content 'D:\A-klasör\Youtube\youtube-content\README.md' -TotalCount 120
Get-Content 'D:\A-klasör\Youtube\youtube-content\09-production-pipeline.md' -TotalCount 120
Get-Content 'D:\A-klasör\Youtube\youtube-responses\README.md' -TotalCount 120
```

Expected:
- source folders confirm the governance files point at real operational domains

- [ ] **Step 2: Make any wording corrections needed to match the repo reality**

Allowed edits:
- add or remove one source folder reference
- tighten a workflow step
- clarify master vs mirror wording

Do not:
- introduce new task classes
- add automation commands
- duplicate domain content from source folders

- [ ] **Step 3: Run a final diff review scoped to the new governance layer**

Run:

```powershell
git diff -- system OPERATING_RULES.md docs/superpowers/specs/2026-05-05-youtube-system-governance-design.md docs/superpowers/plans/2026-05-05-youtube-system-governance-implementation.md
```

Expected:
- diff shows only the governance files and the two documentation files
- no unrelated repository files are changed

- [ ] **Step 4: Verify the implementation matches the approved spec**

Check:
- `system/` exists
- exactly four governance files exist under `system/`
- `OPERATING_RULES.md` exists at repo root
- task classes remain content, response, operations, strategy
- no operational source folders were moved or renamed

- [ ] **Step 5: Commit the governance layer**

Run:

```bash
git add system OPERATING_RULES.md docs/superpowers/specs/2026-05-05-youtube-system-governance-design.md docs/superpowers/plans/2026-05-05-youtube-system-governance-implementation.md
git commit -m "docs: add youtube system governance layer"
```

Expected:
- commit succeeds with only governance files staged

## Self-Review

### Spec coverage
- `system/` structure: covered by Task 1
- root contract file: covered by Task 1
- file responsibilities: covered by Task 1
- source-of-truth routing: covered by Task 1 and Task 2
- memory discipline: covered by Task 1 and Task 2
- no migration of existing folders: protected by Task 2

### Placeholder scan
No `TODO`, `TBD`, or deferred implementation placeholders are intentionally included in this plan.

### Type consistency
The plan consistently uses these task classes:
- content
- response
- operations
- strategy
