# Rive Learning Path for Joju Animations

**Your Profile:** Design expert, some animation experience, complete Rive beginner  
**Goal:** Create interactive animations for Joju  
**Style:** Hands-on tutorials

---

## Phase 1: Rive Fundamentals (2-3 hours)

### Tutorial 1: Interface & Basic Animation (30 min)
**Goal:** Create your first animated shape

1. **Download Rive:** https://rive.app/downloads
2. **Follow along:** https://rive.app/community/doc/getting-started/docLl4XkQxgR
   - Create artboard
   - Draw shapes with pen tool
   - Add bones for rigging
   - Create simple animation timeline
   - Export as .riv file

**Practice Exercise:**
- Animate the Joju logo appearing (fade in + scale)
- 2 second loop
- Export and save to `joju/animations/logo_intro.riv`

---

### Tutorial 2: State Machines (45 min)
**Goal:** Make animations interactive

1. **Watch:** [State Machine Basics](https://www.youtube.com/watch?v=bZSNXRzXaxg) (Rive official)
2. **Follow tutorial:** https://rive.app/community/doc/state-machine/docvPB8eRFIx
   - Create multiple animation states
   - Add transitions between states
   - Set up inputs (boolean, number, trigger)
   - Test interactivity

**Practice Exercise:**
- Create a button with 3 states: Idle → Hover → Pressed
- Add smooth transitions
- Use boolean input for hover
- Use trigger input for press

---

### Tutorial 3: Listeners & Events (30 min)
**Goal:** Respond to user interactions

1. **Tutorial:** https://rive.app/community/doc/listeners/docBBJE5Bvnx
   - Add click/hover listeners to shapes
   - Connect listeners to state machine inputs
   - Create interactive hotspots

**Practice Exercise:**
- Create an interactive card that flips on click
- Front shows book cover
- Back shows book details
- Smooth flip animation

---

## Phase 2: Joju-Specific Animations (3-4 hours)

### Project 1: Library Card Animation
**Use Case:** User adds book to library

**Build:**
- Book icon flies into library shelf
- Shelf glows/pulses briefly
- Success checkmark appears
- All triggered by "add_book" input

**Skills:** Paths, transforms, state machines, timing

---

### Project 2: Search Loading State
**Use Case:** AI is processing search query

**Build:**
- Animated search icon with pulsing rings
- Smooth loop (no jarring restart)
- Can be triggered/stopped via state machine
- Matches Joju brand colors

**Skills:** Loops, smooth transitions, color management

---

### Project 3: Empty State Illustration
**Use Case:** User has no books yet

**Build:**
- Animated character reading
- Subtle movements (page turn, eye blink)
- Idle loop that feels alive but not distracting
- CTA button with hover state

**Skills:** Character animation, subtle motion, idle states

---

### Project 4: Onboarding Flow
**Use Case:** First-time user walkthrough

**Build:**
- 3-step animated sequence
- Progress indicator
- Forward/back navigation
- Each step has enter/exit animations

**Skills:** Multi-state machines, complex transitions, sequencing

---

## Phase 3: Integration & Optimization (1-2 hours)

### Tutorial 4: Rive in React
**Goal:** Use animations in Joju app

1. **Install:** `npm install @rive-app/react-canvas`
2. **Follow:** https://rive.app/community/doc/react/docYTRZ8bYx
3. **Implement:**
   ```jsx
   import { useRive } from '@rive-app/react-canvas';
   
   function JojuButton() {
     const { RiveComponent, rive } = useRive({
       src: '/animations/button.riv',
       stateMachines: 'State Machine 1',
       autoplay: true,
     });
     
     return <RiveComponent />;
   }
   ```

**Practice Exercise:**
- Add your button animation to a test React component
- Trigger state changes on real hover/click
- Control animation via props

---

### Tutorial 5: Performance & Export
**Goal:** Optimize for production

1. **Learn:** https://rive.app/community/doc/optimization/docCJbTXLxy
   - Reduce file size
   - Optimize bones/vertices
   - Use runtime efficiently
   - Lazy loading

**Practice Exercise:**
- Audit your animations for file size
- Optimize largest animation by 50%
- Set up lazy loading for non-critical animations

---

## Resources

### Official Rive Resources
- **Docs:** https://rive.app/community/doc
- **YouTube:** https://www.youtube.com/@Rive_app
- **Community:** https://rive.app/community
- **Examples:** https://rive.app/community/files

### Inspiration
- **Rive Community Files:** Browse for UI animation patterns
- **Joju Competitors:** Note what animations they use
- **Dribbble:** Search "micro-interactions" for ideas

### Quick Reference
- **Keyboard Shortcuts:** https://rive.app/community/doc/keyboard-shortcuts/docMPVPcXlBx
- **State Machine Cheatsheet:** Create your own as you learn

---

## Joju Animation Priorities

Based on Joju's needs, focus on these animation types:

1. **Micro-interactions** (buttons, toggles, inputs)
2. **Loading states** (search, AI processing)
3. **Empty states** (no books, no results)
4. **Success/error feedback** (book added, save failed)
5. **Onboarding flows** (first-time user)
6. **Delight moments** (achievements, milestones)

---

## Progress Tracker

- [ ] Phase 1, Tutorial 1: Interface & Basic Animation
- [ ] Phase 1, Tutorial 2: State Machines
- [ ] Phase 1, Tutorial 3: Listeners & Events
- [ ] Phase 2, Project 1: Library Card Animation
- [ ] Phase 2, Project 2: Search Loading State
- [ ] Phase 2, Project 3: Empty State Illustration
- [ ] Phase 2, Project 4: Onboarding Flow
- [ ] Phase 3, Tutorial 4: Rive in React
- [ ] Phase 3, Tutorial 5: Performance & Export

---

## Next Steps

1. **Start now:** Download Rive and do Tutorial 1
2. **Save work:** Create `joju/animations/` folder for .riv files
3. **Document:** Screenshot your progress for team
4. **Share:** Post animations in Joju channel for feedback

**Estimated Total Time:** 6-9 hours to complete all phases

**Ready to start?** Begin with Phase 1, Tutorial 1!
