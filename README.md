# Agent Quality Gate Protocol 🚧✅

**A three-level completion verification framework for AI agents.**

Every agent says "done" — but is it really done? The Agent Quality Gate Protocol defines a repeatable, auditable process for agents to self-verify before reporting completion.

```
L1 Self-Verify → L2 Produce Evidence → L3 Independent Review
```

## Why?

AI agents routinely:
- Claim a file was written when it was truncated
- Claim a config was updated when the patch missed its target
- Modify one profile but forget the other four
- Report "done" without checking if the change is actually visible to the target system

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
```

## Contents

| Path | Description |
|------|-------------|
| `protocol/` | Full specification of the three-level gate |
| `scripts/` | Self-verify and evidence-generation scripts |
| `templates/` | Completion checklist, evidence report, review assignment |
| `integrations/` | How to embed into Hermes SOUL.md or as a skill |
| `examples/` | Step-by-step usage scenarios |

## License

MIT
