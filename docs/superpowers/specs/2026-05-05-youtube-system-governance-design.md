# YouTube System Governance Design

## Status
- Date: 2026-05-05
- Scope: content production, comment responses, channel operations
- Decision: tool-agnostic hybrid governance layer

## Goal
Create a small, durable system layer for this repository so any agent or human can work against the same operating rules without restructuring the existing YouTube knowledge and operations folders.

The design should:
- keep domain knowledge in its current home
- add a lightweight governance layer above it
- make task routing and memory updates predictable
- stay portable across Claude, Codex, or other future agents

## Current Context
The repository already contains meaningful operational memory in native locations:
- `youtube-content/` for production workflows, checklists, pipeline, and post-mortem style knowledge
- `youtube-responses/` for response handling and editorial rules
- `youtube-api/` and `data/` for operational execution artifacts
- a master vault outside the repo for deeper strategic and medical source material

This means the right move is not to rebuild the system from scratch. The right move is to add a governance layer that tells workers how to navigate the existing structure safely.

## Approaches Considered

### 1. Minimal root-only rules
Add only a single root rules file and keep everything else implicit.

Pros:
- fastest to add
- almost no structural change

Cons:
- task routing stays ambiguous
- memory discipline remains weak
- future agents still need repo-specific interpretation

### 2. Fully centralized system folder
Move operational knowledge into a brand-new central system directory.

Pros:
- maximum conceptual centralization
- easier to explain in one place

Cons:
- high migration cost
- breaks established file ownership boundaries
- increases risk of duplicated or stale knowledge

### 3. Hybrid governance layer
Keep current source folders intact and add a small `system/` layer that defines routing, workflows, and memory rules.

Pros:
- low-risk
- compatible with current repo shape
- clear source-of-truth boundaries
- portable across tools and agents

Cons:
- requires disciplined adherence to the governance files
- still depends on existing folder quality

## Recommended Approach
Use the hybrid governance layer.

This gives the repository a stable operating model without forcing migration of the current content, response, and operations knowledge. It also matches the user goal of staying tool-agnostic.

## Proposed Structure

```text
system/
├── README.md
├── source-map.md
├── workflows.md
└── memory-rules.md

OPERATING_RULES.md
```

## File Responsibilities

### `system/README.md`
Acts as the system entrypoint.

Contents:
- system purpose
- scope boundaries
- covered source folders
- mandatory read order before any task starts

### `system/source-map.md`
Defines which folders are authoritative for each task type.

Task classes:
- content
- response
- operations
- strategy

For each class, the document should specify:
- primary source
- secondary source
- typical outputs

### `system/workflows.md`
Defines the standard operating flow for each task class.

It should contain:
- content workflow
- response workflow
- operations workflow

Each workflow should describe:
- entry checks
- source reading order
- expected outputs
- safety/compliance checks
- when memory updates are required

### `system/memory-rules.md`
Defines how durable knowledge is maintained.

It should distinguish:
- canonical memory
- working memory
- master vs mirror
- update thresholds
- forbidden memory behaviors

This is the main guardrail against noisy or inconsistent long-term updates.

### `OPERATING_RULES.md`
A tool-agnostic root-level contract.

This file should:
- direct any worker to the `system/` files first
- require task classification before action
- enforce source discipline
- constrain when persistent memory can be updated
- define escalation conditions

## Task Model

### Content Task
Purpose:
- produce or refine content assets for planned or active videos

Expected outputs:
- script or outline
- titles
- description pack
- thumbnail brief
- publish checklist
- post-mortem update when relevant

Primary source:
- `youtube-content/`

Secondary source:
- master vault

### Response Task
Purpose:
- produce safe, on-brand replies to audience comments

Expected outputs:
- response draft
- risk note when needed
- escalation suggestion when needed

Primary source:
- `youtube-responses/`

Secondary source:
- master vault
- `youtube-content/` when video context matters

### Operations Task
Purpose:
- manage channel mechanics and repeatable channel maintenance actions

Expected outputs:
- ops plan
- execution checklist
- verification note
- operational memory update when reusable

Primary source:
- `youtube-api/`
- `data/`
- `youtube-content/`

## Data Flow
The system should work like this:

1. A task begins.
2. The worker classifies it as content, response, operations, or strategy.
3. The worker reads `OPERATING_RULES.md`.
4. The worker consults `system/source-map.md`.
5. The worker follows the matching flow in `system/workflows.md`.
6. The worker completes the task.
7. The worker checks `system/memory-rules.md` to decide whether a reusable update belongs in canonical memory, working memory, or nowhere.

This keeps the execution path stable even when the agent layer changes.

## Error Handling and Escalation
The system must escalate instead of guessing when:
- there is medical or compliance ambiguity
- the correct source of truth is unclear
- a live channel operation could have destructive effects
- an operational mirror conflicts with a master source

In those cases, the worker should record the uncertainty, avoid irreversible changes, and request confirmation.

## Testing and Validation
This design does not require code tests first. It requires workflow validation.

Validation checklist:
- a new worker can identify the correct source set for a content task
- a new worker can identify the correct source set for a response task
- a new worker can identify the correct source set for an operations task
- memory updates can be categorized consistently
- the governance files do not duplicate domain content

Once implemented, a simple manual test should be run against one example of each task type.

## Non-Goals
This design does not:
- migrate master vault knowledge into the repo
- replace `youtube-content/` or `youtube-responses/`
- create a large multi-agent orchestration layer
- define automation commands yet

Those can come later, after the governance layer proves stable.

## Implementation Notes
The first implementation should stay intentionally small:
- create the five governance files
- keep them concise
- avoid premature templates unless repetition appears

Optional later additions:
- `system/templates/content-task.md`
- `system/templates/response-task.md`
- `system/templates/ops-task.md`

## Decision Summary
Adopt a hybrid governance layer that preserves current domain folders and adds a compact `system/` directory plus a root `OPERATING_RULES.md` contract.

This gives the repository:
- stronger consistency
- lower ambiguity
- safer memory updates
- future portability across tools
