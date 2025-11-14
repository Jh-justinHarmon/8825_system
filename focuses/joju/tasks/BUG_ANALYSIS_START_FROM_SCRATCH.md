# 🐛 Bug Analysis: "Start from Scratch" Wipes User Data

**Date:** November 10, 2025  
**Severity:** ⚠️ **CRITICAL** - Data Loss Risk  
**Status:** Confirmed in Code  
**Task:** "Start from Scratch" wipes user data on homepage

---

## 📍 Bug Location

### Found in 2 files:
1. **`src/pages/Index.tsx`** (line 217-228)
2. **`src/pages/ProfilePage.tsx`** (line 155-173)

---

## 🔍 Code Analysis

### Current Implementation

```typescript
// In Index.tsx (Homepage)
<Button
  variant="outline"
  onClick={() => {
    setCVData(BLANK_TEMPLATE);  // ⚠️ Immediately wipes data
    navigate('/local-profile');
  }}
>
  START FROM SCRATCH
</Button>

// In ProfilePage.tsx
<Button
  variant="outline"
  onClick={() => {
    setCVData(BLANK_TEMPLATE);  // ⚠️ Immediately wipes data
    navigate('/profile');
  }}
>
  START FROM SCRATCH
</Button>
```

---

## ⚠️ THE PROBLEM

### What Happens:
1. User clicks "START FROM SCRATCH" button
2. **Immediately** calls `setCVData(BLANK_TEMPLATE)`
3. Replaces all CV data with blank template
4. Navigates to profile page
5. **NO CONFIRMATION DIALOG**
6. **NO UNDO OPTION**
7. **DATA IS LOST**

### Why It's Critical:
- ❌ **No warning** before data deletion
- ❌ **No confirmation dialog**
- ❌ **No "Are you sure?" prompt**
- ❌ **Immediate data loss**
- ❌ **No undo functionality**
- ❌ **User may click by accident**

---

## 🔬 Technical Details

### What `setCVData(BLANK_TEMPLATE)` Does:

1. **Replaces entire CV data** with blank template
2. **Triggers auto-save** to localStorage (if in demo mode)
3. **Overwrites** `joju_demo_profile` in localStorage
4. **Syncs to Supabase** (if authenticated)

### Data Flow:
```
User Click
    ↓
setCVData(BLANK_TEMPLATE)
    ↓
CVContext updates state
    ↓
Auto-save triggered (if enabled)
    ↓
localStorage.setItem('joju_demo_profile', BLANK_TEMPLATE)
    ↓
USER DATA LOST ❌
```

---

## 🎯 Impact Assessment

### Who's Affected:
- **All users** on homepage or profile page
- **Demo mode users** (localStorage)
- **Authenticated users** (Supabase)

### Data at Risk:
- ✅ All CV sections (work, education, skills, etc.)
- ✅ Profile information
- ✅ Custom achievements
- ✅ Uploaded media
- ✅ All user customizations

### Scenarios:
1. **Accidental click** - User meant to click something else
2. **Misunderstanding** - User doesn't realize it wipes data
3. **Testing** - User clicks to "see what happens"
4. **Mobile tap** - Easier to accidentally tap on mobile

---

## ✅ Recommended Fix

### Option 1: Confirmation Dialog (RECOMMENDED)

```typescript
// Add confirmation dialog
<Button
  variant="outline"
  onClick={() => {
    // Show confirmation dialog
    if (confirm(
      "⚠️ WARNING: This will delete ALL your current data.\n\n" +
      "Are you sure you want to start from scratch?\n\n" +
      "This action cannot be undone."
    )) {
      setCVData(BLANK_TEMPLATE);
      navigate('/local-profile');
    }
  }}
>
  START FROM SCRATCH
</Button>
```

### Option 2: Modal with Explicit Confirmation (BETTER)

