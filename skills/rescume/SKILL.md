---
name: rescume
description: "Intelligent resume tailoring system that 'rescues' your resume for specific job applications. Use when user wants to: (1) Tailor their resume for a specific job description, (2) Build a comprehensive resume database from existing resumes, (3) Optimize resume for ATS (Applicant Tracking Systems), (4) Ensure resume fits on one page while covering all required skills, (5) Get feedback on resume quality for a specific role. Works exclusively with DOCX files. Orchestrates specialized subagents (resume-parser, ats-analyzer, coverage-mapper, content-generator, hr-critic, compression-strategist, interview-conductor) to handle the complete workflow from parsing uploaded resumes to delivering a perfectly tailored one-page resume."
---

# Rescume - Rescue Your Resume

**Tagline**: "Rescue My Resume" - An intelligent multi-agent system for tailoring resumes to specific job descriptions.

## Overview

Rescume is a coordinator skill that orchestrates specialized AI subagents to transform your existing resumes into a comprehensive database, then craft perfectly tailored resumes for each job application. The system ensures all required skills are covered while maintaining professional quality and one-page format.

## Core Workflow

### Phase 1: Initial Setup (One-Time)

**Goal**: Build comprehensive resume database from user's existing resumes

1. **User uploads DOCX resumes** (can be multiple, including job-specific versions)
2. **Call `resume-parser` subagent** for each uploaded file
   - Input: DOCX file path
   - Output: Structured JSON (experiences, skills, projects, education)
   - The subagent uses the `docx` skill and `json-database` skill
3. **Call `interview-conductor` subagent** to deepen understanding
   - Input: Current database state
   - Output: Intelligent follow-up questions
   - Mode: `initial_setup`
4. **Present questions to user** and collect answers
5. **Update database** with new information using `json-database` skill
6. **Database ready** for tailoring jobs

**Data structure** created:
```
data/
├── comprehensive_db/
│   ├── experiences.json
│   ├── skills.json
│   ├── projects.json
│   ├── education.json
│   └── metadata.json
└── uploaded_resumes/
    └── *.docx  (style templates)
```

### Phase 2: Tailoring for a Specific Job

**Goal**: Create optimized one-page resume for target role

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

#### Step 3: Content Generation

1. **Select style template**: Choose any uploaded DOCX for formatting reference
2. **Call `content-generator` subagent**
   - Input: Database, coverage matrix, JD analysis, style template
   - Output: Initial draft DOCX (likely >1 page)
   - Note: Content from database, formatting from template
   - Save to: `data/job_applications/[job_id]/working_resume.docx`

#### Step 4: HR Content Critique

1. **Call `hr-critic` subagent** in `comprehensive` mode
   - Input: Initial draft, JD analysis
   - Focus: Content quality (ignore page limit)
   - Output: Bullet scores, improvement suggestions, priority assignments
