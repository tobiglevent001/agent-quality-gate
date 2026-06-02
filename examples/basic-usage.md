# Agent Quality Gate — Usage Examples

## Example 1: File Write

**Scenario:** Agent writes a configuration file and must report completion.

### Before Protocol (what usually happens)
```
Agent: "Config written."
User: "Let me check... the config is empty. It was truncated."
```

### With Protocol

**Step 1 — L1 Self-Verify:**
```bash
# Check file exists
ls -la /path/to/config.yaml
# Output: -rw-r--r-- 1 agent agent 284 Jun 3 10:00 config.yaml ✅

# Check content
head -5 /path/to/config.yaml
# Output shows correct config fields ✅

# Check dependencies
# (None — single file, single scope)
```

**Step 2 — L2 Produce Evidence:**
```
Evidence Report:
- File: /path/to/config.yaml (284 bytes, Jun 3 10:00)
- Content preview: [key sections verified]
- No restart required (application supports hot-reload)
- No cross-profile dependencies
```

**Step 3 — L3 Review:** (Not required — low risk, single scope)

**Final Report:**
```
✅ Done. Config written and verified.
Evidence: /path/to/config.yaml exists (284 bytes), key fields confirmed.
```

---

## Example 2: Config Modification

**Scenario:** Agent updates `memory_char_limit` from 5000 to 15000 in 3 config files.

### Step 1 — L1 Self-Verify:
```bash
# Check each file
grep "memory_char_limit" ~/.hermes/config.yaml      # → 15000 ✅
grep "memory_char_limit" ~/profiles/dev-agent/config.yaml  # → 15000 ✅
grep "memory_char_limit" ~/profiles/marketing-agent/config.yaml  # → 15000 ✅

# Check dependencies
# (profiles inherit from default)
```

### Step 2 — L2 Produce Evidence:
```diff
- memory_char_limit: 5000
+ memory_char_limit: 15000
- user_char_limit: 2500
+ user_char_limit: 3000
```
(Applied to 3 files, verified via grep all 3 ✅)

### Step 3 — L3 Review:
Assign review to a separate session:
```
Review request: Config change — 3 files updated.
Reviewer verifies by reading back each file.
Review result: ✅ Pass — all 3 files confirmed.
```

**Final Report:**
```
✅ Done. memory_char_limit updated to 15000 across all active profiles.
Evidence: 3 files verified, 2 inherited profiles auto-enabled.
Review: Passed independent check.
```

---

## Example 3: Cross-Profile Operation

**Scenario:** Agent writes a file to profile A that profile B needs to read.

### Step 1 — L1 Self-Verify (Source):
```bash
# Confirm file was written from current perspective
ls -la ~/.hermes/profiles/profile-a/target.md  ✅
```

### Step 2 — L1 Extended (Target verification):
```bash
# Read from target profile's path (different working directory perspective)
cat ~/.hermes/profiles/profile-b/../profile-a/target.md
# OR: switch to profile B's context and confirm access
```

### Step 3 — L2 Produce Evidence:
```
Evidence Report:
- Source profile A: file exists ✅
- Target profile B path: accessible ✅
- Content consistent: same hash ✅
```

### Step 4 — L3 Review:
Delegate to profile B's agent to check:
```
Profile B agent: "Can access /path/to/target.md from my context."
```

**Final Report:**
```
✅ Done. Cross-profile write verified from both sides.
Evidence: source + target path confirmed.
Review: Profile B agent confirmed access.
```

---

## Example 4: Cross-Agent Knowledge Injection (CADVP v1.1)

**Scenario:** Coordinator agent injects business knowledge into a sub-agent's memory system.

### Step 0 — CC-0 Channel Confirmation:
```
Data path: Coordinator → SQLite INSERT → Target's memory_store.db → holographic provider → context injection

Channel analysis:
  A. Direct DB write (SQLite INSERT) → ✅ Available (target has holographic enabled, DB exists)
  B. Target self-write (memory tool) → ✅ Available (but requires target session)
  C. Cron delegate → ❌ Not available (leaf agent lacks memory tool)

Decision: Use Channel A.
```

### Step 1 — Inject via Direct DB Write:
```bash
DB=~/.hermes/profiles/assistant-profile/memory_store.db
sqlite3 "$DB" "INSERT INTO facts (content, category) VALUES ('Business rule: ...', 'memory');"
```

### Step 2 — Run CADVP Verification:
```bash
python3 scripts/cadvp-verify.py assistant-profile
```

### Step 3 — Review CADVP Output:
```
✅ [CC-0] Channel Confirmation: PASS — Channel A available
✅ [PC-1] Target Identity: PASS — profile exists, gateway online
✅ [PC-2] Data Channel Mapping: PASS — holographic enabled, DB exists
✅ [WV-1] Data Write: PASS — facts table has 15 records
✅ [WV-2] Content Integrity: PASS — content verified
✅ [RV-1] Config Activation: PASS — provider=holographic, enabled=true
✅ [RV-2] Runtime Load: PASS — memory_banks populated
✅ [RV-3] Tool Reachability: PASS — FTS search matched
✅ [RV-4] User Perception: PASS — gateway online
✅ [GR-1] Dependency Impact: PASS
✅ [GR-2] Documentation: PASS

Total: 13 PASS / 0 FAIL
✅ All passed — delivery ready
```

**Final Report:**
```
✅ Done. Knowledge injected via Channel A (direct DB write).
CADVP: 13/13 dimensions passed. Delivery chain verified end-to-end.
```

### What If Channel C Was Used (Failure Example):
```
Coordinator created cron job to run memory() in target profile.
CC-0 check: ❌ FAIL — cron leaf agent has no memory tool.
Result: Data never reached target's memory system.
Fix: Switch to Channel A (direct SQLite INSERT).
```
