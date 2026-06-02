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
| **"Channel hallucination"** | Designed a delivery path through a channel where the receiving end lacks the required tools | CC-0 (design phase) |
| **"Vague evidence"** | "Looks good", "Should be fine", "I think it works" | L2 evidence requirement |

---

## CADVP — Cross-Agent Delivery Verification Protocol (v1.1)

> *Born from a production incident where a coordinator agent injected knowledge into a sub-agent, verified the write side, but never checked whether the delivery channel was functional. The data existed — but the sub-agent could never read it.*

CADVP is a **supplementary protocol** for cross-agent delivery scenarios: when Agent A writes data/knowledge that Agent B needs to read, CADVP verifies the entire chain — write layer, data layer, read layer, and **channel layer**.

### Core Insight: Four-Layer Separation

| Layer | Question | Verification Focus |
|-------|----------|-------------------|
| **Write Layer** | What operation did I perform? | Was the operation executed correctly? |
| **Data Layer** | Where does the data live? | Does the data exist in the storage medium? |
| **Read Layer** | Where does the target agent read from? | Config activated? Runtime loaded? Tool reachable? User perceivable? |
| **Channel Layer ★** | What channel carries data from "me" to "it"? | Is the channel functional at the receiving end? |

### Golden Rules

1. **Inverse Verification Principle:** Ask what the receiver's read path is first, then verify data has arrived there. Never reason forward from the write side.
2. **Channel Matching Principle:** What channel carries the data? Is that channel available at the target end? Never design a flow on an unavailable channel.

### CC-0 — Channel Confirmation (v1.1 Veto-Level Check)

Before writing any code or prompt for cross-agent delivery, draw the full data path:

```
Data source → [channel] → Target agent's read mechanism
```

Mark each hop's tool/permission/environment availability. If any hop's tool is unavailable, **block immediately** — do not proceed.

**Practical exercise:** Before injecting knowledge into a sub-agent, write down:
1. Where is the data coming from?
2. What channel carries it? (direct DB write / target self-write / cron delegate)
3. What tool does the target use to read it?
4. Is that tool available in the target's environment?

If question 4 is "no", the delivery will fail regardless of how correct the write side is.

### Channel Comparison Table

| Channel | Method | Reliability | Notes |
|---------|--------|-------------|-------|
| **A. Direct DB Write** | Coordinator writes directly to target's `memory_store.db` via SQLite INSERT | ✅ **Highest** | Data arrives directly, bypasses target agent's tool constraints. Best for batch injection. |
| **B. Target Self-Write** | Target agent uses its own `memory()` tool within its session | ✅ **Reliable** | Requires target profile to have memory system enabled. Each session writes independently. |
| **❌ C. Cron Delegate** | Coordinator creates a cron job under target profile to run memory/fact_store writes | ❌ **Not Viable** | Cron leaf agents do not have `memory` or `fact_store` tools. This path is always broken. |

### CADVP 13-Dimension Verification Checklist (v1.1)

#### Channel Confirmation (CC) ← v1.1 addition, highest priority

| # | Code | Name | Severity | Method | Block Criterion |
|---|------|------|----------|--------|----------------|
| 0 | **CC-0** | **Channel Confirmation** | 🔴 Critical | Map full data path A→B, check tool/permission/env at each hop | Any hop's tool unavailable → block |

#### Prerequisite Checks (PC — 3 items)

| # | Code | Name | Severity | Method |
|---|------|------|----------|--------|
| 1 | PC-1 | Target Identity Confirmation | 🔴 Critical | ls + ps + cat config |
| 2 | PC-2 | Data Channel Mapping | 🔴 Critical | Read target config + DB existence |
| 3 | PC-3 | Impact Assessment | 🟠 High | Enumerate profiles |

#### Write-side Verification (WV — 3 items)

| # | Code | Name | Severity | Method |
|---|------|------|----------|--------|
| 4 | WV-1 | Data Write Confirmation | 🟢 Routine | ls/sqlite/read_file |
| 5 | WV-2 | Content Integrity | 🟢 Routine | cat/grep/verify |
| 6 | WV-3 | Write Permissions | 🟠 High | ls -l / sqlite connection |

#### Read-side Verification (RV — 4 items) ← Core

| # | Code | Name | Severity | Method |
|---|------|------|----------|--------|
| 7 | **RV-1** | **Config Activation Check** | 🔴 Critical | Read target config.yaml memory section |
| 8 | **RV-2** | **Runtime Load Verification** | 🔴 Critical | Check memory_store.db facts table |
| 9 | **RV-3** | **Tool Reachability Verification** | 🔴 Critical | Check memory status + FTS verification |
| 10 | **RV-4** | **User Perception Verification** | 🔴 Critical | Send test query |

#### Global Regression (GR — 2 items)

| # | Code | Name | Severity | Method |
|---|------|------|----------|--------|
| 11 | GR-1 | Dependency Impact Check | 🟠 High | diff comparison |
| 12 | GR-2 | Documentation & Notification | 🟢 Routine | Triple check |

### Channel Decision Tree

```
Inject data into sub-agent →
  ├─ Target has holographic memory configured? ─No→ Configure config.yaml first
  │                                                    ↓
  │                                             Restart gateway
  │                                                    ↓
  └─ Target memory system ready →
       ├─ Small data (<100 records) → Channel A: Direct DB write (SQLite INSERT)
       ├─ Needs periodic updates   → Channel A: Coordinator cronjob writes DB directly (not via delegate agent)
       └─ Runtime dynamic inject   → Channel A or B, NEVER Channel C
```

### Automated Verification Script

```bash
# Usage
python3 scripts/cadvp-verify.py <target_profile>

# Example: verify a sub-agent's memory channel
python3 scripts/cadvp-verify.py assistant-profile
```

The script outputs a formatted JSON report with PASS/FAIL for each dimension, detailed evidence, and delivery decision recommendation.

### Enhanced L1 Gate for Cross-Agent Scenarios

The original L1-3 "Can the target access it?" is expanded for cross-agent scenarios:

```
□ 3a. Read from the target profile's path (file level)
   → cat / grep files in target directory

□ 3b. What is the target agent's runtime read channel?
   → Check config.yaml memory section

□ 3c. Does the data exist in the target's storage medium?
   → Check memory_store.db facts table

□ 3d. What channel carries the data? Is that channel's tool available at the target?
   → Map the full path. If via cron delegate, confirm leaf agent has memory/fact_store tools
   → Answer: Channel __available / unavailable__

□ 3e. Is the target gateway online?
   → Check gateway.pid / ps
```

### Application Scenarios

- **Knowledge injection verification:** After injecting business knowledge into an agent, confirm Channel A (direct DB write) was used, verify all layers with CADVP
- **Config change verification:** After modifying agent config, check config→load→tool→perception chain
- **Multi-agent consistency:** After deploying N identical agents, configure holographic for all, then write DB per profile
- **Pre-launch gate:** Mandatory gate before delivery — CC-0 is a veto item
- **Incident root cause:** When agent behavior is abnormal, locate the broken layer (channel/config/storage/tool)
