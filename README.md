# Agent Quality Gate Protocol 🚧✅

**A three-level completion verification framework for AI agents — now with CADVP v1.1 cross-agent delivery verification.**

Every agent says "done" — but is it really done? The Agent Quality Gate Protocol defines a repeatable, auditable process for agents to self-verify before reporting completion.

```
L1 Self-Verify → L2 Produce Evidence → L3 Independent Review
```

## What's New in v1.1

- **CC-0 Channel Confirmation** — a veto-level zero-check that validates the data transfer channel before any cross-agent delivery begins. If the channel is unreliable, the delivery is blocked immediately.
- **13-Dimension Verification** — expanded from 12 to 13 dimensions with the addition of CC-0 (Channel Confirmation).
- **Channel Decision Tree** — three delivery paths evaluated: direct DB write ✅, target self-write ✅, cron delegate ❌.
- **Inverse Verification Principle** — verify from the receiver's read path, not the sender's write path.

## Why?

AI agents routinely:
- Claim a file was written when it was truncated
- Claim a config was updated when the patch missed its target
- Modify one profile but forget the other four
- Report "done" without checking if the change is actually visible to the target system
- Design a delivery path through a channel that doesn't have the required tools at the receiving end

This protocol catches those gaps before they reach the user.

## Quick Start

### As a Hermes Agent Skill

```yaml
# In config.yaml delegation or skill list
- name: agent-quality-gate
```

Then load it when completing a task:

```
Load skill: agent-quality-gate
```

### As a SOUL.md Template

Copy `integrations/hermes-soul.md` into your agent's SOUL.md as a permanent L1-level rule.

### As a Standalone Script

```bash
# Quick file verification
./scripts/self-verify.sh /path/to/file "expected_keyword"

# Generate an evidence report
./scripts/generate-evidence.sh "Updated configuration" config-modify /path/to/config.yaml

# Cross-agent delivery verification (CADVP — 13 dimensions)
python3 scripts/cadvp-verify.py <target_profile>
```

## Contents

| Path | Description |
|------|-------------|
| `protocol/` | Full specification of the three-level gate + CADVP v1.1 |
| `scripts/` | Self-verify, evidence-generation, and CADVP verification scripts |
| `templates/` | Completion checklist, evidence report, review assignment |
| `integrations/` | How to embed into Hermes SOUL.md or as a skill |
| `examples/` | Step-by-step usage scenarios |

## CADVP — Cross-Agent Delivery Verification Protocol

CADVP is a supplementary protocol for cross-agent delivery scenarios. When Agent A injects knowledge or data into Agent B, CADVP verifies the entire delivery chain — not just the write side, but the read side, the channel, and the end-user perception.

**Key insight:** "I wrote it" ≠ "They can read it." The delivery channel must be verified independently.

See `protocol/index.md` for the full CADVP specification including the 13-dimension checklist and channel decision tree.

## Related Publication

A detailed paper describing the CADVP methodology, its theoretical foundations, and case studies from production multi-agent deployments is currently in preparation.

> **Status:** Pre-print forthcoming on ArXiv.  
> **Working title:** *"Cross-Agent Delivery Verification: A Channel-Aware Protocol for Knowledge Injection in Multi-Agent Systems"*  
> **Expected availability:** 2025

Watch this repository for updates.

## License

MIT
