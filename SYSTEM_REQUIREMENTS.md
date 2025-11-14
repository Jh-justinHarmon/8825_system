# 8825 System Requirements

**Version:** 3.1.0  
**Last Updated:** 2025-11-13

---

## Operating System

### **Supported:**
- ✅ **macOS** 12.0+ (Monterey or later)
- ✅ **Linux** (Ubuntu 20.04+, Debian 11+)

### **Not Supported:**
- ❌ **Windows** (not tested, may work with WSL2)

---

## Software Requirements

### **Required:**

#### **1. Python**
- **Version:** 3.10 or higher
- **Check:** `python3 --version`
- **Install (macOS):** `brew install python@3.10`
- **Install (Linux):** `sudo apt install python3.10`

#### **2. pip**
- **Version:** 23.0 or higher
- **Check:** `pip3 --version`
- **Upgrade:** `python3 -m pip install --upgrade pip`

#### **3. Git**
- **Version:** 2.30 or higher
- **Check:** `git --version`
- **Install (macOS):** `brew install git`
- **Install (Linux):** `sudo apt install git`

---

### **Optional (for specific features):**

#### **4. Tesseract OCR**
**Required for:** Bill processing (Phil's Book)
- **Check:** `tesseract --version`
- **Install (macOS):** `brew install tesseract`
- **Install (Linux):** `sudo apt install tesseract-ocr`

#### **5. Playwright Browsers**
**Required for:** Screenshot generation, web automation
- **Install:** `python3 -m playwright install chromium`
- **Size:** ~300MB

#### **6. Node.js** (if using MCP servers)
**Required for:** MCP server development
- **Version:** 18.0 or higher
- **Check:** `node --version`
- **Install (macOS):** `brew install node`
- **Install (Linux):** `sudo apt install nodejs npm`

---

## API Keys & Credentials

### **Required:**

#### **1. OpenAI API Key**
**Required for:** All AI features (brain, agents, protocols)
- **Get key:** https://platform.openai.com/api-keys
- **Cost:** ~$5-20/month for typical usage
- **Set in:** `.env` file as `OPENAI_API_KEY`

### **Optional:**

#### **2. Google OAuth Credentials**
**Required for:** Gmail, Calendar, Drive integrations
- **Get credentials:** https://console.cloud.google.com/
- **Scopes needed:**
  - Gmail: `gmail.modify`
  - Calendar: `calendar.events`
  - Drive: `drive.file`
- **Set in:** `credentials.json` + `token.json`

#### **3. Reddit API Credentials**
**Required for:** Reddit integration (beta tester evaluation)
- **Get credentials:** https://www.reddit.com/prefs/apps
- **Set in:** `.env` file as `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`

---

## Storage Requirements

### **Disk Space:**
- **Minimum:** 500 MB (core system)
- **Recommended:** 2 GB (with data and logs)
- **With brain history:** 5 GB+ (grows over time)

### **Memory:**
- **Minimum:** 4 GB RAM
- **Recommended:** 8 GB RAM (for concurrent operations)

---

## Network Requirements

### **Internet Connection:**
- **Required for:**
  - OpenAI API calls
  - Google API calls
  - Package installation
  - MCP server communication

### **Ports:**
- **5000-5010:** MCP servers (local only)
- **No inbound ports required**

---

## Python Package Dependencies

See `requirements-full.txt` for complete list.

### **Core packages:**
```
openai>=1.0.0
python-dotenv>=1.0.0
requests>=2.31.0
```

### **Google integration:**
```
google-auth>=2.23.0
google-auth-oauthlib>=1.1.0
google-api-python-client>=2.100.0
```

### **Document processing:**
```
python-docx>=0.8.11
pillow>=10.0.0
pytesseract>=0.3.10
```

### **Web automation:**
```
playwright>=1.40.0
flask>=3.0.0
```

---

## Installation Verification

Run this command to check your system:

```bash
./scripts/check_requirements.sh
```

This will verify:
- ✅ Python version
- ✅ Required packages
- ✅ Optional dependencies
- ✅ API key configuration
- ✅ Directory permissions

---

## Troubleshooting

### **Python version too old:**
```bash
# macOS
brew install python@3.10
brew link python@3.10

# Linux
sudo apt install python3.10 python3.10-venv
```

### **pip install fails:**
```bash
# Upgrade pip
python3 -m pip install --upgrade pip

# Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-full.txt
```

### **Playwright install fails:**
```bash
# Install system dependencies first (Linux)
sudo apt install libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2

# Then install browsers
python3 -m playwright install chromium
```

### **Tesseract not found:**
```bash
# macOS
brew install tesseract

# Linux
sudo apt install tesseract-ocr

# Verify
tesseract --version
```

---

## Next Steps

After verifying requirements:
1. Run `./scripts/install.sh` to install 8825
2. See `INSTALLATION.md` for setup guide
3. See `QUICKSTART.md` to get started

---

**Questions?** See `docs/FAQ.md` or open an issue.
