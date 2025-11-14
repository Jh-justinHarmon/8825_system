# Sandbox - Experiments & POCs

**Purpose:** Development and experimentation area. Everything starts here.

## What Goes Here

### Characteristics
- New ideas and experiments
- Proof of concepts
- Unstable/changing rapidly
- May or may not graduate
- Can be deleted if experiment fails

## Subdirectories

### `/experimental`
Active experiments and POCs
- New features being developed
- Testing new approaches
- Quick prototypes
- May fail, may succeed

### `/graduated`
Ready for promotion
- Stable and working
- Passed testing
- Ready to move to `shared/` or `focuses/`
- Waiting for promotion review

## Graduation Flow

```
1. Build in sandbox/experimental/
2. Test and refine
3. Move to sandbox/graduated/
4. Review for promotion
5. Promote to shared/ or focuses/ (or back to core/ if universal)
```

## Promotion Criteria

### To Graduate (experimental → graduated):
- [ ] Works reliably
- [ ] No major changes in 7+ days
- [ ] Basic documentation exists
- [ ] Has a clear use case

### From Graduated to Production:
- [ ] Used in real workflow (not just testing)
- [ ] Has owner/maintainer
- [ ] Documented
- [ ] Decision on destination (shared/ or focuses/)

## Monthly Review

Every month, review sandbox contents:
- **Active experiments** → Keep in experimental/
- **Stable POCs** → Graduate or promote
- **Abandoned** → Delete (with note in deletion log)
- **In production** → MUST promote (no production code in sandbox!)

## Examples

**Experiment:**
```
sandbox/experimental/new-automation-idea/
└── quick_prototype.py
```

**Graduated:**
```
sandbox/graduated/meeting-automation/
├── README.md
├── automation.py
├── test_automation.py
└── READY_FOR_PROMOTION.txt
```

## Rules

1. **Everything new starts in experimental/**
2. **Nothing stays in sandbox longer than 60 days without review**
3. **Production code MUST be promoted**
4. **Failed experiments get deleted (with log entry)**
5. **Graduated items must move within 14 days**

## NOT in Sandbox

- Production code → `shared/` or `focuses/`
- System essentials → `core/`
- User personal work → `users/`
