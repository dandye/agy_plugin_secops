#!/usr/bin/env bash
# Validation script for the google-secops plugin.
set -e

echo "=== Validating Antigravity Plugin: google-secops ==="

# Check manifest file
if [ -f "plugin.json" ]; then
    echo "[OK] plugin.json found"
    # Basic json check if python is available
    if command -v python3 >/dev/null 2>&1; then
        python3 -c "import json; json.load(open('plugin.json'))"
        echo "  [OK] plugin.json parses as valid JSON"
    fi
else
    echo "[FAIL] Error: plugin.json not found!"
    exit 1
fi

# Check optional component directories / files
if [ -f "mcp_config.json" ]; then
    echo "[OK] mcp_config.json found"
    if command -v python3 >/dev/null 2>&1; then
        python3 -c "import json; json.load(open('mcp_config.json'))"
        echo "  [OK] mcp_config.json parses as valid JSON"
    fi
fi

if [ -f "hooks/hooks.json" ]; then
    echo "[OK] hooks/hooks.json found"
    if command -v python3 >/dev/null 2>&1; then
        python3 -c "import json; json.load(open('hooks/hooks.json'))"
        echo "  [OK] hooks/hooks.json parses as valid JSON"
    fi
fi

if [ -d "skills" ]; then
    echo "[OK] skills/ directory found"
    # Verify SKILL.md has YAML header
    find skills -name "SKILL.md" | while read -r skill_file; do
        if head -n 1 "$skill_file" | grep -q "^---"; then
            echo "  [OK] $skill_file contains metadata frontmatter header"
        else
            echo "  [FAIL] Warning: $skill_file does not start with --- frontmatter header!"
        fi
    done
fi

if [ -d "rules" ]; then
    echo "[OK] rules/ directory found"
fi

# Run dynamic validate tool if agy command exists
if command -v agy >/dev/null 2>&1; then
    echo "[OK] running 'agy plugin validate' command..."
    agy plugin validate .
else
    echo "[INFO] 'agy' CLI command not found in PATH; skipping native validation."
    echo "  (You can install it globally or check your shell configuration)"
fi

echo "=== Validation Completed Successfully ==="
