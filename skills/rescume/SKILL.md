---
name: rescume
description: "Intelligent resume tailoring system with Typst-based PDF rendering. Use when user wants to: (1) Tailor their resume for a specific job description, (2) Build a comprehensive resume database from existing resumes, (3) Optimize resume for ATS (Applicant Tracking Systems), (4) Generate single-page PDF resume with auto-fit layout, (5) Get feedback on resume quality for a specific role. Orchestrates specialized subagents (resume-parser, ats-analyzer, coverage-mapper, content-generator, hr-critic, interview-conductor) and typst-renderer skill to deliver professional PDF resumes in <200ms."
---

# Rescume - Rescue Your Resume

**Tagline**: "Rescue My Resume" - An intelligent multi-agent system with Typst-based PDF rendering for perfectly tailored resumes.

## Overview

Rescume v2.0 is a coordinator skill that orchestrates specialized AI subagents to transform your existing resumes into a comprehensive database, then craft perfectly tailored single-page PDF resumes for each job application. The system uses Typst templates with auto-fit logic to ensure professional PDF output without word-counting or iterative compression.

## Core Workflow

### Phase 1: Initial Setup (One-Time)

**Goal**: Build comprehensive resume database from user's existing resumes

1. **User uploads DOCX resumes** (can be multiple, including job-specific versions)
2. **Call `resume-parser` subagent** for each uploaded file
   - Input: DOCX file path
   - Output: Structured JSON (experiences, skills, projects, education)
   - The subagent uses the `json-database` skill
3. **Call `interview-conductor` subagent** to deepen understanding
   - Input: Current database state
   - Output: Intelligent follow-up questions
   - Mode: `initial_setup`
4. **Present questions to user** and collect answers
5. **Update database** with new information using `json-database` skill
6. **Database ready** for tailoring jobs

**Data structure created:**
```
data/
├── comprehensive_db/
│   ├── experiences.json
│   ├── skills.json
│   ├── projects.json
│   ├── education.json
│   └── metadata.json
└── uploaded_resumes/
    └── *.docx  (for parsing only)
```

### Phase 2: Tailoring for a Specific Job (v2.0 Workflow)

**Goal**: Create optimized single-page PDF resume for target role

#### Step 1: Job Analysis

1. **User uploads job description** (text or URL)
2. **Call `ats-analyzer` subagent**
   - Input: Job description text
   - Output: Required skills (must-have vs nice-to-have), ATS keywords, experience requirements
   - Save to: `data/job_applications/[job_id]/jd_analyzed.json`

#### Step 2: Coverage Mapping & Gap Filling

1. **Call `coverage-mapper` subagent**
   - Input: Database + JD requirements
   - Output: Coverage matrix, gap analysis, prioritized experiences
2. **If gaps exist** (coverage < 100%):
   - Call `interview-conductor` subagent in `gap_filling` mode
   - Present gap-filling questions to user
   - Update database with new experiences
   - Re-run `coverage-mapper` subagent
3. **Repeat until** coverage = 100% or user confirms no more experiences

#### Step 3: Template Selection (NEW in v2.0)

1. **List available templates** using `typst-renderer` skill:
   ```bash
   python skills/typst-renderer/scripts/list_templates.py
   ```
2. **Present template options** to user with previews
3. **User selects template** (or use default: `simple-technical-resume`)
4. **Save template choice** for this job application

**Available templates** (v2.0 launch):
- `simple-technical-resume` - Clean, ATS-friendly, single-column (default)

#### Step 4: Content Generation (SIMPLIFIED in v2.0)

**CRITICAL CHANGE**: Content generator now outputs pure JSON, NOT DOCX

1. **Call `content-generator` subagent**
   - Input: Database, coverage matrix, JD analysis
   - Output: Structured JSON content (see schema below)
   - NO formatting concerns, NO word counting
   - Focus: Write the best, most tailored content
   - Save to: `data/job_applications/[job_id]/content.json`

**Content JSON Schema:**
```json
{
  "header": {
    "name": "string",
    "location": "string",
    "email": "string",
    "phone": "string",
    "linkedin": "string",
    "github": "string",
    "website": "string"
  },
  "summary": "optional string",
  "education": [...],
  "experience": [...],
  "projects": [...],
  "skills": {
    "languages": ["..."],
    "frameworks": ["..."],
    "tools": ["..."],
    "concepts": ["..."]
  }
}
```

**Soft guidelines for content-generator:**
- 3-5 bullet points per experience
- 1-2 sentences per bullet
- Focus on impact and relevance
- Don't artificially limit content to fit a page

#### Step 5: Typst Compilation (NEW in v2.0)

1. **Compile to PDF** using `typst-renderer` skill:
   ```bash
   python skills/typst-renderer/scripts/compile.py \
     data/job_applications/[job_id]/content.json \
     [selected_template] \
     data/job_applications/[job_id]/resume.pdf
   ```
2. **Auto-fit handles page fitting**:
   - Template adjusts font size (9-10.5pt) to fit content
   - Compilation takes ~50-100ms
   - Guaranteed single-page output

