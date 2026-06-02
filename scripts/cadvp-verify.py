#!/usr/bin/env python3
"""
CADVP — Cross-Agent Delivery Verification Protocol v1.1

Usage: python3 cadvp-verify.py <target_profile>
Example: python3 cadvp-verify.py assistant-profile

Prerequisites: pip install pyyaml
"""
import sqlite3, json, sys, os, datetime

try:
    import yaml
except ImportError:
    # Fallback: simple text parsing
    yaml = None

TARGET = sys.argv[1] if len(sys.argv) > 1 else None
if not TARGET:
    print("Usage: python3 cadvp-verify.py <target_profile>")
    sys.exit(1)

BASE = os.path.expanduser(f"~/.hermes/profiles/{TARGET}")
RESULTS = []


def check(code, name, urgent, func):
    try:
        ok, detail = func()
        RESULTS.append({
            "code": code, "name": name, "urgent": urgent,
            "status": "PASS" if ok else "FAIL",
            "detail": detail
        })
    except Exception as e:
        RESULTS.append({
            "code": code, "name": name, "urgent": urgent,
            "status": "FAIL", "detail": f"Exception: {str(e)}"
        })


# ── PC-1: Target Exists ──
def pc1():
    exists = os.path.isdir(BASE)
    pidfile = os.path.join(BASE, "gateway.pid")
    pid_str = "N/A"
    if os.path.isfile(pidfile):
        with open(pidfile) as f:
            raw = f.read().strip()
            try:
                pid_data = json.loads(raw)
                pid_str = str(pid_data.get("pid", raw))
            except json.JSONDecodeError:
                pid_str = raw
    ok = exists and pid_str != "N/A"
    return ok, f"profile_dir={'✅ exists' if exists else '❌ not found'}, pid={pid_str}"


# ── CC-0: Channel Confirmation (v1.1 addition) ──
def cc0():
    """Core question: What channel carries data from 'me' to 'it'?
    Is that channel available at the target end?

    Known constraints:
    - Cron leaf agents do not have memory or fact_store tools
    - Only two reliable channels: direct DB write or target self-write
    - If data was injected via cron delegate, this channel is always broken
    """
    cfg_path = os.path.join(BASE, "config.yaml")
    mem_enabled = False
    if os.path.isfile(cfg_path) and yaml:
        with open(cfg_path) as f:
            cfg = yaml.safe_load(f)
        mem = cfg.get("memory", {})
        if mem:
            mem_enabled = mem.get("memory_enabled", False)

    db_exists = os.path.isfile(os.path.join(BASE, "memory_store.db"))

    # Determine available channels
    channels = []
    if mem_enabled and db_exists:
        channels.append("A. Direct DB write (SQLite INSERT) → ✅ Available")
    if mem_enabled:
        channels.append("B. Target self-write (memory tool) → ✅ Available (execute in target session)")
    channels.append("❌ C. Cron delegate write (leaf agent lacks memory/fact_store) → Never available")

    ok = mem_enabled and db_exists
    return ok, f"Available channels:\n" + "\n".join(f"       {c}" for c in channels)


