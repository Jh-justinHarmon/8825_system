# Protocol Tracking Integration Guide

How to integrate protocol tracking into your workflow and systems.

---

## Manual Integration (Current)

### During Work

When you consult a protocol:

1. **Open protocol** (e.g., `DEEP_DIVE_RESEARCH_PROTOCOL.md`)
2. **Follow protocol steps**
3. **Track usage immediately:**

```bash
cd 8825_core/protocols
./track_protocol.py DEEP_DIVE_RESEARCH_PROTOCOL --success \
  --context "Debugging Downloads sync" \
  --notes "Found Universal Inbox Watch issue"
```

### Weekly Review

Every Friday:

```bash
cd 8825_core/protocols
./track_protocol.py --report > ~/Documents/protocol_report_$(date +%Y%m%d).md
```

Review:
- Which protocols are promoted? (working well)
- Which are decaying? (need updates or removal)
- Which are unused? (consider removing)

---

## Cascade Integration

### Option 1: Manual Checkpoint

At Cascade checkpoints, track protocols consulted:

```python
# In your Cascade workflow
from protocol_tracker import ProtocolTracker

tracker = ProtocolTracker()
tracker.record_usage(
    "DEEP_DIVE_RESEARCH_PROTOCOL",
    success=True,
    context="Debugging sync issue"
)
```

### Option 2: Automatic Detection

Parse checkpoint summaries for protocol mentions:

```python
import re
from protocol_tracker import ProtocolTracker

def track_protocols_from_checkpoint(checkpoint_text: str):
    """Detect protocol mentions in checkpoint"""
    tracker = ProtocolTracker()
    
    # Pattern: "consulted X protocol" or "used X protocol"
    pattern = r'(consulted|used|followed)\s+([A-Z_]+(?:_PROTOCOL)?)'
    
    for match in re.finditer(pattern, checkpoint_text, re.IGNORECASE):
        protocol_id = match.group(2)
        
        # Determine success from context
        success = 'failed' not in checkpoint_text.lower()
        
        tracker.record_usage(protocol_id, success, context="From checkpoint")
```

---

## Brain Sync Daemon Integration

### Add Protocol Tracking to Daemon

Edit `8825_core/brain/brain_sync_daemon.py`:

```python
from protocol_tracker import ProtocolTracker

class BrainSyncDaemon:
    def __init__(self):
        # ... existing init ...
        self.protocol_tracker = ProtocolTracker()
    
    def check_protocol_decay(self):
        """Check for decaying protocols and broadcast"""
        # Get all protocols
        protocols = self.protocol_tracker.list_protocols()
        
        # Find decaying
        decaying = [p for p in protocols if p['status'] == 'decaying']
        
        if decaying:
            self.broadcast_update({
                'type': 'protocol_decay',
                'protocols': decaying,
                'message': f"{len(decaying)} protocols are decaying"
            })
    
    def run_cycle(self):
        # ... existing cycle ...
        
        # Check protocol decay every 10 cycles (5 min)
        if self.cycle_count % 10 == 0:
            self.check_protocol_decay()
```

---

## IDE Integration

### VSCode Extension (Future)

Track when protocol files are opened:

```javascript
// extension.js
vscode.workspace.onDidOpenTextDocument((doc) => {
  const path = doc.fileName;
  
  // Check if it's a protocol file
  if (path.includes('8825_core/protocols/') && 
      (path.endsWith('.md') || path.endsWith('.json'))) {
    
    const protocolId = path.split('/').pop().replace(/\.(md|json)$/, '');
    
    // Show quick action
    vscode.window.showInformationMessage(
      `Track usage of ${protocolId}?`,
      'Success', 'Failure', 'Cancel'
    ).then(selection => {
      if (selection === 'Success' || selection === 'Failure') {
        // Call track_protocol.py
        exec(`./track_protocol.py ${protocolId} --${selection.toLowerCase()}`);
      }
    });
  }
});
```

---

## Git Integration

### Pre-commit Hook

Track protocols mentioned in commits:

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Get commit message
COMMIT_MSG=$(git log -1 --pretty=%B)

# Check for protocol mentions
if echo "$COMMIT_MSG" | grep -i "protocol"; then
  # Extract protocol names
  PROTOCOLS=$(echo "$COMMIT_MSG" | grep -oE '[A-Z_]+_PROTOCOL')
  
  for PROTOCOL in $PROTOCOLS; do
    # Ask user if they want to track
    read -p "Track usage of $PROTOCOL? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      cd 8825_core/protocols
      ./track_protocol.py "$PROTOCOL" --success --context "From commit"
    fi
  done
fi
```

---

## Slack/Discord Integration

### Slash Command

```python
# slack_bot.py
from protocol_tracker import ProtocolTracker

