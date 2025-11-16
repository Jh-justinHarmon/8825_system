#!/bin/bash
# Set Gemini API Key for 8825 System
# Usage: ./set_gemini_key.sh YOUR_API_KEY

if [ -z "$1" ]; then
    echo "❌ Error: No API key provided"
    echo "Usage: ./set_gemini_key.sh YOUR_API_KEY"
    exit 1
fi

API_KEY="$1"
ENV_FILE="$(dirname "$0")/.env"

# Validate key format
if [[ ! "$API_KEY" =~ ^AIzaSy ]]; then
    echo "❌ Error: Invalid API key format. Should start with 'AIzaSy'"
    exit 1
fi

# Backup existing .env if it exists
if [ -f "$ENV_FILE" ]; then
    BACKUP_DIR="$(dirname "$0")/backups/env_backups"
    mkdir -p "$BACKUP_DIR"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    cp "$ENV_FILE" "$BACKUP_DIR/.env.backup_$TIMESTAMP"
    echo "📦 Backed up existing .env to: $BACKUP_DIR/.env.backup_$TIMESTAMP"
fi

# Check if key already exists in .env
if [ -f "$ENV_FILE" ] && grep -q "^GOOGLE_GEMINI_API_KEY=" "$ENV_FILE"; then
    # Replace existing key
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/^GOOGLE_GEMINI_API_KEY=.*/GOOGLE_GEMINI_API_KEY=$API_KEY/" "$ENV_FILE"
    else
        # Linux
        sed -i "s/^GOOGLE_GEMINI_API_KEY=.*/GOOGLE_GEMINI_API_KEY=$API_KEY/" "$ENV_FILE"
    fi
    echo "✅ Updated GOOGLE_GEMINI_API_KEY in $ENV_FILE"
else
    # Add new key
    echo "" >> "$ENV_FILE"
    echo "# Google Gemini API Configuration" >> "$ENV_FILE"
    echo "# Added: $(date -Iseconds)" >> "$ENV_FILE"
    echo "# Auto-activated - no restart required" >> "$ENV_FILE"
    echo "GOOGLE_GEMINI_API_KEY=$API_KEY" >> "$ENV_FILE"
    echo "✅ Added GOOGLE_GEMINI_API_KEY to $ENV_FILE"
fi

# Set in current environment
export GOOGLE_GEMINI_API_KEY="$API_KEY"
echo "✅ Set in current environment"

# Show preview
KEY_PREVIEW="${API_KEY:0:10}...${API_KEY: -4}"
echo ""
echo "🔑 API Key: $KEY_PREVIEW"
echo "📁 Location: $ENV_FILE"
echo "✨ Status: Active (no restart needed)"
echo ""
echo "Next steps:"
echo "1. Test connection in gemini_integration_setup.html"
echo "2. Or use: python3 -c 'import os; print(os.getenv(\"GOOGLE_GEMINI_API_KEY\"))'"