# ── PC-2: Data Channel Mapping ──
def pc2():
    cfg_path = os.path.join(BASE, "config.yaml")
    if not os.path.isfile(cfg_path):
        return False, "config.yaml not found"
    provider = "NONE"
    enabled = False
    if yaml:
        with open(cfg_path) as f:
            cfg = yaml.safe_load(f)
        mem = cfg.get("memory", {})
        provider = mem.get("provider", "NONE") if mem else "NONE"
        enabled = mem.get("memory_enabled", False) if mem else False
    else:
        with open(cfg_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("provider:"):
                    provider = line.split(":", 1)[1].strip()
                if line.startswith("memory_enabled:"):
                    enabled = line.split(":", 1)[1].strip().lower() == "true"
    has_db = os.path.isfile(os.path.join(BASE, "memory_store.db"))
    return (provider not in ("NONE", "", None) and enabled and has_db), \
           f"provider={provider}, enabled={enabled}, memory_store.db={'✅ exists' if has_db else '❌ not found'}"


# ── PC-3: Impact Assessment ──
def pc3():
    profiles_dir = os.path.expanduser("~/.hermes/profiles/")
    if not os.path.isdir(profiles_dir):
        return True, "No profiles directory found (single-profile setup)"
    profiles = sorted([
        d for d in os.listdir(profiles_dir)
        if os.path.isdir(os.path.join(profiles_dir, d))
    ])
    return True, f"{len(profiles)} profile(s): {', '.join(profiles)}"


# ── WV-1: Data Write Confirmation ──
def wv1():
    db = os.path.join(BASE, "memory_store.db")
    if not os.path.isfile(db):
        return False, "memory_store.db not found"
    conn = sqlite3.connect(db)
    try:
        cnt = conn.execute("SELECT COUNT(*) FROM facts").fetchone()[0]
        conn.close()
        return cnt > 0, f"facts table has {cnt} record(s)"
    except sqlite3.OperationalError:
        conn.close()
        return False, "facts table does not exist"


# ── WV-2: Content Integrity ──
def wv2():
    db = os.path.join(BASE, "memory_store.db")
    if not os.path.isfile(db):
        return False, "memory_store.db not found"
    conn = sqlite3.connect(db)
    try:
        rows = conn.execute(
            "SELECT content FROM facts ORDER BY rowid DESC LIMIT 5"
        ).fetchall()
        conn.close()
    except sqlite3.OperationalError:
        conn.close()
        return False, "facts table not found or unreadable"
    if not rows:
        return False, "facts table is empty"
    contents = "\n".join(
        f"  [{i + 1}] {r[0][:80]}..." for i, r in enumerate(rows)
    )
    return True, f"Sample content (top 5):\n{contents}"


# ── WV-3: Write Permissions ──
def wv3():
    db = os.path.join(BASE, "memory_store.db")
    if not os.path.isfile(db):
        return False, "memory_store.db not found"
    st = os.stat(db)
    mode = oct(st.st_mode)[-3:]
    return True, f"permissions={mode}, size={st.st_size // 1024}KB"


# ── RV-1: Config Activation (core!) ──
def rv1():
    cfg_path = os.path.join(BASE, "config.yaml")
    if not os.path.isfile(cfg_path):
        return False, "config.yaml not found"
    provider = "NONE"
    enabled = False
    char_limit = "not set"
    if yaml:
        with open(cfg_path) as f:
            cfg = yaml.safe_load(f)
        mem = cfg.get("memory", {})
        if mem:
            provider = mem.get("provider", "NONE")
            enabled = mem.get("memory_enabled", False)
            char_limit = str(mem.get("memory_char_limit", "not set"))
    else:
        with open(cfg_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("provider:"):
                    provider = line.split(":", 1)[1].strip()
                if line.startswith("memory_enabled:"):
                    enabled = line.split(":", 1)[1].strip().lower() == "true"
    ok = provider not in ("NONE", "", None) and enabled
    return ok, f"provider={provider}, memory_enabled={enabled}, memory_char_limit={char_limit}"


# ── RV-2: Runtime Load Verification ──
def rv2():
    db = os.path.join(BASE, "memory_store.db")
    if not os.path.isfile(db):
        return False, "memory_store.db not found → cannot load"
    conn = sqlite3.connect(db)
    try:
        banks = conn.execute("SELECT COUNT(*) FROM memory_banks").fetchone()[0]
        conn.close()
        return True, f"memory_banks={banks} record(s), size={os.path.getsize(db) // 1024}KB"
    except sqlite3.OperationalError:
        conn.close()
        return False, "memory_banks table not found"


# ── RV-3: Tool Reachability ──
def rv3():
    db = os.path.join(BASE, "memory_store.db")
    if not os.path.isfile(db):
        return False, "memory_store.db not found"
    conn = sqlite3.connect(db)
    try:
        rows = conn.execute(
            "SELECT content FROM facts_fts WHERE facts_fts MATCH ?",
            ("format OR benchmark OR preference",)
        ).fetchall()
        conn.close()
        return len(rows) > 0, f"FTS search 'format OR benchmark OR preference' matched {len(rows)} record(s)"
    except sqlite3.OperationalError:
        conn.close()
        return False, "FTS index not built or query failed"


# ── RV-4: User Perception Verification ──
def rv4():
    pidfile = os.path.join(BASE, "gateway.pid")
    if os.path.isfile(pidfile):
        with open(pidfile) as f:
            raw = f.read().strip()
            try:
                pid_data = json.loads(raw)
                pid = pid_data.get("pid", 0)
            except json.JSONDecodeError:
                pid = raw
        alive = os.path.isdir(f"/proc/{pid}")
        return alive, f"gateway PID={pid}, {'✅ online' if alive else '❌ offline'}"
    return False, "No gateway.pid file found"


# ── GR-1: Dependency Impact ──
def gr1():
    profiles_dir = os.path.expanduser("~/.hermes/profiles/")
    if not os.path.isdir(profiles_dir):
        return True, "No other profiles (single-profile setup)"
    holographic_profiles = []
    for p in sorted(os.listdir(profiles_dir)):
        pdir = os.path.join(profiles_dir, p)
        if not os.path.isdir(pdir) or p == TARGET:
            continue
        cfg_file = os.path.join(pdir, "config.yaml")
        if os.path.isfile(cfg_file):
            if yaml:
                with open(cfg_file) as f:
                    try:
                        c = yaml.safe_load(f)
                        if c.get("memory", {}).get("provider") == "holographic":
                            holographic_profiles.append(p)
                    except Exception:
                        pass
            else:
                with open(cfg_file) as f:
                    for line in f:
                        if 'holographic' in line:
                            holographic_profiles.append(p)
                            break
    return True, f"Other profiles with holographic enabled: {', '.join(holographic_profiles) if holographic_profiles else 'none'}"


# ── GR-2: Documentation & Notification ──
def gr2():
    kb = os.path.expanduser("~/.hermes/knowledge/")
    exists = os.path.isdir(kb)
    return exists, f"Knowledge base directory {'✅ exists' if exists else '❌ not found'}"


# ===== Execute all checks =====
print(f"\n{'=' * 64}")
print(f" CADVP v1.1 — Cross-Agent Delivery Verification Protocol")
print(f" Target: {TARGET}")
print(f" Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'=' * 64}\n")

urgent_icons = {"Critical": "🔴", "High": "🟠", "Routine": "🟢"}

check("CC-0", "Channel Confirmation", "Critical", cc0)
check("PC-1", "Target Identity", "Critical", pc1)
check("PC-2", "Data Channel Mapping", "Critical", pc2)
check("PC-3", "Impact Assessment", "High", pc3)
check("WV-1", "Data Write Confirmation", "Routine", wv1)
check("WV-2", "Content Integrity", "Routine", wv2)
check("WV-3", "Write Permissions", "High", wv3)
check("RV-1", "Config Activation", "Critical", rv1)
check("RV-2", "Runtime Load", "Critical", rv2)
check("RV-3", "Tool Reachability", "Critical", rv3)
check("RV-4", "User Perception", "Critical", rv4)
check("GR-1", "Dependency Impact", "High", gr1)
check("GR-2", "Documentation & Notification", "Routine", gr2)

fail_count = 0
crit_fail = 0
for r in RESULTS:
    icon = "✅" if r["status"] == "PASS" else "❌"
    urg = urgent_icons.get(r["urgent"], "")
    print(f" {icon} [{r['code']}] {urg} {r['name']}: {r['status']}")
    if r["status"] == "FAIL":
        fail_count += 1
        if r["urgent"] == "Critical":
            crit_fail += 1
    # Indent details
    for line in r["detail"].split("\n"):
        print(f"       {line}")
    print()

# ===== Summary =====
print(f"{'=' * 64}")
p = sum(1 for r in RESULTS if r["status"] == "PASS")
f = sum(1 for r in RESULTS if r["status"] == "FAIL")
print(f" Total: {p} PASS / {f} FAIL (Critical: {crit_fail})")
print()
if crit_fail > 0:
    print(f" 🔴 {crit_fail} critical failure(s) — NOT deliverable, fix immediately!")
    print(f"    Fix order: RV-1(config) → RV-2/3(DB) → RV-4(test)")
elif fail_count > 0:
    print(f" 🟠 {fail_count} non-critical failure(s) — deliverable with risk acceptance")
else:
    print(f" ✅ All passed — delivery ready")
print(f"{'=' * 64}")
print()
print("# 📋 Delivery Decision")
if crit_fail > 0:
    print("    NOT deliverable. Critical chain is broken — user perception will fail.")
elif fail_count > 0:
    print("    Deliverable with risk. Close non-critical items before notifying user.")
else:
    print("    Fully ready. Safe to notify user.")
