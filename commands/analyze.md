---
name: analyze
description: Analyze a job description to extract ATS keywords and requirements
usage: /rescume analyze [paste-jd] or "analyze this job description"
aliases: ["check", "requirements", "ats"]
---

# Analyze Job Description Command

Analyze job descriptions to extract requirements, ATS keywords, and skill priorities.

## Usage

### Option 1: Slash Command
```
/rescume analyze
[Paste job description when prompted]
```

### Option 2: Natural Language
```
Analyze this job description: [paste JD]
```
```
What skills does this job require? [paste JD]
```
```
Check my coverage for this role [paste JD]
```

## What Happens

1. **JD Input**: You provide job description
   - Paste text directly
   - Upload text file
   - Provide URL (if supported)

2. **Extraction**: ATS Analyzer identifies:
   - **Required skills** (must-have)
   - **Preferred skills** (nice-to-have)
   - **Experience requirements** (years, seniority)
   - **ATS keywords** (exact phrases to use)
   - **Education requirements**
   - **Red flags** (security clearance, relocation, etc.)

3. **Categorization**: Each skill gets:
   - Category: must-have or nice-to-have
   - Importance score: 1-10
   - Mention count: How many times it appears
   - Context: How it's used in the role

4. **Coverage Check**: If database exists:
   - Maps your experiences to requirements
   - Shows coverage percentage
   - Identifies gaps

5. **Report**: Saves analysis to:
   - `data/job_applications/[job_id]/jd_analyzed.json`
   - `data/job_applications/[job_id]/coverage_matrix.json`

## Output Example

```
✓ Job Description Analyzed!

Position: Senior Data Analyst at PCI Energy
Level: Senior (3-5 years required)

Required Skills (Must-Have): 12 skills
1. Python (importance: 10/10) - mentioned 4x
2. SQL (importance: 9/10) - mentioned 3x
3. A/B Testing (importance: 8/10) - mentioned 2x
...

Preferred Skills (Nice-to-Have): 8 skills
1. Tableau (importance: 6/10) - mentioned 1x
2. R (importance: 5/10) - mentioned 1x
...

ATS Keywords to Include:
✓ "A/B testing" (exact phrase, not "AB testing")
✓ "stakeholder communication"
✓ "cross-functional collaboration"

Your Coverage: 85% (17/20 skills)
Missing: Kubernetes, Tableau, AWS
```

## When to Use

**Before tailoring**: Analyze JD to understand requirements
```
/rescume analyze
[See what skills are needed]
[Check your coverage]
[Fill gaps if needed]
Then: /rescume start
```

**Standalone**: Just want to see requirements
```
/rescume analyze
[Get breakdown without generating resume]
```

## Parameters

- `--save`: Save analysis without checking coverage
- `--format <json|markdown>`: Output format

## Examples

```bash
# Analyze and check coverage
/rescume analyze
[Paste JD]
# Shows gaps and triggers gap-filling if needed

# Just analyze (no coverage check)
/rescume analyze --save
[Paste JD]
# Saves analysis for later use

# Natural language
"What are the requirements for this role?"
[Paste JD when prompted]
```

## Next Steps After Analysis

**If 100% coverage**: Ready to generate!
```
/rescume start
```

**If <100% coverage**: Fill gaps first
- Answer Interview Conductor questions
- Add missing skills to database
- Re-check coverage

**If major gaps**: Decide strategy
- Apply anyway (if nice-to-have skills)
- Skip application (if critical must-haves missing)
- Learn missing skills first

## Troubleshooting

**Issue**: "Cannot extract requirements"
- **Solution**: Ensure JD has clear sections (Requirements, Qualifications, etc.)

**Issue**: "Too generic"
- **Solution**: ATS Analyzer works best with detailed JDs. Try pasting full description, not just summary.

**Issue**: "Missing obvious skills"
- **Solution**: Some JDs use non-standard terms. Analyzer uses synonym matching but may miss edge cases.
