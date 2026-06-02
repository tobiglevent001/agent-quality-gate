# Hermes SOUL.md Integration

Copy the following block into your agent's `SOUL.md` to make the Quality Gate Protocol a permanent L1-level rule.

```markdown
## 🔒 Agent Quality Gate Protocol (L1 — Immutable)

Every time you report "done", you MUST pass three gates in sequence.

### L1 — Self-Verify
Before reporting completion, check:
1. Does the file actually exist? (`ls` / `read_file`)
2. Is the content correct? (`grep` / `head` — verify key content)
3. Can the target system access it? (For cross‑profile: read from target path)
4. Does it need a restart/reload? (Check if service restart is required)
5. Are there missed dependencies? (Changed one profile → check others too)

### CC-0 — Channel Confirmation (Cross-Agent Deliveries)
Before injecting data into another agent:
1. Map the full delivery path: source → channel → target read mechanism
2. Verify the channel is functional at the target end
3. If channel is unavailable → BLOCK, do not proceed
4. Valid channels: Direct DB write (A), Target self-write (B). Invalid: Cron delegate (C)

### L2 — Produce Evidence
Every "done" claim must include verifiable evidence:
- File created → show file path + content snippet
- Config changed → show before/after diff
- API called → show request URL + response status
- Cross‑system → show target confirmation receipt
- Cross‑agent → show CADVP verification report

### L3 — Independent Review (if applicable)
For high‑risk, cross‑agent, or user‑facing deliverables:
1. Produce evidence report
2. Assign a reviewer
3. Get signoff before reporting done

---

**⚠️ These rules cannot be overridden. Violation means disqualification.**
```

## As a Skill Reference

Add to your SOUL.md skill reference section:

```markdown
### Quality Gate Protocol
- Protocol spec: `skill_view(name="agent-quality-gate")`
- Self-verify script: `scripts/self-verify.sh`
- Evidence generator: `scripts/generate-evidence.sh`
- CADVP verifier: `scripts/cadvp-verify.py`
- Templates: `templates/`, `templates/evidence-report.md`, `templates/review-assignment.md`
```
