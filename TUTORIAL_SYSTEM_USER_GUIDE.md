# Tutorial System User Guide
**Learn how to create and use tutorials in the 8825 system**

---

## What is this?

The Tutorial System solves a problem you've experienced: **software tutorials that don't match reality.**

Instead of reading docs that say "click the Settings button" (which button? where?), you get:
- **Step-by-step guidance** with actual screenshots
- **AI validation** that checks if you did it right
- **Self-updating tutorials** that adapt when software UIs change

Think of it as having an expert looking over your shoulder, but available 24/7 and stored in your 8825 system.

---

## Core Concepts (in plain English)

### 1. Tutorial Objects
A tutorial is not a document—it's a **structured, interactive guide** that includes:
- **Goal:** What you'll learn (e.g., "Create a fade animation in Rive")
- **Steps:** Each step has:
  - What to do ("Click the Animate tab")
  - What it should look like (a screenshot with the button highlighted)
  - How to verify you did it right (AI checks your screenshot)

### 2. Capture vs. Use
- **Capture:** Creating a tutorial by recording your steps
- **Use:** Following a tutorial someone else created

You'll mostly **use** tutorials others created, but you can **capture** your own when you figure something out.

### 3. Three Modes of Using Tutorials

**Coach Mode** (Step-by-Step)
- AI shows you one step at a time
- You do it, then send a screenshot or say "done"
- AI verifies and moves you to the next step
- Best for: Learning something completely new

**Co-pilot Mode** (Work at Your Own Pace)
- AI shows you the whole tutorial upfront
- You work on your own
- When stuck, send a screenshot and ask "what's next?"
- AI figures out where you are and tells you the next step
- Best for: You have some experience, just need occasional guidance

**Overview Mode** (Just the Facts)
- AI shows you all steps as a list with thumbnails
- You don't interact, just read
- Best for: Quick reference or deciding if this tutorial is what you need

---

## How to Use a Tutorial (Coach Mode Example)

Let's say you want to learn how to create a fade animation in Rive.

### Step 1: Start the Tutorial
In Cascade chat, type:
```
/tutorial coach rive-fade-animation
```

### Step 2: Follow Along
Cascade responds:
```
📘 Tutorial: Create Fade Animation in Rive
   Goal: Learn to animate text fading in and out

Step 1 of 8: Switch to Animate Mode
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Action: Click the "Animate" tab in the top-right corner of the Rive editor.

[Screenshot showing where "Animate" tab is]

When you've done this, send me a screenshot or say "done".
```

### Step 3: Do It
You open Rive, click the Animate tab, and take a screenshot of your window.

### Step 4: Validate
You send the screenshot to Cascade.

Cascade responds:
```
✅ Step 1 complete! 
   I can see the Animate tab is now active and the Timeline panel appeared.

Step 2 of 8: Create a New Animation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Action: Click the "+" button next to "Animations" in the left panel.

[Screenshot showing where "+" button is]

When you've done this, send me a screenshot or say "done".
```

### Step 5: Repeat
You continue through all 8 steps, getting validated at each stage, until you've completed the tutorial.

---

## How to Create a Tutorial (Capture Mode)

Let's say you just figured out how to do something in a tool, and you want to save it as a tutorial so you (or others) can repeat it easily.

### Step 1: Start Capture
In Cascade chat, type:
```
/tutorial capture start Figma "Create a component from a frame"
```

Cascade responds:
```
📝 Starting tutorial capture...
   Tool: Figma
   Goal: Create a component from a frame

I'll guide you through capturing each step.

Perform the first step of your workflow, then send me a screenshot of the entire window.
```

### Step 2: Do the First Step
You open Figma, select a frame, and take a screenshot.

### Step 3: Send Screenshot
You send the screenshot to Cascade.

Cascade responds:
```
Analyzing screenshot...

I see:
- A frame named "Button" is selected (coordinates: 412, 230)
- The right panel shows "Selection" options
- Text visible: "Button", "Selection", "Design", "Prototype"

What did you do in this step? (Describe it simply, e.g., "Select the frame I want to convert")
```

### Step 4: Describe the Step
You type:
```
Select the frame I want to convert to a component
```

Cascade responds:
```
✓ Step 1 saved.

Title: Select the frame I want to convert to a component
Action Type: click
Target: Frame named "Button"

Ready for the next step?
Type /tutorial capture next to continue, or /tutorial capture done if finished.
```

### Step 5: Repeat for All Steps
You type:
```
/tutorial capture next
```

Then do the next step (e.g., right-click the frame), send screenshot, describe it, and continue until done.

### Step 6: Finalize
When you've captured all steps, type:
```
/tutorial capture done
```

Cascade responds:
```
✅ Tutorial saved!

ID: figma-create-component-v1
Steps: 4
Screenshots: 4

To use this tutorial:
/tutorial coach figma-create-component-v1

To view it:
/tutorial overview figma-create-component-v1
```

---

## What Happens Behind the Scenes?

When you send a screenshot, here's what the AI does:

1. **OCR (Text Recognition)**
   - Scans your screenshot for all visible text
   - Identifies button labels, menu items, panel titles
   - Example: Finds "Animate" at coordinates (1420, 60)

2. **Image Comparison**
   - Compares your screenshot to the stored "correct" screenshot
   - Calculates similarity (0-100%)
   - If >75% similar, considers it a match

3. **Validation**
   - Checks if expected text is visible (e.g., "Timeline" panel should appear)
   - Checks if the UI state changed as expected (e.g., new panel opened)
   - Gives you a thumbs up or actionable feedback

