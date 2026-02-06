---
name: word-counter
description: "Section-by-section word counting tool for DOCX files. Use when you need to: (1) Count words in specific resume sections (header, education, experience, skills), (2) Track word count changes across iterations, (3) Determine if resume fits one-page target (450-550 words), (4) Identify which sections to compress. Essential for the rescume compression workflow where only Experience and Skills sections are editable."
---

# Word Counter - Section-Based Word Counting

A tool skill for counting words by section in DOCX resume files, enabling precise word count optimization.

## Overview

This skill provides section-by-section word counting for resume documents, which is critical for the rescume compression strategy where only certain sections (Experience and Skills) are editable while others (Header, Education) remain fixed.

## Quick Reference

| Task | Command |
|------|---------|
| Count all sections | `count_sections.py resume.docx` |
| Track changes | `track_changes.py --before v1.docx --after v2.docx` |
| Check target | `check_target.py resume.docx --target 475` |
| Get section range | `get_section.py resume.docx --section experience` |

## Word Count Heuristics

**Standard one-page resume**: 450-550 words total
- **Header**: 10-20 words (name, contact info)
- **Education**: 40-60 words
- **Experience**: 350-400 words (main compression target)
- **Skills**: 40-60 words (secondary compression target)

**Target for compression**: 475 words (safe buffer for 1 page)

## Core Operations

### Count All Sections

Count words in each section of a resume:

```bash
python scripts/count_sections.py resume.docx
```

**Output:**
```json
{
  "header": {
    "words": 15,
    "editable": false,
    "content": "John Doe | john@email.com | +1-555-0123 | linkedin.com/in/johndoe"
  },
  "education": {
    "words": 45,
    "editable": false,
    "section_start": 50,
    "section_end": 95
  },
  "experience": {
    "words": 420,
    "editable": true,
    "section_start": 100,
    "section_end": 520,
    "target": 360
  },
  "skills": {
    "words": 70,
    "editable": true,
    "section_start": 525,
    "section_end": 595,
    "target": 55
  },
  "total": 550,
  "target": 475,
  "reduction_needed": 75,
  "estimated_pages": 1.1
}
```

### Track Changes Across Iterations

Compare word counts between two versions:

```bash
python scripts/track_changes.py --before draft_v1.docx --after draft_v2.docx
```

**Output:**
```json
{
  "changes": {
    "header": {"before": 15, "after": 15, "delta": 0},
    "education": {"before": 45, "after": 45, "delta": 0},
    "experience": {"before": 420, "after": 385, "delta": -35},
    "skills": {"before": 70, "after": 60, "delta": -10},
    "total": {"before": 550, "after": 505, "delta": -45}
  },
  "compression_progress": {
    "target": 475,
    "current": 505,
    "remaining": 30,
    "percent_complete": 60
  }
}
```

### Check Against Target

Check if resume meets word count target:

```bash
python scripts/check_target.py resume.docx --target 475
```

**Output:**
```json
{
  "current_words": 505,
  "target_words": 475,
  "within_target": false,
  "reduction_needed": 30,
  "estimated_pages": 1.01,
  "status": "needs_compression",
  "recommendation": "Compress Experience section by 30 words"
}
```

### Get Section Word Range

Get word indices for a specific section (useful for targeted editing):

```bash
python scripts/get_section.py resume.docx --section experience
```

**Output:**
```json
{
  "section": "experience",
  "word_start": 100,
  "word_end": 520,
  "word_count": 420,
  "line_numbers": [12, 45],
  "editable": true
}
```

## Section Detection

The word counter automatically detects sections using common resume headers:

- **Header**: Everything before first section header (usually name and contact)
- **Education**: Matches "Education", "Academic Background", etc.
- **Experience**: Matches "Experience", "Work Experience", "Professional Experience", etc.
- **Skills**: Matches "Skills", "Technical Skills", "Core Competencies", etc.

**Custom headers** can be specified:

```bash
python scripts/count_sections.py resume.docx --headers '{"experience": "Professional Background", "skills": "Expertise"}'
```

## Integration with rescume Workflow

### Initial Draft
```bash
# Generate initial draft
content-generator creates draft_v0.docx

# Count sections
python scripts/count_sections.py draft_v0.docx > word_count_v0.json

# Result: 550 words total (75 over target)
```