3. **Check compilation result**:
   - ✅ Success → Continue to Step 6
   - ⚠️ Font too small (<9pt) → Go to Step 5a
   - ❌ Error → Debug and retry

#### Step 5a: Content Trimming (If Needed)

**Only if** auto-fit reports font dropped below 9pt:

1. **Ask content-generator to trim** 2-3 bullet points:
   - Remove least relevant bullets
   - Keep all must-have skill demonstrations
   - Focus on highest-impact achievements
2. **Recompile** with trimmed content (Step 5)
3. **Iterate max 2-3 times** (content should fit easily with reasonable volume)

**Important**: This is NOT iterative compression like v1.0. It's a simple trim-and-recompile loop that typically completes in 1-2 iterations.

#### Step 6: Quality Check (SIMPLIFIED in v2.0)

1. **Call `hr-critic` subagent** in `final_validation` mode
   - Input: Resume content JSON (not PDF)
   - Focus: Content quality ONLY (not formatting)
   - Evaluate: Relevance, impact, keyword coverage, professionalism
   - Output: Quality score (1-10), hire probability, ship/no-ship decision

2. **Decision logic**:
   - Score ≥ 7.0 AND hire probability ≥ 0.70 → APPROVED
   - Otherwise → NEEDS_REVISION

3. **If NEEDS_REVISION**:
   - Review HR Critic feedback
   - Update content JSON (strengthen weak bullets)
   - Recompile PDF (Step 5)
   - Re-evaluate (Step 6)

#### Step 7: Deliver PDF to User

1. **Show final PDF path**: `data/job_applications/[job_id]/resume.pdf`
2. **Display metrics**:
   - HR Critic score: X/10
   - Hire probability: XX%
   - ATS keyword coverage: 100%
   - Page count: 1
   - Compilation time: ~XXms
3. **Offer to open PDF** for user review
4. **Done!**

## Workflow Diagram (v2.0)

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: Database Building (Unchanged from v1.0)                 │
│                                                                   │
│  DOCX Resume → resume-parser → JSON Database                     │
│                 ↓                                                 │
│            interview-conductor → Enriched Database                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: Resume Tailoring (SIGNIFICANTLY CHANGED in v2.0)        │
│                                                                   │
│  Job Description                                                  │
│       ↓                                                           │
│  ats-analyzer → Requirements JSON                                 │
│       ↓                                                           │
│  coverage-mapper → Coverage Matrix                                │
│       ↓                                                           │
│  [If gaps] → interview-conductor → Fill gaps → Re-map             │
│       ↓                                                           │
│  User selects template (NEW)                                      │
│       ↓                                                           │
│  content-generator → JSON content (NOT DOCX)                      │
│       ↓                                          ↑                │
│  typst-renderer → compile.py → PDF              │                │
│       ↓                                          │                │
│  Font too small? ──YES─→ Trim content ──────────┘                │
│       │ NO                                                        │
│       ↓                                                           │
│  hr-critic → Quality validation                                   │
│       ↓                                                           │
│  Deliver PDF                                                      │
└─────────────────────────────────────────────────────────────────┘
```

## Key Differences from v1.0

### What Changed

| Aspect | v1.0 (DOCX) | v2.0 (Typst) |
|--------|-------------|--------------|
| **Output Format** | DOCX + PDF conversion | Pure PDF via Typst |
| **Content Format** | Formatted DOCX | Structured JSON |
| **Page Fitting** | Iterative compression (10+ iterations) | Auto-fit templates (0-2 iterations) |
| **Word Counting** | Constant word tracking | Not needed |
| **Compression** | `compression-strategist` agent | Simple trim-and-recompile |
| **Rendering Speed** | Slow (DOCX → PDF conversion) | Fast (~50-100ms) |
| **LLM Concerns** | Layout, fonts, spacing, word counts | Content quality only |
| **Determinism** | Inconsistent (style drift) | Deterministic (same content → same PDF) |

### What Was Removed

- ❌ `word-counter` skill - Replaced by auto-fit
- ❌ `compression-strategist` agent - Replaced by simple trimming
- ❌ DOCX output pipeline - Pure Typst PDF now
- ❌ Iterative compression loops - Auto-fit handles it
- ❌ Style template matching - Typst templates define style
- ❌ Word count targets - No longer relevant

### What Was Added

- ✅ `typst-renderer` skill - Complete PDF compilation pipeline
- ✅ Template system - Modular, auto-fit Typst templates
- ✅ Template selection step - User chooses design
- ✅ JSON content format - Pure structured data
- ✅ Auto-fit logic - Guaranteed single-page output
- ✅ Fast compilation - ~50-100ms per resume

## Agent Responsibilities (v2.0)

### resume-parser
- **Input**: DOCX file
- **Output**: Structured JSON
- **Changes**: None (unchanged from v1.0)

### ats-analyzer
- **Input**: Job description text
- **Output**: Required skills, keywords, requirements
- **Changes**: None (unchanged from v1.0)

### coverage-mapper
- **Input**: Database + JD requirements
- **Output**: Coverage matrix, prioritization
- **Changes**: Minor - removed word budget references

### content-generator
- **Input**: Database, coverage matrix, JD analysis
- **Output**: Structured JSON (MAJOR CHANGE from DOCX)
- **Changes**: Now outputs pure JSON, no formatting concerns

### hr-critic
- **Input**: Content JSON
- **Output**: Quality score, hire probability, ship/no-ship
- **Changes**: Removed "triage" mode, evaluates content only

### interview-conductor
- **Input**: Database state, gaps
- **Output**: Intelligent questions
- **Changes**: None (unchanged from v1.0)

## Skills Used (v2.0)

### json-database (Unchanged)
- Load/save resume database
- Query experiences, skills, projects
- Validate database structure

### typst-renderer (NEW)
- **compile.py**: Main compilation orchestrator
- **json_to_typst.py**: Convert JSON → Typst data
- **validate_pdf.py**: Validate PDF page count
- **list_templates.py**: Discover available templates

### coverage-tracker (Minor Changes)
- Verify required skills are present
- No longer interfaces with word counting

## Error Handling

### Common Issues

**"Typst CLI not found"**
```bash
brew install typst  # macOS
# Or visit https://typst.app
```

**"Content overflows 1 page"**
- Auto-fit reduced font to minimum but still doesn't fit
- Solution: Trim 2-3 bullet points and recompile
- Rare: Usually only happens with >25 bullets

**"Invalid JSON schema"**
- Content generator produced malformed JSON
- Solution: Validate JSON, regenerate if needed

**"Template not found"**
- Selected template doesn't exist
- Solution: Run `list_templates.py` to see available options

## Performance Expectations

| Operation | v1.0 Time | v2.0 Time | Improvement |
|-----------|-----------|-----------|-------------|
| Content generation | ~10s | ~5s | 2x faster |
| Page fitting | ~2-5min (10+ iterations) | ~100ms (auto-fit) | **30x faster** |
| PDF rendering | ~5-10s | ~50-100ms | **100x faster** |
| **Total Phase 2** | ~3-6min | ~15-30s | **12x faster** |

## User Experience Flow

### Typical Session (v2.0)

```
User: "Tailor my resume for this Data Scientist role at TechCorp"