```typescript
// Use a proper modal component
const handleStartFromScratch = () => {
  setShowConfirmModal(true);
};

// In modal:
<AlertDialog>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>⚠️ Delete All Data?</AlertDialogTitle>
      <AlertDialogDescription>
        This will permanently delete all your current CV data including:
        • Work experience
        • Education
        • Skills
        • Projects
        • All other sections
        
        This action cannot be undone.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction 
        className="bg-red-600"
        onClick={() => {
          setCVData(BLANK_TEMPLATE);
          navigate('/local-profile');
        }}
      >
        Yes, Delete Everything
      </AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

### Option 3: Backup Before Wipe (BEST)

```typescript
const handleStartFromScratch = async () => {
  // Create backup first
  const backup = {
    data: cvData,
    timestamp: new Date().toISOString()
  };
  
  // Save backup to localStorage
  localStorage.setItem('joju_last_backup', JSON.stringify(backup));
  
  // Show confirmation
  const confirmed = confirm(
    "⚠️ WARNING: This will delete ALL your current data.\n\n" +
    "A backup will be saved. You can restore it from Settings.\n\n" +
    "Continue?"
  );
  
  if (confirmed) {
    setCVData(BLANK_TEMPLATE);
    navigate('/local-profile');
    
    // Show toast with undo option
    toast({
      title: "Data cleared",
      description: "Your previous data has been backed up.",
      action: <Button onClick={restoreBackup}>Undo</Button>
    });
  }
};
```

---

## 🧪 Testing Checklist

### Before Fix:
- [x] Confirmed button exists in Index.tsx
- [x] Confirmed button exists in ProfilePage.tsx
- [x] Verified no confirmation dialog
- [x] Verified immediate data wipe
- [x] Confirmed localStorage overwrite

### After Fix:
- [ ] Confirmation dialog appears
- [ ] User can cancel action
- [ ] Data only wiped after confirmation
- [ ] Backup created before wipe
- [ ] Undo option available
- [ ] Toast notification shown
- [ ] Works in both locations (Index & ProfilePage)

---

## 📝 Implementation Steps

### 1. Create Confirmation Component
```bash
# Add AlertDialog if not already present
# Check if shadcn/ui alert-dialog is installed
```

### 2. Update Index.tsx
- Add confirmation dialog
- Add backup logic
- Add undo functionality

### 3. Update ProfilePage.tsx
- Same changes as Index.tsx
- Keep consistent UX

### 4. Add Backup System
- Create backup before wipe
- Store in localStorage
- Add restore function
- Add UI for restore

### 5. Add Tests
- Test confirmation appears
- Test cancel works
- Test backup created
- Test restore works

---

## 🚨 Severity Justification

### Why This is CRITICAL:

1. **Data Loss** - Permanent loss of user work
2. **No Warning** - User not informed of consequences
3. **No Undo** - Cannot recover after action
4. **Easy to Trigger** - Single click, no confirmation
5. **High Impact** - Affects all user data
6. **User Trust** - Damages trust in application

### Comparison:
- Similar to "Delete Account" button with no confirmation
- Like "Format Drive" with one click
- Equivalent to "Clear All" in a text editor

---

## 📊 Risk Assessment

**Likelihood:** High (prominent button, easy to click)  
**Impact:** Critical (complete data loss)  
**Overall Risk:** **CRITICAL**

### User Scenarios:
- 😰 "I clicked it by accident!"
- 😰 "I didn't know it would delete everything!"
- 😰 "Can I get my data back?"
- 😰 "I just wanted to see what it does!"

---

## ✅ Acceptance Criteria for Fix

### Must Have:
- [ ] Confirmation dialog before data wipe
- [ ] Clear warning about data loss
- [ ] Cancel button
- [ ] Explicit "Yes, delete" confirmation

### Should Have:
- [ ] Backup created automatically
- [ ] Undo option (at least temporarily)
- [ ] Toast notification
- [ ] Consistent across both pages

### Nice to Have:
- [ ] Restore from backup in settings
- [ ] Multiple backup slots
- [ ] Export before wipe option

---

## 🎯 Recommended Priority

**Priority:** 🔴 **URGENT**

**Rationale:**
- Data loss is unacceptable
- Easy fix (add confirmation)
- High user impact
- Damages trust if not fixed

**Timeline:** Should be fixed ASAP (within 1-2 days)

---

## 📚 Related Issues

- Share link clarity (Medium priority)
- Date validation (Low priority)
- Section reorder (Medium priority)

---

## 🔗 Files to Modify

1. `src/pages/Index.tsx` (lines 217-228)
2. `src/pages/ProfilePage.tsx` (lines 155-173)
3. `src/context/CVContext.tsx` (add backup/restore functions)
4. `src/components/ui/alert-dialog.tsx` (if not exists)

---

## 💡 Additional Recommendations

### 1. Add "Recent Backups" Feature
- Auto-backup before major actions
- Show list of recent backups
- Allow restore from any backup

### 2. Add "Export Before Clear"
- Offer to download current data
- Before wiping everything
- As JSON or PDF

### 3. Add Settings Toggle
- "Confirm destructive actions"
- User preference
- Default: ON

### 4. Add Analytics
- Track how often clicked
- Track cancellation rate
- Understand user behavior

---

## ✅ Conclusion

**Bug Confirmed:** Yes  
**Severity:** Critical  
**Fix Difficulty:** Easy (2-4 hours)  
**User Impact:** High  
**Recommendation:** Fix immediately

**The "Start from Scratch" button is a data loss hazard and should have confirmation before execution.**

---

**Next Steps:**
1. Create confirmation dialog component
2. Add backup system
3. Update both files
4. Test thoroughly
5. Deploy fix
6. Update task status to "Released"
