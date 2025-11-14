#!/bin/bash
# 8825 Dependency Checker
# Verifies all required dependencies are installed

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REGISTRY="$SCRIPT_DIR/SYSTEM_REGISTRY.json"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo "=== Dependency Check ==="
echo ""

# Check if jq is available (needed to read registry)
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}⚠️  jq not installed (needed to read registry)${NC}"
    echo "   Installing jq..."
    if command -v brew &> /dev/null; then
        brew install jq
        echo -e "${GREEN}✅ jq installed${NC}"
    else
        echo -e "${YELLOW}⚠️  Homebrew not found, please install jq manually${NC}"
        exit 1
    fi
fi

# Read dependencies from registry
deps=$(jq -r '.system_dependencies | keys[]' "$REGISTRY")

missing_count=0
installed_count=0

for dep in $deps; do
    check_cmd=$(jq -r ".system_dependencies.$dep.check" "$REGISTRY")
    
    if eval "$check_cmd" > /dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} $dep"
        installed_count=$((installed_count + 1))
    else
        echo -e "${YELLOW}⚠️${NC}  $dep not found"
        install_cmd=$(jq -r ".system_dependencies.$dep.install" "$REGISTRY")
        
        if [ "$install_cmd" != "built-in (macOS)" ]; then
            echo "   Installing $dep..."
            if eval "$install_cmd"; then
                echo -e "   ${GREEN}✅${NC} $dep installed"
                installed_count=$((installed_count + 1))
            else
                echo -e "   ${YELLOW}⚠️${NC}  Failed to install $dep"
                missing_count=$((missing_count + 1))
            fi
        else
            echo -e "   ${GREEN}✅${NC} $dep (built-in)"
            installed_count=$((installed_count + 1))
        fi
    fi
done

echo ""
if [ $missing_count -eq 0 ]; then
    echo -e "${GREEN}✅ All dependencies satisfied ($installed_count/$installed_count)${NC}"
else
    echo -e "${YELLOW}⚠️  $missing_count dependencies missing${NC}"
fi
echo ""
