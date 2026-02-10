# Agent Files Update Action List for v2.0.0

## Status Check: 6 Agent Files

### ✅ 1. content-generator.md - ALREADY UPDATED
**Status:** Clean ✓
- Already mentions JSON output only
- No word count references
- No DOCX output
- Correctly states "Typst rendering pipeline handles ALL formatting"
- **Action:** None needed

### ⚠️ 2. hr-critic.md - PARTIALLY UPDATED
**Status:** Needs cleanup
**Issues found:**
- Line ~167, 223: JSON examples still contain `"word_count": 520` fields
- Line 251: "### Triage Principles" heading remnant

**Actions needed:**
1. Remove or update JSON examples that contain word_count fields
2. Clean up any remaining triage section fragments
3. Verify all 3 modes reduced to 2 modes

### ⚠️ 3. coverage-mapper.md - NEEDS UPDATE
**Status:** Has v1.0 reference
**Issues found:**
- Line 328: "Helps compression-strategist know which bullets are critical"

**Actions needed:**
1. Remove compression-strategist reference
2. Update to: "Helps prioritize which experiences are most relevant"
3. Scan for any other compression/word budget references

### ✅ 4. ats-analyzer.md - CLEAN
**Status:** Clean ✓
- No word count references
- No compression references
- No DOCX output concerns
- Pure JD analysis (unchanged between v1/v2)
- **Action:** None needed

### ✅ 5. interview-conductor.md - CLEAN
**Status:** Clean ✓
- No word count references
- No compression references
- Pure question generation (unchanged between v1/v2)
- **Action:** None needed

### ✅ 6. resume-parser.md - CLEAN (DOCX is intentional)
**Status:** Clean ✓
- Mentions DOCX parsing - this is CORRECT
  - v2.0 still parses DOCX in Phase 1 (database building)
  - Only Phase 2 output changed to PDF
- No word count references
- No compression references
- **Action:** None needed

---

## Summary

**Clean files:** 4/6
- content-generator.md ✓
- ats-analyzer.md ✓
- interview-conductor.md ✓
- resume-parser.md ✓

**Need updates:** 2/6
- hr-critic.md - Remove word_count from JSON examples, clean up triage remnants
- coverage-mapper.md - Remove compression-strategist reference

---

## Detailed Actions

### Action 1: Fix hr-critic.md

**Remove/Update these JSON examples:**

Line ~167-197: JSON example with word_count fields
```json
{
  "mode": "triage",  // REMOVE
  "word_count": 520,  // REMOVE
  ...
}
```

Line ~221-248: Another JSON example with word_count
```json
{
  "mode": "triage",  // REMOVE
  "word_count": 495,  // REMOVE
  ...
}
```

**Solution:** Remove these entire JSON example blocks as they're for the deleted triage mode.

### Action 2: Fix coverage-mapper.md

**Line 328:** Change
```
- Helps compression-strategist know which bullets are critical
```
To:
```
- Helps content-generator prioritize which experiences to emphasize
```

---

## Verification Checklist

After updates:
- [ ] hr-critic.md: No word_count in any JSON examples
- [ ] hr-critic.md: No triage references
- [ ] hr-critic.md: Only 2 modes (comprehensive, final_validation)
- [ ] coverage-mapper.md: No compression-strategist references
- [ ] All 6 agents: grep for "word.count|compression|triage" returns 0 results
- [ ] Commit and push changes

---

## Implementation Order

1. Fix coverage-mapper.md (simple 1-line change)
2. Fix hr-critic.md (remove JSON example blocks)
3. Verify with grep across all files
4. Commit and push
