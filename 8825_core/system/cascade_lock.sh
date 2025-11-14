#!/bin/bash
# Cascade Lock System
# Prevents multiple Cascade instances from making simultaneous system-wide changes
# Auto-unlocks after 15 minutes

LOCK_DIR="$HOME/.8825"
LOCK_FILE="$LOCK_DIR/cascade.lock"
LOCK_TIMEOUT=900  # 15 minutes in seconds

# Ensure lock directory exists
mkdir -p "$LOCK_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if lock is stale (older than timeout)
is_lock_stale() {
    if [ ! -f "$LOCK_FILE" ]; then
        return 1  # No lock file, not stale
    fi
    
    local lock_time=$(stat -f %m "$LOCK_FILE" 2>/dev/null || stat -c %Y "$LOCK_FILE" 2>/dev/null)
    local current_time=$(date +%s)
    local age=$((current_time - lock_time))
    
    if [ $age -gt $LOCK_TIMEOUT ]; then
        return 0  # Stale lock
    else
        return 1  # Fresh lock
    fi
}

# Acquire lock
acquire_lock() {
    local operation="$1"
    local cascade_id="${2:-$(uuidgen 2>/dev/null || echo "cascade-$$")}"
    
    # Check for existing lock
    if [ -f "$LOCK_FILE" ]; then
        if is_lock_stale; then
            echo -e "${YELLOW}⚠️  Stale lock detected (>15 min), removing...${NC}"
            rm -f "$LOCK_FILE"
        else
            echo -e "${RED}❌ System is locked by another Cascade instance${NC}"
            echo ""
            cat "$LOCK_FILE"
            echo ""
            echo "Options:"
            echo "  1. Wait for the other operation to complete"
            echo "  2. Override (risky if other Cascade is still working)"
            echo "  3. Cancel this operation"
            return 1
        fi
    fi
    
    # Create lock file
    cat > "$LOCK_FILE" << EOF
{
  "cascade_id": "$cascade_id",
  "operation": "$operation",
  "started_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "pid": $$,
  "timeout_minutes": 15
}
EOF
    
    echo -e "${GREEN}✅ Lock acquired for: $operation${NC}"
    return 0
}

# Release lock
release_lock() {
    if [ -f "$LOCK_FILE" ]; then
        local operation=$(grep -o '"operation": "[^"]*"' "$LOCK_FILE" | cut -d'"' -f4)
        rm -f "$LOCK_FILE"
        echo -e "${GREEN}✅ Lock released: $operation${NC}"
    fi
}

# Check lock status
check_lock() {
    if [ -f "$LOCK_FILE" ]; then
        if is_lock_stale; then
            echo -e "${YELLOW}Stale lock present (will auto-remove):${NC}"
        else
            echo -e "${YELLOW}Active lock:${NC}"
        fi
        cat "$LOCK_FILE"
        return 1
    else
        echo -e "${GREEN}No active lock${NC}"
        return 0
    fi
}

# Force unlock (use with caution)
force_unlock() {
    if [ -f "$LOCK_FILE" ]; then
        echo -e "${RED}⚠️  Force removing lock${NC}"
        cat "$LOCK_FILE"
        rm -f "$LOCK_FILE"
        echo -e "${GREEN}✅ Lock removed${NC}"
    else
        echo -e "${GREEN}No lock to remove${NC}"
    fi
}

# Main command interface
case "${1:-}" in
    acquire)
        acquire_lock "$2"
        ;;
    release)
        release_lock
        ;;
    check)
        check_lock
        ;;
    force-unlock)
        force_unlock
        ;;
    *)
        echo "Cascade Lock System"
        echo ""
        echo "Usage:"
        echo "  source cascade_lock.sh"
        echo "  acquire_lock 'operation description'"
        echo "  release_lock"
        echo ""
        echo "Or:"
        echo "  cascade_lock.sh acquire 'operation'"
        echo "  cascade_lock.sh release"
        echo "  cascade_lock.sh check"
        echo "  cascade_lock.sh force-unlock"
        ;;
esac
