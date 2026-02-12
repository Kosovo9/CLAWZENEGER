---
name: project-management-skills
description: A governed project management OS for OpenClaw that applies to master prompts, supports optional project creation with sub-agents, and emphasizes memory-first continuity.
---

# Project Management Skills

## Trigger Conditions
Use this skill whenever:
- The request comes from the **master** and involves project work, planning, delivery, or changes that can impact scope, safety, or governance.
- The master asks to create or manage a project, or to evaluate whether a request should become a project.
- Conflicts, uncertainty, or policy violations are possible.
- You must coordinate memory/continuity across sessions.
- **Do not** apply this skill to proactive work the agent initiates; that work should proceed and be categorized afterward.

## Quickstart Checklist
1. Capture the request and **infer missing fields** from prior conversation context (only when evidence is clear).
2. **Clarify any inferred fields you are not confident in** before committing them or creating a project.
3. Ask the master if this should become a **project** (break into two questions; ask even for small tasks):
   - “Should I make and log this into a project to store it in my memory?”
   - “Should I execute this now, or spin up a specialized agent for higher-quality work (this will use more tokens)?”
4. If yes, auto-create a **Project ID** and start a **Charter Lite** in `LOG_CHARTERS.md`.
5. Load only the necessary log files: `LOG_PROJECTS.md`, `LOG_CHARTERS.md`, `LOG_CONFLICTS.md`, `LOG_DECISIONS.md`, `LOG_ACTIVITY.md`.
6. On setup and first call, ask how often to run **conflict checks** via HEARTBEAT (default **daily**); inform that more checks consume more tokens, then write the schedule into `~/.openclaw/workspace/HEARTBEAT.md`.
7. Run the **Conflict Detection Checklist**.
8. Proceed only if gates pass; otherwise log conflict and stop.
9. Execute the governed workflow in `INFO_GOVERNANCE.md` under **Governed Workflow**.
10. Log outcomes in `LOG_ACTIVITY.md`, decisions in `LOG_DECISIONS.md`.
11. **Always sync logs and memory** (even for small tasks or early stops).
12. Update runtime workspace files per `INFO_RUNTIME.md`.

## The 10 Setup Commandments (Stop-Work Rules)
**C1 Lock project isolation:** every unit of work belongs to exactly one Project ID **or** is explicitly logged as non-project work.
**C2 Master Project as OS/kernel governs all projects.**
**C3 Charter first:** no charter, no work.
**C4 Project optionality:** if the master did not request a project, ask whether this should become one; proceed without a Project ID only if the master declines, then log as non-project work.
**C5 Conflict detection:** run gates; conflicts can block.
**C6 Conflicts become logs:** every conflict is recorded.
**C7 Conflicts routed to messenger:** provide manual copy/paste payload.
**C8 Severity defined up front:** info, warn, block, reject, critical.
**C9 Kill fast-but-wrong:** if uncertain, add checks or record unknowns—never guess.
**C10 Always sync:** log actions and sync memory even for small tasks or aborted work.

## Core References
- Governance rules: [INFO_GOVERNANCE.md](INFO_GOVERNANCE.md)
- Runtime integration: [INFO_RUNTIME.md](INFO_RUNTIME.md)
- Research notes: [INFO_RESEARCH.md](INFO_RESEARCH.md)

## Safety & Trust Warning
Safety and correctness override speed. If uncertain, **stop**, document unknowns, and escalate or request clarification rather than guessing.
