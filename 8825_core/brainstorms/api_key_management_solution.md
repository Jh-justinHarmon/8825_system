# API Key Management: Secure & Scalable Solution

**Created:** 2025-11-12  
**Problem:** Recurring "hidden key challenge" - API keys not accessible across contexts  
**Goal:** Permanent, secure, scalable solution for 8825 system

---

## The Problem

### Current Pain Points

**Symptom:** Every new Cascade chat requires re-entering API keys
- OpenAI API key not found
- Anthropic API key not found
- Other service keys not accessible

**Root Causes:**
1. **Environment variables don't persist** across Cascade sessions
2. **`.env` files are gitignored** (correctly, for security)
3. **No centralized key management** system
4. **Each project has separate `.env`** files
5. **Keys stored in multiple locations** (inconsistent)

**Impact:**
- Friction on every new chat
- Repeated manual key entry
- Risk of exposing keys in chat history
- Inconsistent key availability across projects

---

## The 8825 Philosophy Applied

### Decision Matrix Analysis

**Philosophy Alignment:**
- ✅ Zero maintenance butler (should be automatic)
- ✅ User data sovereignty (keys are user's, not external service)
- ✅ Cloud folder storage (leverage existing Dropbox sync)
- ✅ Practical over perfect (simple solution that works)
- ✅ Breadth-first (solve once, use everywhere)

**User Friction:**
- Current: HIGH (manual entry every chat)
- Target: ZERO (automatic key availability)

**Stability:**
- Must be corruption-resistant
- Must survive system restarts
- Must work across all contexts (Windsurf, Goose, CLI, etc.)

**Efficiency:**
- Fast key retrieval (<10ms)
- No external dependencies
- Works offline

---

## Solution Architecture

### Option 1: Centralized Key Vault (RECOMMENDED)

**Concept:** Single encrypted key store in Dropbox, loaded by all projects

```
~/Hammer Consulting Dropbox/.../8825_keys/
├── vault.json              # Encrypted key storage
├── vault_loader.sh         # Load keys into environment
└── README.md               # Usage instructions
```

**How It Works:**

1. **Storage:** Keys stored in encrypted JSON file in Dropbox
2. **Loading:** Shell script loads keys into environment on demand
3. **Access:** All projects source the loader script
4. **Sync:** Dropbox keeps vault synced across devices

**Implementation:**

```bash
# vault.json (encrypted with user's password)
{
  "openai_api_key": "sk-...",
  "anthropic_api_key": "sk-ant-...",
  "github_token": "ghp_...",
  "mailgun_api_key": "key-...",
  "created": "2025-11-12",
  "last_updated": "2025-11-12"
}

# vault_loader.sh
#!/bin/bash
VAULT_PATH="$HOME/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825_keys/vault.json"

# Decrypt and load keys
if [ -f "$VAULT_PATH" ]; then
  export OPENAI_API_KEY=$(jq -r '.openai_api_key' "$VAULT_PATH")
  export ANTHROPIC_API_KEY=$(jq -r '.anthropic_api_key' "$VAULT_PATH")
  export GITHUB_TOKEN=$(jq -r '.github_token' "$VAULT_PATH")
  # ... etc
  echo "✓ API keys loaded from vault"
else
  echo "✗ Vault not found at $VAULT_PATH"
fi
```

**Pros:**
- ✅ Single source of truth
- ✅ Synced across devices via Dropbox
- ✅ Encrypted at rest
- ✅ Easy to update (edit one file)
- ✅ Works across all projects
- ✅ No external dependencies

**Cons:**
- ⚠️ Requires initial setup
- ⚠️ Password needed for decryption (can cache)
- ⚠️ Must source loader in each shell

---

### Option 2: macOS Keychain Integration

**Concept:** Store keys in macOS Keychain, retrieve programmatically

```bash
# Store key
security add-generic-password \
  -a "$USER" \
  -s "8825_openai_key" \
  -w "sk-..."

# Retrieve key
security find-generic-password \
  -a "$USER" \
  -s "8825_openai_key" \
  -w
```

**How It Works:**

1. **Storage:** Keys stored in macOS Keychain (encrypted by OS)
2. **Loading:** Scripts retrieve keys from Keychain on demand
3. **Access:** System-wide availability
4. **Sync:** iCloud Keychain syncs across Apple devices

**Implementation:**

```bash
# keychain_loader.sh
#!/bin/bash

# Load OpenAI key
export OPENAI_API_KEY=$(security find-generic-password -a "$USER" -s "8825_openai_key" -w 2>/dev/null)

# Load Anthropic key
export ANTHROPIC_API_KEY=$(security find-generic-password -a "$USER" -s "8825_anthropic_key" -w 2>/dev/null)

# Load GitHub token
export GITHUB_TOKEN=$(security find-generic-password -a "$USER" -s "8825_github_token" -w 2>/dev/null)

if [ -n "$OPENAI_API_KEY" ]; then
  echo "✓ API keys loaded from Keychain"
else
  echo "✗ Keys not found in Keychain"
fi
```

**Pros:**
- ✅ OS-level encryption (very secure)
- ✅ iCloud sync across Apple devices
- ✅ No password needed (uses system auth)
- ✅ Native macOS integration
- ✅ Survives system restarts

**Cons:**
- ⚠️ macOS only (not cross-platform)
- ⚠️ Requires Keychain Access permission
- ⚠️ More complex to debug
- ⚠️ Not in Dropbox (separate sync mechanism)

---

### Option 3: Shell Profile Integration

**Concept:** Export keys in shell profile, available in all terminals

```bash
# ~/.zshrc or ~/.bash_profile
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GITHUB_TOKEN="ghp_..."
```

**How It Works:**

1. **Storage:** Keys in shell profile (plain text, but file permissions protect)
2. **Loading:** Automatic on every shell session
3. **Access:** Available in all terminal sessions
4. **Sync:** Manual (edit file on each device)

**Pros:**
- ✅ Simple to implement
- ✅ Automatic loading
- ✅ Works everywhere (terminal, scripts, apps)
- ✅ No external dependencies

**Cons:**
- ❌ Plain text storage (security risk)
- ❌ Not synced across devices
- ❌ Keys in shell history if edited manually
- ❌ Exposed in `env` command output

---

### Option 4: Hybrid Approach (BEST)

**Concept:** Combine Keychain + Dropbox vault + Shell integration

```
Storage Layer:
├── macOS Keychain (primary, encrypted)
└── Dropbox vault (backup, encrypted)

Loading Layer:
├── Shell profile sources loader
└── Loader checks Keychain first, vault second

Access Layer:
├── Environment variables (runtime)
└── Direct API calls (programmatic)
```

**How It Works:**

1. **Primary:** Keys in macOS Keychain (most secure)
2. **Backup:** Encrypted vault in Dropbox (cross-device)
3. **Loading:** Shell profile sources smart loader
4. **Fallback:** If Keychain fails, use vault

**Implementation:**

```bash
# ~/.zshrc
source "$HOME/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825_keys/smart_loader.sh"

# smart_loader.sh
#!/bin/bash

load_from_keychain() {
  OPENAI_API_KEY=$(security find-generic-password -a "$USER" -s "8825_openai_key" -w 2>/dev/null)
  ANTHROPIC_API_KEY=$(security find-generic-password -a "$USER" -s "8825_anthropic_key" -w 2>/dev/null)
  
  if [ -n "$OPENAI_API_KEY" ]; then
    export OPENAI_API_KEY
    export ANTHROPIC_API_KEY
    return 0
  fi
  return 1
}

load_from_vault() {
  VAULT_PATH="$HOME/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825_keys/vault.json"
  if [ -f "$VAULT_PATH" ]; then
    export OPENAI_API_KEY=$(jq -r '.openai_api_key' "$VAULT_PATH")
    export ANTHROPIC_API_KEY=$(jq -r '.anthropic_api_key' "$VAULT_PATH")
    return 0
  fi
  return 1
}

# Try Keychain first, fallback to vault
if load_from_keychain; then
  echo "✓ Keys loaded from Keychain"
elif load_from_vault; then
  echo "✓ Keys loaded from Dropbox vault"
else
  echo "⚠ No API keys found - run: 8825 setup-keys"
fi
```

**Pros:**
- ✅ Best of all worlds
- ✅ Secure (Keychain) + Portable (Dropbox)
- ✅ Automatic fallback
- ✅ Works across devices
- ✅ Easy to maintain

**Cons:**
- ⚠️ More complex setup
- ⚠️ Two storage locations to manage

---

## Recommended Solution: Hybrid Approach

### Implementation Plan

#### Phase 1: Create Key Vault (Week 1)

**Step 1:** Create vault directory
```bash
mkdir -p "$HOME/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825_keys"
cd "$HOME/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825_keys"
```

**Step 2:** Create vault.json (encrypted)
```json
{
  "version": "1.0",
  "created": "2025-11-12",
  "last_updated": "2025-11-12",
  "keys": {
    "openai_api_key": "sk-...",
    "anthropic_api_key": "sk-ant-...",
    "github_token": "ghp_...",
    "mailgun_api_key": "key-...",
    "figma_token": "figd_..."
  },
  "notes": {
    "openai": "Personal account, used for all 8825 projects",
    "anthropic": "Backup LLM for high-quality tasks",
    "github": "Personal access token for repo operations",
    "mailgun": "Email gateway for customer platform",
    "figma": "Figma Make integration token"
  }
}
```

**Step 3:** Create smart_loader.sh
```bash
#!/bin/bash
# 8825 Smart Key Loader
# Loads API keys from Keychain (primary) or Dropbox vault (fallback)

VAULT_PATH="$HOME/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825_keys/vault.json"

# Function: Load from macOS Keychain
load_from_keychain() {
  local openai=$(security find-generic-password -a "$USER" -s "8825_openai_key" -w 2>/dev/null)
  local anthropic=$(security find-generic-password -a "$USER" -s "8825_anthropic_key" -w 2>/dev/null)
  local github=$(security find-generic-password -a "$USER" -s "8825_github_token" -w 2>/dev/null)
  
  if [ -n "$openai" ]; then
    export OPENAI_API_KEY="$openai"
    export ANTHROPIC_API_KEY="$anthropic"
    export GITHUB_TOKEN="$github"
    return 0
  fi
  return 1
}

# Function: Load from Dropbox vault
load_from_vault() {
  if [ -f "$VAULT_PATH" ]; then
    export OPENAI_API_KEY=$(jq -r '.keys.openai_api_key' "$VAULT_PATH")
    export ANTHROPIC_API_KEY=$(jq -r '.keys.anthropic_api_key' "$VAULT_PATH")
    export GITHUB_TOKEN=$(jq -r '.keys.github_token' "$VAULT_PATH")
    export MAILGUN_API_KEY=$(jq -r '.keys.mailgun_api_key' "$VAULT_PATH")
    export FIGMA_TOKEN=$(jq -r '.keys.figma_token' "$VAULT_PATH")
    return 0
  fi
  return 1
}

# Try Keychain first, fallback to vault
if load_from_keychain; then
  echo "✓ 8825 keys loaded from Keychain" >&2
elif load_from_vault; then
  echo "✓ 8825 keys loaded from Dropbox vault" >&2
else
  echo "⚠ No API keys found - run: 8825 setup-keys" >&2
  return 1
fi
```

**Step 4:** Add to shell profile
```bash
# Add to ~/.zshrc
echo 'source "$HOME/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825_keys/smart_loader.sh"' >> ~/.zshrc
```

#### Phase 2: Populate Keychain (Week 1)

**Create setup script:**
```bash
# setup_keys.sh
#!/bin/bash

echo "🔐 Setting up 8825 API Keys"
echo

# OpenAI
read -sp "Enter OpenAI API key: " openai_key
echo
security add-generic-password -U -a "$USER" -s "8825_openai_key" -w "$openai_key"

# Anthropic
read -sp "Enter Anthropic API key: " anthropic_key
echo
security add-generic-password -U -a "$USER" -s "8825_anthropic_key" -w "$anthropic_key"

# GitHub
read -sp "Enter GitHub token: " github_token
echo
security add-generic-password -U -a "$USER" -s "8825_github_token" -w "$github_token"

echo
echo "✓ Keys stored in Keychain"
echo "✓ Keys will be available in all new terminal sessions"
```

#### Phase 3: Update All Projects (Week 1)

**For each project with `.env`:**

1. Remove hardcoded keys from `.env`
2. Add loader to project startup
3. Test key availability

**Example for customer platform:**
```bash
# In 8825_customers/package.json
"scripts": {
  "prestart": "source ~/Hammer\\ Consulting\\ Dropbox/Justin\\ Harmon/Public/8825/8825_keys/smart_loader.sh",
  "start": "node mcp_server/server.js"
}
```

#### Phase 4: Add to 8825 Startup (Week 1)

**Update `8825_unified_startup.sh`:**
```bash
# Load API keys
source "$HOME/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825_keys/smart_loader.sh"

# Verify keys loaded
if [ -z "$OPENAI_API_KEY" ]; then
  echo "⚠ Warning: OPENAI_API_KEY not loaded"
  echo "  Run: 8825 setup-keys"
fi
```

---

## Security Considerations

### Encryption Options

**Option A: No Encryption (Simple)**
- Store keys in plain JSON
- Rely on file permissions (600)
- Dropbox encryption at rest

**Option B: GPG Encryption (Moderate)**
```bash
# Encrypt vault
gpg --symmetric --cipher-algo AES256 vault.json

# Decrypt on load
gpg --decrypt vault.json.gpg | jq -r '.keys.openai_api_key'
```

**Option C: Password-Based Encryption (Strong)**
```bash
# Encrypt with password
openssl enc -aes-256-cbc -salt -in vault.json -out vault.json.enc

# Decrypt on load
openssl enc -aes-256-cbc -d -in vault.json.enc
```

**Recommendation:** Start with Option A (plain JSON with file permissions), upgrade to Option B if needed.

### File Permissions

```bash
# Vault directory
chmod 700 ~/Hammer\ Consulting\ Dropbox/.../8825_keys/

# Vault file
chmod 600 ~/Hammer\ Consulting\ Dropbox/.../8825_keys/vault.json

# Loader script
chmod 700 ~/Hammer\ Consulting\ Dropbox/.../8825_keys/smart_loader.sh
```

### Gitignore Protection

```bash
# Add to all .gitignore files
8825_keys/
vault.json
*.env
.env*
```

---

## Cascade/Windsurf Integration

### Problem: Cascade Doesn't Inherit Shell Environment

**Why keys aren't available:**
- Cascade runs in separate process
- Doesn't source shell profile
- Environment variables not inherited

**Solution: Explicit Loading**

**Option 1: Load in Cascade startup**
```javascript
// In Cascade initialization
const { execSync } = require('child_process');
const keys = execSync('source ~/path/to/smart_loader.sh && env | grep API_KEY').toString();
// Parse and set process.env
```

**Option 2: Direct vault access**
```javascript
// In Cascade initialization
const vault = JSON.parse(fs.readFileSync('~/path/to/vault.json'));
process.env.OPENAI_API_KEY = vault.keys.openai_api_key;
```

**Option 3: Add to Windsurf settings**
```json
// .windsurf/settings.json
{
  "terminal.integrated.env.osx": {
    "OPENAI_API_KEY": "${env:OPENAI_API_KEY}"
  }
}
```

---

## Maintenance & Updates

### Adding New Keys

```bash
# Add to Keychain
security add-generic-password -U -a "$USER" -s "8825_new_service_key" -w "key-value"

# Add to vault
jq '.keys.new_service_key = "key-value"' vault.json > vault.tmp && mv vault.tmp vault.json

# Update loader script
# Add export line for new key
```

### Rotating Keys

```bash
# Update Keychain
security delete-generic-password -a "$USER" -s "8825_openai_key"
security add-generic-password -a "$USER" -s "8825_openai_key" -w "new-key"

# Update vault
jq '.keys.openai_api_key = "new-key" | .last_updated = "2025-11-12"' vault.json > vault.tmp && mv vault.tmp vault.json
```

### Backup & Recovery

```bash
# Backup vault
cp vault.json vault.backup.$(date +%Y%m%d).json

# Export from Keychain
security find-generic-password -a "$USER" -s "8825_openai_key" -w > openai_key.backup.txt

# Restore to Keychain
security add-generic-password -U -a "$USER" -s "8825_openai_key" -w "$(cat openai_key.backup.txt)"
```

---

## Testing Plan

### Phase 1: Vault Creation
- [ ] Create vault directory
- [ ] Create vault.json with test keys
- [ ] Set file permissions
- [ ] Verify Dropbox sync

### Phase 2: Loader Script
- [ ] Create smart_loader.sh
- [ ] Test Keychain loading
- [ ] Test vault loading
- [ ] Test fallback logic

### Phase 3: Shell Integration
- [ ] Add to ~/.zshrc
- [ ] Open new terminal, verify keys loaded
- [ ] Test in existing terminal (source manually)

### Phase 4: Project Integration
- [ ] Update customer platform
- [ ] Update HCSS sandbox
- [ ] Update Joju project
- [ ] Test each project

### Phase 5: Cascade Integration
- [ ] Test key availability in Cascade
- [ ] Add explicit loading if needed
- [ ] Verify across multiple chats

---

## Success Criteria

**Zero Friction:**
- ✅ Keys available in all new terminal sessions
- ✅ Keys available in all Cascade chats
- ✅ No manual key entry required

**Secure:**
- ✅ Keys encrypted at rest (Keychain)
- ✅ Proper file permissions (vault)
- ✅ Not in git history

**Scalable:**
- ✅ Easy to add new keys
- ✅ Easy to rotate keys
- ✅ Works across all projects

**Maintainable:**
- ✅ Single source of truth (vault)
- ✅ Automatic sync (Dropbox)
- ✅ Simple backup/restore

---

## Timeline

**Week 1 (Now):**
- Day 1: Create vault + loader script
- Day 2: Populate Keychain
- Day 3: Test shell integration
- Day 4: Update all projects
- Day 5: Test Cascade integration

**Week 2:**
- Monitor for issues
- Refine as needed
- Document learnings

---

## Alternative: 8825 Command Integration

**Add to 8825 governance system:**

```bash
# 8825 setup-keys
# Interactive key setup

# 8825 rotate-key <service>
# Rotate specific key

# 8825 test-keys
# Verify all keys are accessible

# 8825 backup-keys
# Backup vault to timestamped file
```

---

## Recommendation

**Implement Hybrid Approach (Option 4):**

1. **Primary:** macOS Keychain (most secure, automatic)
2. **Backup:** Dropbox vault (portable, synced)
3. **Loading:** Smart loader with fallback
4. **Integration:** Shell profile + 8825 startup

**Why:**
- ✅ Solves the problem permanently
- ✅ Secure (Keychain encryption)
- ✅ Portable (Dropbox sync)
- ✅ Zero friction (automatic loading)
- ✅ Scalable (easy to add keys)
- ✅ Aligns with 8825 philosophy

**Time to implement:** 2-3 hours
**Time saved per week:** 1-2 hours (no more manual key entry)
**ROI:** Pays for itself in Week 1

---

## Next Steps

1. Create vault directory and files
2. Populate with current keys
3. Add to shell profile
4. Test in new terminal
5. Update customer platform
6. Test in Cascade
7. Document and create memory

**Ready to implement?**
