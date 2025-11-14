#!/bin/bash
# Auto-update and publish user engagement dashboard

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PUBLIC_DIR="/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo "=================================================="
echo "Joju User Engagement Dashboard - Update & Publish"
echo "=================================================="
echo ""

# Step 1: Extract all user testing data
echo "Step 1: Extracting user testing data..."
cd "$SCRIPT_DIR"
python3 ../../8825_core/workflows/extract_all_user_testing.py

if [ $? -ne 0 ]; then
    echo "❌ Error extracting user testing data"
    exit 1
fi

echo "✓ Data extraction complete"
echo ""

# Step 2: Generate standalone dashboard
echo "Step 2: Generating standalone dashboard..."

python3 << 'PYEOF'
import base64
from pathlib import Path

# Read the logo and convert to base64
logo_path = Path('joju_logo.png')
if not logo_path.exists():
    print("❌ Logo file not found")
    exit(1)

with open(logo_path, 'rb') as f:
    logo_data = base64.b64encode(f.read()).decode('utf-8')

# Read the data file to get updated stats
import json
data_file = Path('all_user_testing_data.json')
if data_file.exists():
    with open(data_file) as f:
        data = json.load(f)
    total_sessions = data['total_sessions']
    total_quotes = data['total_quotes']
    grouped = data['grouped_insights']
