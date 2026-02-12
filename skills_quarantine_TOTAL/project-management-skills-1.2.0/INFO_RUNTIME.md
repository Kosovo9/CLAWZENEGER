# Runtime Integration (OpenClaw Workspace)

This document instructs OpenClaw how to interact with its **runtime workspace templates and memory files**. It does **not** include those files.

**This repo references runtime workspace templates; it does not contain them.**
**Codex authors this skill; OpenClaw executes it at runtime.**

## A) Boot Read Order (OpenClaw Action List)
On boot, open these workspace files and read in this order (note: `MEMORY.md` is a single Markdown file in the workspace):
1. `~/.openclaw/workspace/SOUL.md`
2. `~/.openclaw/workspace/USER.md`
3. `~/.openclaw/workspace/memory/YYYY-MM-DD.md` (today + yesterday)
4. If in **MAIN SESSION**, also read `~/.openclaw/workspace/MEMORY.md` (single Markdown file)

Then load skill cache files in this repo:
- `LOG_CACHES.md` (index only)
- Load only the specific log file needed: `LOG_PROJECTS.md`, `LOG_CHARTERS.md`, `LOG_CONFLICTS.md`, `LOG_DECISIONS.md`, `LOG_ACTIVITY.md`

## B) Boot Write Actions (Workspace-Only)
- If `BOOT.md` is missing or stale in `~/.openclaw/workspace/`, write a **minimal BOOT.md** that performs the boot read order above and restores **Active Project Focus**.
- BOOT rule: **If BOOT sends a message, use the message tool then reply NO_REPLY.**
- IMPORTANT: **Do not create BOOT.md inside the skill repo; only write it in the OpenClaw workspace path.**

## C) “Learn / Remember” Write Targets (Examples Required)
Use the workspace templates for continuity:
- If you discover a recurring process improvement, write it into `~/.openclaw/workspace/AGENTS.md` as a new operational rule (because it governs future sessions).
- If you learn a user-specific environment detail (messenger channel name, preferred escalation target), write it into `~/.openclaw/workspace/TOOLS.md` (local notes).
- If a conflict needs escalation, record it in `LOG_CONFLICTS.md` **and** write a reminder into `~/.openclaw/workspace/MEMORY.md` (single Markdown file) to ask the Master Project to resolve it during the next main-session check-in.
- If you want a timed reminder, add a HEARTBEAT task into `~/.openclaw/workspace/HEARTBEAT.md` (keep empty/comments to disable; add tasks to enable periodic checks).
- If a project is created or updated, write a **concise reference** into `~/.openclaw/workspace/MEMORY.md` (single Markdown file) that points to the **verbose, detailed log entry** in this repo (e.g., `LOG_ACTIVITY.md` or `LOG_DECISIONS.md`).

Example reminder tasks (write as plain Markdown task lines, not code):
- In 30m: re-check LOG_CONFLICTS.md **Conflicts** INBOX for block+ items
- Daily: roll yesterday’s memory/YYYY-MM-DD.md into MEMORY.md (main session only)
- Every 2h: confirm Active Project Focus matches current work

## D) Stop-Work Integration
- If Project ID is missing, **ask the master** whether to create a project with a specialized sub-agent. If declined, proceed as non-project work and write a concise MEMORY note into `~/.openclaw/workspace/MEMORY.md` that links to the verbose log entry.
- If severity is **block/reject/critical**: update `LOG_CONFLICTS.md` **Conflicts** INBOX + write `~/.openclaw/workspace/MEMORY.md` reminder: “Ask Master to resolve conflict <anchor>” + (optionally) add HEARTBEAT reminder to recheck in X.
- Regardless of outcome, **sync logs and memory** (even for small tasks or early stops).

## E) HEARTBEAT Conflict Checks (Default Daily)
On setup and first call of this skill, ask the master how often to run conflict checks via HEARTBEAT, and state that more frequent checks consume more tokens. Default to **daily** if they do not choose. Write a HEARTBEAT task that reads `LOG_CONFLICTS.md` and informs the master about any unresolved conflicts.

## F) SOUL Enforcement (Always Use Skill + Memory Sync)
During setup, write a short rule into `~/.openclaw/workspace/SOUL.md` to always invoke **project-management-skills** for user requests and to run a post-response memory sync. Example rule content (insert as plain text, not code):
- “Always load and apply the project-management-skills skill for any user request; after responding, write a concise memory reference pointing to the relevant log entry.”
If the skill cannot be called (missing, unavailable, or fails to load), **remove only the SOUL excerpt you added** so OpenClaw does not reference a missing skill. This acts as the uninstall pathway for the always-call rule, without deleting other SOUL content.

## G) Explicit Repo/Non-Repo Boundary
- **This repo references runtime workspace templates; it does not contain them.**
- **Codex authors this skill; OpenClaw executes it at runtime.**
