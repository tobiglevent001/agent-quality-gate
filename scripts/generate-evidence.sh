#!/bin/bash
# generate-evidence.sh — Agent Quality Gate L2 evidence report generator
# Usage: ./generate-evidence.sh <description> <operation-type> [evidence-files...]
# Operation types: file-write | config-modify | api-call | cross-profile | content-publish | file-delete | data-write

set -euo pipefail

DESCRIPTION="${1:-}"
OP_TYPE="${2:-}"
shift 2 2>/dev/null || true

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

if [ -z "$DESCRIPTION" ] || [ -z "$OP_TYPE" ]; then
    echo "Usage: $0 <description> <operation-type> [evidence-files...]"
    echo "Types: file-write | config-modify | api-call | cross-profile | content-publish | file-delete | data-write"
    exit 1
fi

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
REPORT_FILE="evidence-report-$(date '+%Y%m%d%H%M%S').md"

cat > "$REPORT_FILE" << EOF
# L2 Evidence Report

**Operation**: $DESCRIPTION
**Type**: $OP_TYPE
**Time**: $TIMESTAMP

---

## Verification Evidence

EOF

for FILE in "$@"; do
    if [ -f "$FILE" ]; then
        cat >> "$REPORT_FILE" << EOF
### \`$FILE\`

- **Status**: ✅ Exists
- **Size**: $(stat -c%s "$FILE" 2>/dev/null || echo '?') bytes
- **Modified**: $(stat -c%y "$FILE" 2>/dev/null || echo '?')

\`\`\`
$(head -20 "$FILE")
... (first 20 lines)
\`\`\`

EOF
    else
        cat >> "$REPORT_FILE" << EOF
### ❌ \`$FILE\`

- **Status**: ❌ Not found

EOF
    fi
done

cat >> "$REPORT_FILE" << EOF
---
## Gate Status

- [ ] L1 Self-Verify: Pass / Fail
- [ ] L2 Evidence: Report generated
- [ ] L3 Review: Required / Not required → Status: \_\_\_\_\_\_

*Report auto-generated at $TIMESTAMP*
EOF

echo -e "${GREEN}✅ Evidence report generated: $REPORT_FILE${NC}"
echo -e "${YELLOW}📋 Open $REPORT_FILE to fill verification fields${NC}"