### Compression Loop
```bash
# Iteration 1: Compress experience section
compression-strategist compresses draft_v0.docx → draft_v1.docx

# Track changes
python scripts/track_changes.py --before draft_v0.docx --after draft_v1.docx

# Check target
python scripts/check_target.py draft_v1.docx --target 475
# Result: 515 words (40 over target, continue compressing)
```

### Final Validation
```bash
# After compression converges
python scripts/check_target.py final_resume.docx --target 475
# Result: 485 words (within target ✓)
```

## Python Script Reference

### count_sections.py

Count words by section.

**Usage:**
```bash
python scripts/count_sections.py <docx_file> [--headers <json>]
```

**Parameters:**
- `docx_file`: Path to DOCX file
- `--headers`: Optional JSON mapping custom section names

**Returns:** JSON with word counts per section

### track_changes.py

Track word count changes between versions.

**Usage:**
```bash
python scripts/track_changes.py --before <file1> --after <file2>
```

**Parameters:**
- `--before`: Earlier version
- `--after`: Later version

**Returns:** JSON with deltas and progress

### check_target.py

Check if word count meets target.

**Usage:**
```bash
python scripts/check_target.py <docx_file> --target <number>
```

**Parameters:**
- `docx_file`: Path to DOCX file
- `--target`: Target word count (default: 475)

**Returns:** JSON with status and recommendations

### get_section.py

Get word range for specific section.

**Usage:**
```bash
python scripts/get_section.py <docx_file> --section <name>
```

**Parameters:**
- `docx_file`: Path to DOCX file
- `--section`: Section name (header, education, experience, skills)

**Returns:** JSON with word indices

## Word Count Calibration

After user validates that resume is exactly 1 page, calibrate the system:

```bash
python scripts/calibrate.py --file validated_resume.docx --pages 1.0
```

This updates the words-per-page ratio for this user's specific formatting.

**Default**: 500 words/page
**After calibration**: Personalized ratio (e.g., 520 words/page for dense formatting)

## Advanced Features

### Bullet-Level Counting

Count words in individual bullets:

```bash
python scripts/count_bullets.py resume.docx --section experience
```

**Output:**
```json
{
  "bullets": [
    {"id": 1, "words": 18, "text": "Built recommendation system..."},
    {"id": 2, "words": 22, "text": "Led team of 5 engineers..."},
    {"id": 3, "words": 15, "text": "Optimized SQL queries..."}
  ],
  "total_bullets": 3,
  "total_words": 55,
  "avg_words_per_bullet": 18.3
}
```

Useful for identifying which bullets to compress.

### Compression Recommendations

Get automated compression suggestions:

```bash
python scripts/recommend_compression.py resume.docx --target 475
```

**Output:**
```json
{
  "current": 550,
  "target": 475,
  "reduction_needed": 75,
  "recommendations": [
    {
      "action": "compress_experience",
      "section": "experience",
      "current": 420,
      "target": 360,
      "reduction": 60,
      "priority": "high"
    },
    {
      "action": "compress_skills",
      "section": "skills",
      "current": 70,
      "target": 55,
      "reduction": 15,
      "priority": "medium"
    }
  ]
}
```

## Integration with compression-strategist Subagent

The compression-strategist subagent uses this skill to:

1. **Determine compression targets** by section
2. **Track progress** across iterations
3. **Verify when target is reached**
4. **Identify specific bullets** to compress

Example workflow:
```
compression-strategist:
  1. Calls count_sections.py → identifies 75 words over target
  2. Plans: compress experience (60 words) + skills (15 words)
  3. Compresses experience section
  4. Calls track_changes.py → verifies 60 words saved
  5. Calls check_target.py → still 15 words over
  6. Compresses skills section
  7. Calls check_target.py → within target ✓
```

## Best Practices

1. **Always count before compressing** to establish baseline
2. **Track changes after each iteration** to verify progress
3. **Focus on editable sections only** (Experience, Skills)
4. **Use calibration** after user validates page count
5. **Check bullet-level counts** for targeted compression
6. **Set target with buffer** (475 vs 500) for safety

## Error Handling

All scripts return proper exit codes:
- `0`: Success
- `1`: File not found or invalid DOCX
- `2`: Section not found
- `3`: Invalid parameters

Check exit codes:
```bash
python scripts/count_sections.py resume.docx && echo "Success" || echo "Failed"
```

## Notes

- Word count includes all visible text (headers, footers, body)
- Excludes: comments, tracked changes, hidden text
- Section detection is case-insensitive
- Works with standard resume formats (reverse-chronological)
- Accurate within ±5 words due to DOCX parsing