Rescume:
✓ Analyzing job description...
✓ Mapped experiences (100% coverage)
✓ Available templates:
  1. simple-technical-resume (ATS-friendly, clean)
  [More templates coming soon]

Select template (or press Enter for default): [User presses Enter]

✓ Generating tailored content...
✓ Compiling PDF with Typst...
✓ Resume rendered (1 page, 10.2pt font)
✓ HR Critic score: 8.5/10
✓ Hire probability: 85%

📄 Your resume: data/job_applications/techcorp_ds_2026/resume.pdf
```

**Total time: ~20 seconds**

### If Content Trimming Needed

```
⚠ Auto-fit used minimum font (9pt) but content still overflows.

Trimming 3 less relevant bullet points...

✓ Recompiling...
✓ Resume rendered (1 page, 9.5pt font)
✓ All required skills still covered

📄 Your resume: data/job_applications/techcorp_ds_2026/resume.pdf
```

**Additional time: ~5 seconds**

## Success Criteria

After Phase 2 completion, verify:

- ✅ PDF exists at output path
- ✅ Page count = 1
- ✅ HR Critic score ≥ 7.0
- ✅ Hire probability ≥ 0.70
- ✅ All required skills demonstrated
- ✅ ATS keywords present
- ✅ Font size ≥ 9pt
- ✅ Professional, readable formatting

## Tips for Users

### Getting Best Results

**Phase 1 (Database Building):**
- Upload all your resumes (job-specific versions are valuable)
- Answer follow-up questions thoroughly
- Include metrics and quantifiable achievements
- Don't worry about formatting—focus on content

**Phase 2 (Tailoring):**
- Provide complete job description (more detail = better tailoring)
- Trust the auto-fit—don't manually limit content
- Review HR Critic feedback to improve database
- Save good tailored resumes for future reference

### Iteration is Fast

Unlike v1.0, iteration in v2.0 is **extremely fast** (~100ms per compile):
- Want to try different template? Recompile instantly
- Want to adjust a bullet? Recompile instantly
- Want to add a project? Recompile instantly

Don't be afraid to experiment—the pipeline is designed for rapid iteration.

## Future Enhancements

Planned for future releases:
- **More templates** - Multiple professional designs
- **Template customization** - User-defined color schemes, fonts
- **Multi-page CVs** - Option for academic/research CVs
- **PDF parsing** - Accept PDF resumes as input
- **LinkedIn import** - Pull from LinkedIn profile
- **Cover letter generation** - Matching cover letters

## See Also

- **[CHANGELOG.md](../../CHANGELOG.md)** - Version history
- **[templates/README.md](../../templates/README.md)** - Template authoring
- **[skills/typst-renderer/SKILL.md](../typst-renderer/SKILL.md)** - Rendering pipeline
- **[agents/content-generator.md](../../agents/content-generator.md)** - JSON schema

---

**Remember**: v2.0 is about **simplicity and speed**. The LLM writes great content, Typst renders it beautifully, auto-fit ensures it fits, and you get a professional PDF in seconds. No word counting, no compression struggles, no layout headaches.
