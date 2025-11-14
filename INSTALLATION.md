# 8825 Installation Guide

**Complete setup instructions for 8825 system**

**Version:** 3.1.0  
**Last Updated:** 2025-11-13

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Verification](#verification)
5. [Optional Features](#optional-features)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### **Operating System:**
- macOS 12.0+ (Monterey or later)
- Linux (Ubuntu 20.04+, Debian 11+)
- Windows (via WSL2, not tested)

### **Required Software:**
- Python 3.10 or higher
- pip 23.0 or higher
- Git 2.30 or higher

### **Required API Keys:**
- OpenAI API key (required for all AI features)

### **Optional Software:**
- Tesseract OCR (for bill processing)
- Node.js 18+ (for MCP servers)

### **Storage:**
- Minimum: 500 MB
- Recommended: 2 GB

See `SYSTEM_REQUIREMENTS.md` for complete details.

---

## Installation Steps

### **Step 1: Download 8825**

```bash
# Option A: Git clone (if using GitHub)
git clone https://github.com/yourusername/8825-system.git
cd 8825-system

# Option B: Download and extract
# (if you have a zip file)
unzip 8825-system.zip
cd 8825-system
```

### **Step 2: Run Installation Script**

```bash
./scripts/install.sh
```

**What this does:**
1. ✅ Checks Python version (3.10+)
2. ✅ Creates virtual environment
3. ✅ Installs Python dependencies
4. ✅ Creates directory structure (~/.8825)
5. ✅ Auto-configures paths in .env
6. ✅ Checks optional dependencies
7. ✅ Initializes brain system

**Time:** ~5 minutes

### **Step 3: Add OpenAI API Key**

```bash
# Edit .env file
nano .env

# Find this line:
OPENAI_API_KEY=your_openai_api_key_here

# Replace with your actual key:
OPENAI_API_KEY=sk-proj-abc123...

# Save: Ctrl+O, Enter, Ctrl+X
```

**Get your key:** https://platform.openai.com/api-keys

### **Step 4: Verify Installation**

```bash
./scripts/check_requirements.sh
```

**Expected output:**
```
✅ Python 3.10.x
✅ pip 23.x.x
✅ openai (x.x.x)
✅ .env file exists
✅ OpenAI API key configured
✅ ~/.8825 directory exists
✅ Brain state initialized

✅ Passed: 15
⚠️  Warnings: 2
❌ Failed: 0

🎉 All required checks passed!
```

---

## Configuration

### **Environment Variables**

The `.env` file was auto-configured during installation. Review and adjust if needed:

```bash
# System Paths (auto-configured)
SYSTEM_ROOT=/path/to/8825-system
DROPBOX_ROOT=/path/to/Dropbox
DOWNLOADS_DIR=/path/to/Downloads
USER_NAME=your_username

# OpenAI API Key (REQUIRED)
OPENAI_API_KEY=sk-proj-...

# Optional: Google API
# GOOGLE_CREDENTIALS_PATH=${SYSTEM_ROOT}/8825_core/integrations/google/credentials.json
# GOOGLE_TOKEN_PATH=${SYSTEM_ROOT}/8825_core/integrations/google/token.json

# Optional: Reddit API
# REDDIT_CLIENT_ID=your_client_id
# REDDIT_CLIENT_SECRET=your_client_secret
```

### **Path Configuration**

Paths are automatically detected during installation:

- **SYSTEM_ROOT:** Where 8825 is installed
- **DROPBOX_ROOT:** Your Dropbox folder (if you use Dropbox)
- **DOWNLOADS_DIR:** Your Downloads folder
- **USER_NAME:** Your system username

**To override:** Edit `.env` and change the values.

### **Directory Structure**

After installation:

```
~/
├── 8825-system/              # System root
│   ├── 8825_core/           # Core system
│   ├── scripts/             # Installation scripts
│   ├── .env                 # Configuration (not committed)
│   └── venv/                # Virtual environment
│
└── .8825/                    # User config
    ├── brain_state/         # Brain state
    └── accountability_loops.json
```

---

## Verification

### **Test 1: Python Environment**

```bash
source venv/bin/activate
python3 --version
# Should show: Python 3.10.x or higher
```

### **Test 2: Dependencies**

```bash
python3 -c "import openai; print('✅ OpenAI installed')"
python3 -c "from dotenv import load_dotenv; print('✅ dotenv installed')"
```

### **Test 3: Path Configuration**

```bash
python3 8825_core/utils/paths.py
# Should show your actual paths
```

### **Test 4: Brain System**

```bash
python3 8825_core/brain/brain_daemon.py &
# Should start without errors
# Stop with: pkill -f brain_daemon
```

---

## Optional Features

### **Google API Integration**

Required for: Gmail, Calendar, Drive

**Setup:**
1. Go to https://console.cloud.google.com/
2. Create project
3. Enable APIs (Gmail, Calendar, Drive)
4. Create OAuth credentials
5. Download `credentials.json`
6. Place in `8825_core/integrations/google/`
7. Run any Google integration (will prompt for auth)

**Documentation:** `8825_core/integrations/google/README.md`

### **Tesseract OCR**

Required for: Bill processing

```bash
# macOS
brew install tesseract

# Linux
sudo apt install tesseract-ocr

# Verify
tesseract --version
```

### **Playwright Browsers**

Required for: Screenshot generation

```bash
python3 -m playwright install chromium
```

### **Reddit API**

Required for: Reddit integration

1. Go to https://www.reddit.com/prefs/apps
2. Create app
3. Add credentials to `.env`

---

## Troubleshooting

### **Installation Fails**

**"Python version too old"**
```bash
# macOS
brew install python@3.10
brew link python@3.10

# Linux
sudo apt install python3.10 python3.10-venv
```

**"pip install fails"**
```bash
# Upgrade pip
python3 -m pip install --upgrade pip

# Try again
pip install -r requirements-full.txt
```

**"Permission denied"**
```bash
# Make scripts executable
chmod +x scripts/*.sh
```

### **Configuration Issues**

**"OpenAI API key not working"**
- Verify key starts with `sk-proj-` or `sk-`
- Check for extra spaces in .env
- Test: `cat .env | grep OPENAI_API_KEY`

**"Paths not found"**
- Check `.env` file exists
- Verify paths in `.env` are correct
- Test: `python3 8825_core/utils/paths.py`

**"Module not found"**
```bash
# Activate virtual environment
source venv/bin/activate

# Verify you're in venv
which python3
# Should show: .../venv/bin/python3
```

### **Runtime Issues**

**"Brain daemon won't start"**
```bash
# Check brain state
ls -la ~/.8825/brain_state/

# Reinitialize if needed
rm -rf ~/.8825/brain_state/
./scripts/install.sh  # Runs step 7 only
```

**"Import errors"**
```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r requirements-full.txt
```

---

## Post-Installation

### **Next Steps:**

1. **Read QUICKSTART.md** - Get started in 5 minutes
2. **Set up accountability loops** - Track your goals
3. **Configure meeting automation** - Process transcripts
4. **Explore protocols** - Learn workflow system

### **Recommended Setup:**

```bash
# 1. Add accountability loop
python3 8825_core/agents/accountability_loop_agent.py --add "Daily Goals" \
  --description "Track daily progress" \
  --metric-name "Tasks" \
  --metric-target 3 \
  --metric-unit "per day"

# 2. Test meeting automation
cd 8825_core/workflows/meeting_automation
python3 process_meetings.py --help

# 3. Export brain learnings
cd 8825_core/agents
python3 brain_learning_exporter.py --format markdown
```

---

## Uninstallation

```bash
# Remove system
rm -rf 8825-system/

# Remove config (optional)
rm -rf ~/.8825/

# Remove virtual environment
rm -rf venv/
```

---

## Getting Help

**Documentation:**
- `QUICKSTART.md` - Quick start guide
- `SYSTEM_REQUIREMENTS.md` - System requirements
- `8825_core/protocols/README.md` - Workflow protocols
- `8825_core/agents/README.md` - Agent system

**Support:**
- Check `FAQ.md` (coming soon)
- Review troubleshooting section above
- Open an issue (if using GitHub)

---

## Appendix

### **Manual Installation**

If `install.sh` doesn't work:

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements-full.txt

# 3. Create directories
mkdir -p ~/.8825/brain_state

# 4. Create .env
cp .env.template .env
nano .env  # Edit paths and API key

# 5. Initialize brain
echo '{"initialized_at":"'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'","version":"3.1.0","learnings":[],"memories":[],"last_sync":null}' > ~/.8825/brain_state/state.json
```

### **Environment Variables Reference**

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | OpenAI API key |
| `SYSTEM_ROOT` | No | `~/8825-system` | System directory |
| `DROPBOX_ROOT` | No | `~/Dropbox` | Dropbox directory |
| `DOWNLOADS_DIR` | No | `~/Downloads` | Downloads directory |
| `USER_NAME` | No | Current user | Username |
| `CONFIG_DIR` | No | `~/.8825` | Config directory |

---

**Installation complete! See QUICKSTART.md to get started.**
