#!/bin/bash
# Cascade Configuration Diagnostic Script
# Run this after restart to check if configuration persists

echo "=== Cascade Configuration Check ==="
echo ""

echo "1. Checking Windsurf settings..."
if [ -f "$HOME/Library/Application Support/Windsurf/User/settings.json" ]; then
    echo "✅ Settings file exists"
    cat "$HOME/Library/Application Support/Windsurf/User/settings.json"
else
    echo "❌ Settings file not found"
fi
echo ""

echo "2. Checking workspace .cascade folder..."
if [ -d ".cascade" ]; then
    echo "✅ .cascade folder exists"
    ls -la .cascade/
else
    echo "❌ .cascade folder not found"
fi
echo ""

echo "3. Checking for .vscode settings..."
if [ -f ".vscode/settings.json" ]; then
    echo "✅ Workspace settings exist"
    cat .vscode/settings.json
else
    echo "❌ No workspace settings"
fi
echo ""

echo "4. Checking Windsurf config directory..."
if [ -d "$HOME/Library/Application Support/Windsurf" ]; then
    echo "✅ Windsurf config directory exists"
    echo "Contents:"
    ls -la "$HOME/Library/Application Support/Windsurf/" | head -20
else
    echo "❌ Windsurf config directory not found"
fi
echo ""

echo "5. Checking for Cascade-specific files..."
find "$HOME/Library/Application Support/Windsurf" -name "*cascade*" -o -name "*Cascade*" 2>/dev/null | head -10
echo ""

echo "=== Test in Cascade ==="
echo "Ask Cascade: 'What tools do you have access to?'"
echo "Expected: run_command, edit, multi_edit, etc."
echo ""

echo "=== Configuration Backup ==="
echo "Backup location: Documents/CASCADE_CONFIGURATION_BACKUP.md"
echo ""

echo "Done! Compare results with working session."
