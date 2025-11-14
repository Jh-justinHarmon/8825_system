#!/bin/bash
# Test Weekend Soccer Advisor

cd "$(dirname "$0")"

echo "🧪 Testing Weekend Soccer Advisor"
echo "=================================="
echo ""

# Check if dependencies installed
if ! python3 -c "import googlemaps" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
    echo ""
fi

# Check for Maps API key
if [ -z "$GOOGLE_MAPS_API_KEY" ]; then
    echo "⚠️  GOOGLE_MAPS_API_KEY not set"
    echo "   Travel time will use default 20 minutes"
    echo "   To enable: export GOOGLE_MAPS_API_KEY=your_key"
    echo ""
fi

# Run preview
echo "📅 Generating weekend preview..."
python3 soccer_advisor.py --preview

echo ""
echo "✅ Test complete!"
echo ""
echo "Next steps:"
echo "1. Check output in ~/Downloads/soccer_schedule.json"
echo "2. Verify events detected correctly"
echo "3. Check travel time calculations"
echo "4. Review leave_by times"