4. **Feedback Generation**
   - If valid: "Step complete! Moving to next step."
   - If invalid: "I don't see the Timeline panel yet. Make sure you clicked the Animate tab in the top-right."

---

## Common Questions

### Q: What if my screenshot doesn't match, but I did it right?
**A:** This happens if:
- Your window size is different
- You're using dark mode vs. light mode
- The software version is different

Solution: The AI will ask if you want to update the tutorial. Say yes, and it will create a new version (v2) with your screenshot, while keeping the old one for others.

### Q: What if I get stuck and the AI doesn't help?
**A:** Two options:
1. **Skip the step:** Type `/tutorial skip` and the AI will move you to the next step
2. **Exit tutorial:** Type `/tutorial exit` and try again later or ask for human help

### Q: Can I edit a tutorial after creating it?
**A:** Not directly (yet). If you notice an error:
1. Create a new capture (it's faster than you think)
2. Or use the "fork" feature to update specific steps (covered in advanced section)

### Q: Do I need to take perfect screenshots?
**A:** No. The AI is forgiving:
- Screenshots can be different window sizes
- Minor differences in layout are okay
- As long as the key elements (buttons, panels) are visible, it will work

### Q: How do I know which tutorials are available?
**A:** Type:
```
/tutorial list
```

Cascade will show you all tutorials, organized by tool. Example:
```
📚 Available Tutorials

Rive (3)
- rive-fade-animation - Create fade in/out text animation
- rive-state-machine - Build interactive button states
- rive-export - Export animations for React

Figma (2)
- figma-create-component - Create a component from a frame
- figma-auto-layout - Set up auto-layout constraints

...
```

---

## Advanced: Understanding Tutorial Versions

Software changes. Buttons move. New features are added. This is why tutorials break.

The 8825 Tutorial System handles this with **versions**.

### How It Works

1. **Original Tutorial (v1)**
   - Created on Nov 15, 2025
   - Rive version 0.9.8
   - Works perfectly... until Rive updates to 0.9.9

2. **UI Changes**
   - Rive 0.9.9 moves the "Animate" tab from top-right to top-left
   - Users on v0.9.9 try the tutorial
   - Validation fails: "I don't see the Animate tab in the top-right"

3. **Fork Prompt**
   - After 3 failed validations, AI asks: "It looks like Rive's UI has changed. Update this tutorial? (yes/no)"
   - User says yes
   - AI enters mini-capture mode: "Send me a screenshot of where the Animate tab is now"

4. **New Version (v2)**
   - Tutorial forked to `rive-fade-animation-v2`
   - Updated to work with Rive 0.9.9
   - Old version (`rive-fade-animation-v1`) still available for users on 0.9.8

### Using Specific Versions

By default, you get the latest version. To use an older version:
```
/tutorial coach rive-fade-animation-v1
```

---

## Tips & Best Practices

### For Creating Tutorials

1. **Keep steps small**
   - One action per step (e.g., "Click the button", not "Click the button, then type text")
   - Easier to follow, easier to validate

2. **Take full-window screenshots**
   - Don't crop to just the button
   - Context matters for validation

3. **Use clear descriptions**
   - Good: "Click the red 'Animate' button in the top-right toolbar"
   - Bad: "Click that thing"

4. **Test your tutorial**
   - After capturing, use it yourself in Coach mode
   - Fix any confusing steps before sharing

### For Using Tutorials

1. **Start with Overview mode**
   - Get the big picture before diving in
   - Decide if this tutorial is what you need

2. **Use Coach mode for first time**
   - Get validation at each step
   - Builds confidence

3. **Switch to Co-pilot mode later**
   - Once you've done it once, you don't need hand-holding
   - Faster workflow

4. **Send screenshots liberally**
   - When in doubt, send a screenshot
   - Better than guessing

---

## Troubleshooting

### "The tutorial doesn't load"
- Check if Tutorial Hub MCP is running: `ps aux | grep tutorial`
- Start it: `./start_all_mcps.sh`

### "Validation always fails, even when I do it right"
- Your software version may be different
- Trigger a fork: intentionally fail 3 times, then say "yes" to update

### "Screenshots take forever to upload"
- Screenshots are large (2-5 MB)
- Compress them first, or the system will auto-compress

### "I can't find the tutorial I want"
- List all: `/tutorial list`
- Search: `/tutorial search <keyword>` (coming in Phase 4)

---

## What's Next?

This system is designed to grow:

### Short-term (Phase 1-3)
- Basic capture, validation, and guidance
- Coach, Co-pilot, Overview modes
- Works for desktop apps with clear UIs

### Medium-term (Phase 4)
- Tutorial forking (self-healing)
- Better error handling
- Performance optimization

### Long-term (Future)
- Web app tutorials (capture via browser extension)
- Mobile app tutorials (capture via screen recording)
- Video playback option (for users who prefer video)
- Community tutorial sharing (8825 tutorial marketplace?)

---

## Getting Started

**Right now, you can:**
1. Review this guide
2. Approve the implementation plan (TUTORIAL_SYSTEM_IMPLEMENTATION_PLAN.md)
3. Help test Phase 0 (OCR and image comparison validation)

**Once built, you'll be able to:**
- Create tutorials for any software you use
- Follow tutorials others create
- Never lose knowledge when you figure something out
- Onboard new team members faster (Joju tutorials, HCSS workflows, etc.)

**Questions?**
Ask in Cascade: "Explain [concept] from the tutorial system"

---

**Status:** System design complete, awaiting approval to begin implementation.