2. **Apply HR feedback** to improve content
   - Strengthen weak bullets
   - Add quantification
   - Improve action verbs
   - May make resume longer (that's OK)

#### Step 5: Word Count Optimization

**Key principle**: Only Experience and Skills sections are edited. Education and Header are fixed.

1. **Use `word-counter` skill** to track section-by-section word counts
   ```json
   {
     "header": {"words": 15, "editable": false},
     "education": {"words": 45, "editable": false},
     "experience": {"words": 420, "editable": true, "target": 360},
     "skills": {"words": 70, "editable": true, "target": 55},
     "total": 550,
     "target": 475,
     "reduction_needed": 75
   }
   ```

2. **Call `compression-strategist` subagent** iteratively
   - Input: Current DOCX, target word count, HR priorities
   - Strategy: Compress Experience first, then Skills if needed
   - Built-in safety: Never lose required skill coverage
   - Output: Compressed DOCX or "cannot_compress" status

3. **Compression loop**:
   ```
   While total_words > 475:
       result = Call compression-strategist subagent
       If result.status == "success":
           Update working_resume.docx
           Track word count changes
       Else if result.status == "cannot_compress":
           Break loop (need HR triage)
   ```

#### Step 6: HR Triage (If Needed)

**When**: Compression agent can't compress further without violating constraints

1. **Call `hr-critic` subagent** in `triage` mode
   - Input: Current draft, compression options (what could be cut)
   - Output: Strategic decision on what to sacrifice
   - Example: "Remove Excel skill (nice-to-have) to preserve Python leadership (must-have)"
2. **Apply HR decision** and update resume

#### Step 7: User Validation Loop

1. **Show current draft to user**:
   ```
   Draft v3 generated (485 words total):
   - Experience: 355 words
   - Skills: 55 words
   - Total: 485 words (target: 450-500 for 1 page)
   
   Please review the attached DOCX. Does it look like one full page?
   ```
2. **Collect user feedback**:
   - "Perfect!" → Proceed to final validation
   - "Still 1.1 pages" → Compress by 20 more words
   - "Only 0.8 pages" → Expand by 50 words
3. **Adjust based on feedback** and repeat

#### Step 8: Final Validation

1. **Call `hr-critic` subagent** in `final_validation` mode
   - Input: Final draft
   - Output: Binary decision (APPROVED/NEEDS_REVISION), hire probability
   - Threshold: hire_probability > 0.7
2. **If APPROVED**: Proceed to export
3. **If NEEDS_REVISION**: Apply suggestions and re-validate

#### Step 9: Export & Deliver

1. **Save final DOCX**: `outputs/[job_id]/final_resume.docx`
2. **Convert to PDF** using `pdf` skill: `outputs/[job_id]/final_resume.pdf`
3. **Generate coverage report**: What skills are demonstrated where
4. **Present to user**: Both DOCX (editable) and PDF (for submission)

## Available Subagents

These specialized AI agents handle specific tasks. Always call subagents for their expertise:

### 1. resume-parser
- **Purpose**: Parse DOCX resume files → structured JSON
- **When to call**: User uploads a resume
- **Tools**: docx skill, json-database skill
- **Input**: DOCX file path
- **Output**: Structured data (experiences, skills, projects, education)

### 2. ats-analyzer
- **Purpose**: Analyze job descriptions to extract requirements
- **When to call**: User uploads a job description
- **Tools**: Text analysis
- **Input**: Job description text
- **Output**: Required skills, keywords, experience requirements (categorized by importance)

### 3. coverage-mapper
- **Purpose**: Map user's experiences to job requirements
- **When to call**: After JD analysis, to check skill coverage
- **Tools**: coverage-tracker skill, json-database skill
- **Input**: Database + JD requirements
- **Output**: Coverage matrix, gap analysis, experience prioritization

### 4. content-generator
- **Purpose**: Generate tailored resume content
- **When to call**: After coverage is complete (100%)
- **Tools**: docx skill, json-database skill
- **Input**: Database, coverage matrix, JD analysis, style template
- **Output**: Initial draft DOCX

### 5. hr-critic
- **Purpose**: Evaluate resume quality from HR perspective
- **When to call**: After content generation, and for final validation
- **Modes**: 
  - `comprehensive`: Initial content critique
  - `triage`: Make hard choices when can't fit everything
  - `final_validation`: Binary ship/no-ship decision
- **Input**: Resume draft, JD analysis, mode
- **Output**: Quality scores, suggestions, hire probability

### 6. compression-strategist
- **Purpose**: Optimize word count while preserving quality
- **When to call**: When resume exceeds target word count
- **Tools**: docx skill, word-counter skill
- **Input**: DOCX, target word count, HR priorities
- **Output**: Compressed DOCX or "cannot_compress" status

### 7. interview-conductor
- **Purpose**: Generate intelligent follow-up questions
- **When to call**: After initial parsing, or when gaps are discovered
- **Modes**:
  - `initial_setup`: Deepen understanding after parsing
  - `gap_filling`: Fill specific skill gaps for a job
- **Input**: Database state, context (mode)
- **Output**: List of questions

## Custom Tool Skills

These are reusable tools that subagents use:

### word-counter
- **Purpose**: Section-by-section word counting in DOCX
- **Usage**: Track word counts across iterations
- **Output**: Word counts per section, total, reduction needed

### json-database
- **Purpose**: Manage comprehensive resume database
- **Usage**: Read/write structured data (experiences, skills, projects, education)
- **Operations**: Load, update, query

### coverage-tracker
- **Purpose**: Verify skill coverage is maintained
- **Usage**: Check if all required skills are present in resume
- **Output**: Coverage percentage, missing skills

## Built-in Skills (Already Available)

### docx
- **Location**: `/mnt/skills/public/docx/`
- **Purpose**: Read, create, edit Word documents
- **Used by**: resume-parser, content-generator, compression-strategist

### pdf
- **Location**: `/mnt/skills/public/pdf/`
- **Purpose**: Convert DOCX to PDF
- **Used by**: Final export step

## Key Design Principles

1. **Template = Style Only**: Content always from database, formatting from any uploaded resume
2. **Section-Based Optimization**: Only edit Experience and Skills sections
3. **HR is Authoritative**: HR Critic decides quality, not technical metrics
4. **User in the Loop**: Always render and get feedback before finalizing
5. **Coverage is Sacred**: Never sacrifice required skills
6. **Subagent Specialization**: Each subagent has one clear purpose
7. **Progressive Workflow**: Setup once (Phase 1), tailor many times (Phase 2)

## Word Count Heuristics

**Standard resume**: 450-550 words ≈ 1 page
- Varies based on margins, font size, line spacing
- Experience section: typically 350-400 words
- Skills section: typically 40-60 words
- Education section: typically 40-60 words
- Header: typically 10-20 words

**Target for compression**: 475 words (safe buffer)

After user validation, the system learns their specific word-to-page ratio.

## File Structure

```
project_root/
├── data/
│   ├── comprehensive_db/
│   │   ├── experiences.json
│   │   ├── skills.json
│   │   ├── projects.json
│   │   ├── education.json
│   │   └── metadata.json
│   │
│   ├── uploaded_resumes/
│   │   └── *.docx
│   │
│   └── job_applications/
│       └── [job_id]/
│           ├── jd_original.txt
│           ├── jd_analyzed.json
│           ├── coverage_matrix.json
│           ├── working_resume.docx
│           └── word_count_tracker.json
│
└── outputs/
    └── [job_id]/
        ├── final_resume.docx
        ├── final_resume.pdf
        └── coverage_report.json
```

## Usage Examples

### Initial Setup
```
User: "I want to build my resume database from my existing resumes"
Claude: [Uses rescume skill]
Claude: [Calls resume-parser subagent for each uploaded file]
Claude: [Calls interview-conductor subagent]
Claude: "I have some questions to better understand your experience..."
[User answers questions]
Claude: "Your resume database is ready with 5 experiences, 15 skills, and 3 projects"
```

### Tailor for New Job
```
User: "Tailor my resume for this Senior Data Analyst role at PCI Energy"
Claude: [Uses rescume skill]
Claude: [Calls ats-analyzer subagent]
Claude: [Calls coverage-mapper subagent → finds 90% coverage, missing Kubernetes]
Claude: "This role requires Kubernetes. Do you have container orchestration experience?"
User: "Yes, I used Docker extensively at Company X"
Claude: [Updates database, re-runs coverage-mapper → 100%]
Claude: [Calls content-generator subagent]
Claude: [Calls hr-critic subagent → gets feedback]
Claude: [Applies improvements, now 550 words]
Claude: [Calls compression-strategist subagent iteratively]
Claude: "Draft v3 ready (485 words). Please review: does it look like one page?"
User: "Perfect!"
Claude: [Calls hr-critic in final_validation mode → APPROVED]
Claude: "Here's your tailored resume for PCI Energy [DOCX + PDF]"
```

## Error Handling

- **No DOCX uploaded**: Ask user to upload DOCX files (not PDF)
- **Cannot achieve coverage**: Inform user which skills are missing, suggest alternatives
- **Cannot compress to 1 page**: Call hr-critic in triage mode for strategic decisions
- **User rejects final draft**: Iterate based on specific feedback

## Notes

- **DOCX only**: PDF input not supported (no reliable format preservation)
- **Iterative by design**: System expects multiple rounds of feedback
- **Transparent**: Word count tracking and iteration logs show all decisions
- **Growing database**: Each new job enriches the comprehensive database
- **Privacy**: All data stored locally, never transmitted

## Next Steps After Using This Skill

After successfully tailoring a resume, suggest:
1. "Would you like to tailor this for another job?"
2. "Should I update your database with any new skills you've gained?"
3. "Want to review the coverage report to see which experiences were prioritized?"