@app.command("/track-protocol")
def track_protocol_command(ack, command, respond):
    ack()
    
    # Parse: /track-protocol DEEP_DIVE_RESEARCH_PROTOCOL success "Debugging"
    parts = command['text'].split()
    protocol_id = parts[0]
    success = parts[1].lower() == 'success'
    context = ' '.join(parts[2:]).strip('"')
    
    tracker = ProtocolTracker()
    result = tracker.record_usage(protocol_id, success, context)
    
    if result:
        stats = tracker.get_usage_stats(protocol_id)
        respond(f"✅ Tracked {protocol_id}\n"
                f"Uses: {stats['use_count']}, "
                f"Success: {stats['success_rate']:.0%}, "
                f"Status: {stats['status']}")
    else:
        respond(f"❌ Protocol not found: {protocol_id}")
```

---

## Automation Ideas

### 1. Daily Digest

```bash
# crontab: Run daily at 5pm
0 17 * * * cd ~/8825/8825_core/protocols && ./track_protocol.py --report | mail -s "Protocol Usage Report" you@example.com
```

### 2. Decay Alerts

```python
# decay_alert.py
from protocol_tracker import ProtocolTracker

tracker = ProtocolTracker()
protocols = tracker.list_protocols(status='decaying')

if protocols:
    print(f"⚠️  {len(protocols)} protocols are decaying:")
    for p in protocols:
        print(f"  - {p['name']} (last used: {p['last_used']})")
```

### 3. Auto-Archive Deprecated

```python
# archive_deprecated.py
from protocol_tracker import ProtocolTracker
from pathlib import Path
import shutil

tracker = ProtocolTracker()
deprecated = tracker.list_protocols(status='deprecated')

archive_dir = Path('8825_core/protocols/archived')
archive_dir.mkdir(exist_ok=True)

for protocol in deprecated:
    src = Path(protocol['path'])
    dst = archive_dir / src.name
    
    print(f"Archiving {protocol['name']}...")
    shutil.move(src, dst)
```

---

## API Usage

### Python API

```python
from protocol_tracker import ProtocolTracker

# Initialize
tracker = ProtocolTracker()

# Record usage
tracker.record_usage(
    protocol_id="DEEP_DIVE_RESEARCH_PROTOCOL",
    success=True,
    context="Debugging sync issue",
    notes="Found root cause"
)

# Get stats
stats = tracker.get_usage_stats("DEEP_DIVE_RESEARCH_PROTOCOL")
print(f"Success rate: {stats['success_rate']:.0%}")

# List protocols
protocols = tracker.list_protocols(status='promoted')
for p in protocols:
    print(f"{p['name']}: {p['use_count']} uses")

# Generate report
report = tracker.generate_usage_report()
print(report)
```

---

## Best Practices

### 1. Track Immediately
Don't wait until end of day - track right after using protocol.

### 2. Be Specific with Context
Good: "Debugging Downloads sync - found Universal Inbox Watch"
Bad: "Debugging"

### 3. Track Failures Too
Failures are valuable data. They show where protocols don't work.

### 4. Review Regularly
Weekly review keeps protocols current and relevant.

### 5. Update Decaying Protocols
If a protocol is decaying but still valuable, use it or update it.

### 6. Remove Deprecated
Don't let deprecated protocols clutter the system.

---

## Metrics to Track

### System Health
- **Tracking rate:** % of protocols with usage data
- **Active rate:** % of protocols used in last 30 days
- **Success rate:** Average success rate across all protocols
- **Decay rate:** % of protocols decaying

### Protocol Quality
- **Promotion rate:** % of protocols that get promoted
- **Failure rate:** % of uses that fail
- **Context diversity:** # of different contexts per protocol
- **Longevity:** Average age of promoted protocols

---

## Troubleshooting

### Protocol Not Found
```bash
# List all protocols to find correct ID
./track_protocol.py --list
```

### Wrong Protocol ID
Protocol IDs are filenames without extensions:
- `DEEP_DIVE_RESEARCH_PROTOCOL.md` → `DEEP_DIVE_RESEARCH_PROTOCOL`
- `definition_of_done.md` → `definition_of_done`

### State Files Missing
State files are created automatically in `8825_core/protocols/state/`:
- `protocol_usage.jsonl` - Usage log
- `protocol_metadata.json` - Current stats

---

## Future Enhancements

### 1. Web Dashboard
Real-time protocol usage dashboard with charts and trends.

### 2. Recommendation Engine
"You're working on X, consider consulting Y protocol"

### 3. Cross-Protocol Analysis
Which protocols are used together? Which conflict?

### 4. Protocol Templates
Generate new protocols based on successful patterns.

### 5. A/B Testing
Test protocol variations and track which performs better.

---

**Questions?** See `PROTOCOL_TRACKING_README.md` for full documentation.
