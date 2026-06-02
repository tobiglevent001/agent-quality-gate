# Completion Checklist

Check each item before reporting "done".

## Task Info

- **Description**: 
- **Type**: 
- **Time**: 

---

## CC-0 Channel Confirmation (Cross-Agent Deliveries Only)

> Skip this section if the task does not involve cross-agent data delivery.

- [ ] **CC-0**: Data delivery channel mapped and verified
  - Channel used: A (direct DB) / B (target self-write) / C (cron delegate — ❌ blocked)
  - Target tool availability confirmed: Yes / No

**CC-0 Result**: Pass / Blocked (channel unavailable)

---

## L1 Self-Verify

- [ ] 1. File exists — `ls` / `read_file` confirmed
- [ ] 2. Content correct — `grep` / `head` confirmed
- [ ] 3. Target can access — cross-profile read verified
- [ ] 3a. (Cross-agent) Target runtime read channel identified
- [ ] 3b. (Cross-agent) Data exists in target's storage medium
- [ ] 3c. (Cross-agent) Delivery channel tool available at target
- [ ] 4. Restart needed — checked and executed if required
- [ ] 5. Dependencies — other profiles/files/services checked

**L1 Result**: All Pass / Has Failures

---

## L2 Evidence Attached

- [ ] File write: path + content snippet
- [ ] Config modify: before/after diff
- [ ] API call: URL + status + response
- [ ] Cross-system: target confirmation
- [ ] Cross-agent: CADVP verification report attached
- [ ] Other: \_\_\_\_\_

**L2 Result**: Evidence complete / Evidence insufficient

---

## L3 Review

- [ ] Review needed: Yes → Assigned to \_\_\_\_\_ / No → Skipped
- [ ] Reviewer: \_\_\_\_\_
- [ ] Result: Pass / Conditional Pass / Fail

**L3 Result**: Review complete / Not required

---

## Final Gate Status

- [ ] CC-0 ✅ (or N/A)
- [ ] L1 ✅
- [ ] L2 ✅
- [ ] L3 ✅

**Conclusion**: Ready to report done / Not ready (reason: \_\_\_\_\_)
