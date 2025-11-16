#!/bin/bash
# Setup weekly meeting summary cron job
# Runs every Monday at 9 AM

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_PATH=$(which python3)

echo "Setting up weekly meeting summary cron job..."
echo ""
echo "Script directory: $SCRIPT_DIR"
echo "Python path: $PYTHON_PATH"
echo ""

# Create cron job command
CRON_CMD="0 9 * * 1 cd $SCRIPT_DIR && $PYTHON_PATH weekly_summary.py --last-week --email >> $SCRIPT_DIR/logs/weekly_summary.log 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "weekly_summary.py"; then
    echo "⚠️  Cron job already exists!"
    echo ""
    echo "Current cron jobs:"
    crontab -l | grep "weekly_summary.py"
    echo ""
    read -p "Replace existing cron job? (y/n) " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 1
    fi
    
    # Remove old cron job
    crontab -l | grep -v "weekly_summary.py" | crontab -
    echo "✅ Removed old cron job"
fi

# Create logs directory
mkdir -p "$SCRIPT_DIR/logs"

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -

echo ""
echo "✅ Cron job installed!"
echo ""
echo "Schedule: Every Monday at 9:00 AM"
echo "Command: $CRON_CMD"
echo ""
echo "Logs will be saved to: $SCRIPT_DIR/logs/weekly_summary.log"
echo ""
echo "To view current cron jobs:"
echo "  crontab -l"
echo ""
echo "To remove this cron job:"
echo "  crontab -l | grep -v 'weekly_summary.py' | crontab -"
echo ""
echo "To test manually:"
echo "  cd $SCRIPT_DIR"
echo "  python3 weekly_summary.py --last-week"
echo ""