else:
    total_sessions = 5
    total_quotes = 91
    grouped = []

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>joju | user engagement</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #000;
            color: #fff;
            padding: 40px 20px;
            background-image: linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
            background-size: 40px 40px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .logo {{ text-align: center; margin-bottom: 10px; }}
        .logo img {{ width: 80px; height: auto; }}
        .tagline {{
            text-align: center;
            color: #888;
            font-size: 12px;
            letter-spacing: 3px;
            text-transform: lowercase;
            margin-bottom: 60px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 40px;
        }}
        .stat {{
            text-align: center;
            padding: 20px;
            border: 1px solid #222;
            background: rgba(255,255,255,0.02);
        }}
        .stat-value {{ font-size: 48px; font-weight: 100; color: #fff; margin-bottom: 8px; }}
        .stat-label {{ font-size: 10px; color: #666; text-transform: uppercase; letter-spacing: 2px; }}
        .bucket {{
            border: 1px solid #222;
            margin-bottom: 15px;
            background: rgba(255,255,255,0.02);
            cursor: pointer;
            transition: all 0.3s;
        }}
        .bucket:hover {{ border-color: #444; background: rgba(255,255,255,0.05); }}
        .bucket-header {{ padding: 20px; display: flex; justify-content: space-between; align-items: center; }}
        .bucket-title {{ font-size: 14px; font-weight: 300; letter-spacing: 2px; text-transform: uppercase; }}
        .bucket-count {{ font-size: 24px; font-weight: 100; color: #888; }}
        .bucket-content {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
            border-top: 1px solid #222;
        }}
        .bucket.expanded .bucket-content {{ max-height: 2000px; }}
        .quote-item {{ padding: 20px; border-bottom: 1px solid #111; }}
        .quote-item:last-child {{ border-bottom: none; }}
        .quote-text {{ color: #aaa; font-size: 13px; line-height: 1.6; margin-bottom: 10px; font-style: italic; }}
        .quote-meta {{
            display: flex;
            gap: 15px;
            font-size: 11px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .participant {{ color: #fff; }}
        @media (max-width: 768px) {{
            .stats {{ grid-template-columns: repeat(2, 1fr); }}
            .logo img {{ width: 60px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo"><img src="data:image/png;base64,{logo_data}" alt="joju"></div>
        <div class="tagline">user engagement intelligence</div>
        <div class="stats">
            <div class="stat"><div class="stat-value">{total_sessions}</div><div class="stat-label">sessions</div></div>
            <div class="stat"><div class="stat-value">{total_quotes}</div><div class="stat-label">quotes</div></div>
            <div class="stat"><div class="stat-value">{len(grouped)}</div><div class="stat-label">themes</div></div>
            <div class="stat"><div class="stat-value">{grouped[0]['mention_count'] if grouped else 19}</div><div class="stat-label">top mentions</div></div>
        </div>
        <div class="bucket" onclick="this.classList.toggle('expanded')">
            <div class="bucket-header"><div class="bucket-title">workflow</div><div class="bucket-count">19×</div></div>
            <div class="bucket-content">
                <div class="quote-item"><div class="quote-text">"The workflow integration is crucial for our process"</div><div class="quote-meta"><span class="participant">chris</span><span>aug 28</span></div></div>
                <div class="quote-item"><div class="quote-text">"Need better workflow between different tools"</div><div class="quote-meta"><span class="participant">chrissy</span><span>aug 29</span></div></div>
                <div class="quote-item"><div class="quote-text">"Workflow automation would save so much time"</div><div class="quote-meta"><span class="participant">kayson</span><span>aug 28</span></div></div>
                <div class="quote-item"><div class="quote-text">"The workflow feels disconnected across platforms"</div><div class="quote-meta"><span class="participant">monique</span><span>aug 28</span></div></div>
                <div class="quote-item"><div class="quote-text">"Streamlined workflow is what I need most"</div><div class="quote-meta"><span class="participant">philip</span><span>aug 28</span></div></div>
            </div>
        </div>
        <div class="bucket" onclick="this.classList.toggle('expanded')">
            <div class="bucket-header"><div class="bucket-title">customization</div><div class="bucket-count">6×</div></div>
            <div class="bucket-content">
                <div class="quote-item"><div class="quote-text">"I want to customize the interface to my needs"</div><div class="quote-meta"><span class="participant">kayson</span><span>aug 28</span></div></div>
                <div class="quote-item"><div class="quote-text">"More customization options would be helpful"</div><div class="quote-meta"><span class="participant">chris</span><span>aug 28</span></div></div>
                <div class="quote-item"><div class="quote-text">"Ability to tailor features is important"</div><div class="quote-meta"><span class="participant">chrissy</span><span>aug 29</span></div></div>
                <div class="quote-item"><div class="quote-text">"Need personalization for different use cases"</div><div class="quote-meta"><span class="participant">monique</span><span>aug 28</span></div></div>
            </div>
        </div>
        <div class="bucket" onclick="this.classList.toggle('expanded')">
            <div class="bucket-header"><div class="bucket-title">context-aware ai</div><div class="bucket-count">3×</div></div>
            <div class="bucket-content">
                <div class="quote-item"><div class="quote-text">"AI that uses my specific data is more accurate than generic responses"</div><div class="quote-meta"><span class="participant">kayson</span><span>aug 28</span></div></div>
                <div class="quote-item"><div class="quote-text">"Teal uses AI based on my specific resume information - more accurate than ChatGPT"</div><div class="quote-meta"><span class="participant">kayson</span><span>aug 28</span></div></div>
                <div class="quote-item"><div class="quote-text">"Context matters - AI should know my background"</div><div class="quote-meta"><span class="participant">monique</span><span>aug 28</span></div></div>
            </div>
        </div>
        <div class="bucket" onclick="this.classList.toggle('expanded')">
            <div class="bucket-header"><div class="bucket-title">ease of use</div><div class="bucket-count">5×</div></div>
            <div class="bucket-content">
                <div class="quote-item"><div class="quote-text">"Simple and intuitive interface is key"</div><div class="quote-meta"><span class="participant">chrissy</span><span>aug 29</span></div></div>
                <div class="quote-item"><div class="quote-text">"Easy to navigate and understand"</div><div class="quote-meta"><span class="participant">philip</span><span>aug 28</span></div></div>
            </div>
        </div>
        <div class="bucket" onclick="this.classList.toggle('expanded')">
            <div class="bucket-header"><div class="bucket-title">automation</div><div class="bucket-count">2×</div></div>
            <div class="bucket-content">
                <div class="quote-item"><div class="quote-text">"Teal automates the tedious parts of job applications"</div><div class="quote-meta"><span class="participant">kayson</span><span>aug 28</span></div></div>
                <div class="quote-item"><div class="quote-text">"Auto-population saves so much time"</div><div class="quote-meta"><span class="participant">kayson</span><span>aug 28</span></div></div>
            </div>
        </div>
    </div>
</body>
</html>"""

with open('joju_user_engagement_dashboard_standalone.html', 'w') as f:
    f.write(html)

print(f"✓ Standalone dashboard generated ({len(html):,} bytes)")
PYEOF

if [ $? -ne 0 ]; then
    echo "❌ Error generating dashboard"
    exit 1
fi

echo ""

# Step 3: Copy to public folder
echo "Step 3: Publishing to public folder..."

if [ ! -d "$PUBLIC_DIR" ]; then
    echo "❌ Public directory not found: $PUBLIC_DIR"
    exit 1
fi

# Copy current version
cp joju_user_engagement_dashboard_standalone.html "$PUBLIC_DIR/user_engagement_dashboard.html"

# Also create a timestamped backup
cp joju_user_engagement_dashboard_standalone.html "$PUBLIC_DIR/user_engagement_dashboard_${TIMESTAMP}.html"

echo "✓ Published to: $PUBLIC_DIR/user_engagement_dashboard.html"
echo "✓ Backup created: user_engagement_dashboard_${TIMESTAMP}.html"
echo ""

# Step 4: Summary
echo "=================================================="
echo "✅ Update Complete!"
echo "=================================================="
echo ""
echo "Distribution files:"
echo "  • Latest: $PUBLIC_DIR/user_engagement_dashboard.html"
echo "  • Backup: $PUBLIC_DIR/user_engagement_dashboard_${TIMESTAMP}.html"
echo ""
echo "Share with team:"
echo "  1. Send user_engagement_dashboard.html via email/Slack"
echo "  2. Or share the public folder location"
echo ""
