# Jh Mode Quick Start

**Personal workspace for Justin Harmon**

---

## 🚀 Activation

### Enter Jh Mode
```
focus on jh
```

### Exit Jh Mode
```
exit focus
```

---

## 📋 Common Commands

### Project Management
```bash
# List all projects
ls projects/

# Create new project
mkdir projects/[project_name]
cd projects/[project_name]

# Archive project
mv projects/[project_name] archive/
```

### Note Taking
```bash
# Create new note
touch notes/[note_name].md

# Edit note
open notes/[note_name].md

# List all notes
ls notes/
```

### Scripts
```bash
# Create new script
touch scripts/[script_name].py
chmod +x scripts/[script_name].py

# Run script
python3 scripts/[script_name].py

# List scripts
ls scripts/
```

---

## 🎨 Workflows

### Start New Project
1. `mkdir projects/[name]`
2. `cd projects/[name]`
3. Create README.md
4. Set up project structure
5. Start working!

### Quick Note
1. `touch notes/[topic].md`
2. Add content
3. Save and commit

### Custom Script
1. `touch scripts/[name].py`
2. Write script
3. Test it
4. Document in README

---

## 📂 Folder Structure

```
Jh_sandbox/
├── projects/     # Active projects
├── notes/        # Personal notes
├── scripts/      # Custom tools
├── templates/    # Reusable templates
└── archive/      # Completed work
```

---

## 💡 Tips

- Use markdown for all documentation
- Keep projects organized in subfolders
- Archive completed work regularly
- Document scripts for future reference
- Link related notes together

---

## 🔗 Integration

**Available from Jh Mode:**
- All 8825 protocols
- Shared templates and tools
- Connection to other focuses
- System-wide workflows

**Jh-Specific:**
- Personal projects
- Private notes
- Custom scripts
- Individual templates

---

## 🎯 Quick Actions

### Create Project Structure
```bash
mkdir -p projects/[name]/{docs,src,tests}
touch projects/[name]/README.md
```

### Create Note with Template
```bash
cat > notes/[topic].md << 'EOF'
# [Topic]

**Date:** $(date +%Y-%m-%d)
**Tags:** 

---

## Notes

[Your content here]

---

## Links

- 
EOF
```

### Create Python Script Template
```bash
cat > scripts/[name].py << 'EOF'
#!/usr/bin/env python3
"""
[Script Description]
"""

def main():
    print("Script running...")

if __name__ == "__main__":
    main()
EOF
chmod +x scripts/[name].py
```

---

**Jh Mode is ready for your personal work!** 🚀
