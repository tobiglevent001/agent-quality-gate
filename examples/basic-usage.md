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
grep "memory_char_limit" ~/profiles/dev-pony/config.yaml  # → 15000 ✅
grep "memory_char_limit" ~/profiles/marketing-pony/config.yaml  # → 15000 ✅

# Check dependencies
# (profiles/kehu-tuozhan-xiaoqi and laiven-assistant inherit from default)
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
