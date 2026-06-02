# Agent Quality Gate Protocol — Specification

## Overview

The Agent Quality Gate Protocol defines a **three-level mandatory verification sequence** that every AI agent must pass before reporting a task as "complete".

The gates are executed in order. No gate can be skipped. If a gate fails, the agent must fix the issue and restart from the failed gate.

### Core Principles

| Principle | Meaning |
|-----------|---------|
| **Done is verified, not felt** | Every completion requires objective evidence |
| **Evidence replaces promise** | Every operation must produce verifiable proof |
| **Review is not optional for risk** | Complex/high-risk tasks require independent verification |
| **Self-healing loop** | Gate failures trigger repair → re-verify → proceed |

---

## L1 — Self-Verification Gate (Mandatory)

### Purpose

Ensure the agent physically confirms that the intended operation actually happened.

### Checklist

Every agent must answer all 5 questions before proceeding:

```
□ 1. Does the file actually exist?
   → Verify with `ls`, `stat`, or `read_file`

□ 2. Is the content correct?
   → Verify with `grep`, `head`, or read-back
   → For config files: confirm specific field values
   → For code: run syntax check or tests

□ 3. Can the target system access it?
   → For cross-profile operations: read from the target profile's path
   → For cross-system operations: verify via target system's API or tool

□ 4. Does it need a restart/reload?
   → Config changes: check if service reload is required
   → Code changes: check if hot-reload is active
   → Always reload/restart if needed, then verify again

□ 5. Are there any missed dependencies?
   → Changed one profile → check all others
   → Changed one file → check files that reference it
   → Changed one config → check all dependent services
```

### Pass Condition

All 5 checks pass.

### Failure Recovery

If any check fails, fix the issue and re-run all 5 checks.

---

## L2 — Evidence Gate (Mandatory)

### Purpose

Produce objective, verifiable evidence for each operation. The agent must attach evidence to every "done" report.

### Evidence Requirements by Operation Type

| Operation Type | Required Evidence |
|----------------|------------------|
| File write | File existence + content snippet (head/grep output) |
| Config modification | Before/after diff (unified format) |
| File deletion | Pre-deletion confirmation + post-deletion verification |
| Code modification | Diff + syntax check + test results |
| API call | Request + response (sanitized) + HTTP status code |
| Data write | Write confirmation + read-back verification |
| Cross-system operation | Target system acknowledgment or receipt |
| Content publish | Published URL/ID or screenshot |

### Evidence Report

See `templates/evidence-report.md` for the standard report format.

### Pass Condition

Evidence report is produced and covers the operation type.

### Failure Recovery

If evidence is incomplete, re-verify the operation and produce a complete report.

---

## L3 — Independent Review Gate (Conditional)

### Purpose

Provide an independent perspective on high-risk or complex completions.

### When Review Is Required

- **High-risk operations**: config changes, system modifications, data migrations, permission changes
- **Cross-agent operations**: Agent A's output needs verification by Agent B
- **User-facing deliverables**: Final output needs a second pair of eyes
- **Cross-system operations**: Changes affecting systems outside the current scope

### Review Workflow

1. Task is completed with L2 evidence report
2. Assign a reviewer (another agent or separate session in the same profile)
3. Reviewer checks each verification point against the evidence
4. Reviewer marks: **Pass** / **Conditional Pass** / **Fail**
5. If Fail → fix → re-enter gate sequence → re-review

### Review Assignment

See `templates/review-assignment.md` for the standard assignment template.

### Pass Condition

Reviewer marks Pass or Conditional Pass (with conditions documented).

---

## Standard Execution Flow

```
┌─────────────────────────────────────┐
│         Task Complete?              │
└─────────────────────────────────────┘
                │ Yes
                ▼
┌─────────────────────────────────────┐
│  L1: Self-Verification Gate         │
│  ├─ File exists?                    │
│  ├─ Content correct?                │
│  ├─ Target can access?              │
│  ├─ Restart needed?                 │
│  └─ Missed dependencies?            │
└─────────────────────────────────────┘
         All 5 checks pass?
          Yes        No ──→ Fix ──→
                ▼
┌─────────────────────────────────────┐
│  L2: Evidence Gate                  │
│  ├─ Produce evidence report         │
│  └─ Attach to completion            │
└─────────────────────────────────────┘
         Evidence complete?
          Yes        No ──→ Fix ──→
                ▼
┌─────────────────────────────────────┐
│  L3: Independent Review Gate        │
│  (Only if high-risk/complex)        │
│  ├─ Assign reviewer                 │
│  └─ Get sign-off                    │
└─────────────────────────────────────┘
          Review pass?
          Yes        No ──→ Fix ──→
                ▼
┌─────────────────────────────────────┐
│         ✅ Report Done              │
│         (with evidence attached)    │
└─────────────────────────────────────┘
```

## Common Failure Modes

| Failure | Symptom | Gate That Catches It |
|---------|---------|---------------------|
| **"Thought I did it"** | patch command ran but string didn't match — nothing actually changed | L1-1 + L1-2 |
| **"Did it here, not there"** | Only modified one profile/system, forgot the others | L1-5 |
| **"Changed but didn't restart"** | Config file updated but service not reloaded — no effect | L1-4 |
| **"Target can't see it"** | Wrote file from current session's path, but target agent's path is different | L1-3 |
| **"Vague evidence"** | "Looks good", "Should be fine", "I think it works" | L2 evidence requirement |
