#!/bin/bash
# self-verify.sh — Agent Quality Gate L1 self-verification script
# Usage: ./self-verify.sh <file-path> [grep-keyword]
# Example: ./self-verify.sh ~/.hermes/config.yaml "memory_char_limit"

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

TARGET="${1:-}"
KEYWORD="${2:-}"

if [ -z "$TARGET" ]; then
    echo -e "${RED}❌ Usage: $0 <file-path> [grep-keyword]${NC}"
    exit 1
fi

PASS=true

echo "═══════════════════════════════════════════"
echo "  L1 Self-Verification Report"
echo "  Target: $TARGET"
echo "  Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════"
echo ""

# L1-1: Does the file exist?
echo -n "[L1-1] File existence ... "
if [ -f "$TARGET" ]; then
    SIZE=$(stat -c%s "$TARGET" 2>/dev/null || echo "?")
    echo -e "${GREEN}✅ Exists (${SIZE} bytes)${NC}"
else
    echo -e "${RED}❌ Not found${NC}"
    PASS=false
fi

# L1-2: Is the content correct?
if [ -n "$KEYWORD" ] && [ -f "$TARGET" ]; then
    echo -n "[L1-2] Keyword '${KEYWORD}' found ... "
    if grep -q "$KEYWORD" "$TARGET" 2>/dev/null; then
        LINE=$(grep -n "$KEYWORD" "$TARGET" | head -1)
        echo -e "${GREEN}✅ Match: $LINE${NC}"
    else
        echo -e "${RED}❌ Not found${NC}"
        PASS=false
    fi
elif [ -f "$TARGET" ]; then
    echo -e "[L1-2] ${YELLOW}⏭ Skipped (no keyword provided)${NC}"
fi

# L1-3: Is the file readable?
if [ -f "$TARGET" ]; then
    echo -n "[L1-3] File readability ... "
    if head -1 "$TARGET" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Readable${NC}"
    else
        echo -e "${RED}❌ Unreadable${NC}"
        PASS=false
    fi
fi

# L1-4: Restart required?
echo -n "[L1-4] Restart/reload check ... "
case "$TARGET" in
    *.yaml|*.yml|*.json|*.toml|*.conf|*.cfg)
        echo -e "${YELLOW}⚠ Config file — check if service reload needed${NC}" ;;
    *.py|*.js|*.ts|*.vue|*.sh)
        echo -e "${YELLOW}⚠ Script/code file — check hot-reload status${NC}" ;;
    *.md|*.txt|*.html|*.css)
        echo -e "${GREEN}✅ Static file, no restart needed${NC}" ;;
    *)
        echo -e "${YELLOW}⚠ Unknown type — check manually${NC}" ;;
esac

# L1-5: Cross-profile dependencies?
echo -n "[L1-5] Profile dependency check ... "
if echo "$TARGET" | grep -q "profiles/"; then
    THIS_PROFILE=$(echo "$TARGET" | grep -oP 'profiles/[^/]+' || true)
    if [ -n "$THIS_PROFILE" ]; then
        echo -e "${YELLOW}⚠ Belongs to $THIS_PROFILE — check other profiles need sync${NC}"
    fi
else
    echo -e "${GREEN}✅ Single scope, no profile dependency${NC}"
fi

echo ""
echo "═══════════════════════════════════════════"
if [ "$PASS" = true ]; then
    echo -e "  ${GREEN}✅ L1 Self-Verification: ALL PASSED${NC}"
else
    echo -e "  ${RED}❌ L1 Self-Verification: FAILURES DETECTED — fix and re-run${NC}"
fi
echo "═══════════════════════════════════════════"
