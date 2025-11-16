# 8825 Repository Strategy

**Last Updated:** 2025-11-15

---

## 🎯 Quick Reference

**You are in:** `8825-system` (PUBLIC OPEN-SOURCE REPO)

**⚠️ DO NOT EDIT FILES DIRECTLY HERE**

This repo is a curated mirror of `8825-Jh` (private).

---

## 📂 Repository Layout

| Directory | Remote | Role |
|-----------|--------|------|
| **`8825-Jh`** | `8825_Jh.git` (PRIVATE) | Primary development |
| **`8825-system`** | `8825_system.git` (PUBLIC) | Open-source mirror (YOU ARE HERE) |
| **`8825_test/installer`** | `8825_system.git` (PUBLIC) | Test clone |

---

## 🌐 This is the Public Repo

### What's Here
- Integration framework
- UI templates
- Public documentation
- Installer scripts
- Generic protocols

### What's NOT Here
- API keys, tokens
- Customer data
- Brain state
- Personal configs
- Proprietary strategies

---

## 🛠️ How to Update This Repo

### NEVER Edit Directly

If you need to make changes:
1. Go to `8825-Jh` (private repo)
2. Make changes there
3. Test thoroughly
4. Export to this repo using publish workflow

### Publish Workflow

```bash
# From 8825-system directory
cd ~/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/8825-system

# Update from remote
git pull origin main

# Export from private
PRIVATE="../8825-Jh"

rsync -av --delete "$PRIVATE/8825_core/integration_server.py" 8825_core/
rsync -av --delete "$PRIVATE/8825_core/workflows/meeting_automation/"*.html 8825_core/workflows/meeting_automation/
rsync -av --delete "$PRIVATE/8825_core/workflows/meeting_automation/"*INTEGRATION*.md 8825_core/workflows/meeting_automation/
rsync -av --delete "$PRIVATE/8825_core/PORT_REGISTRY.md" 8825_core/
rsync -av --delete "$PRIVATE/README_GITHUB.md" ./

# Review
git status
git diff

# Check for secrets
git diff | grep -i "api_key\|token\|password\|secret\|sk-\|AIzaSy"

# Push if clean
git add -A
git commit -m "chore: sync from private repo"
git push origin main
```

---

## 🚨 Before Every Push

### Security Checklist
- [ ] No API keys in diff
- [ ] No customer names/data
- [ ] No brain state files
- [ ] No `.env` files
- [ ] No personal configs
- [ ] No proprietary strategies

### Review Command
```bash
git diff | grep -i "api_key\|token\|password\|secret\|sk-\|AIzaSy"
```

If this returns anything, **DO NOT PUSH**.

---

## 📋 Golden Rules

1. **Never edit files here directly**
2. **Always sync from `8825-Jh`**
3. **Review every diff before pushing**
4. **When in doubt, don't push**

---

## 🔗 Links

- **Private Repo:** https://github.com/Jh-justinHarmon/8825_Jh
- **Public Repo:** https://github.com/Jh-justinHarmon/8825_system (YOU ARE HERE)

---

**Remember: This is the PUBLIC face of 8825. Keep it clean and safe.**
