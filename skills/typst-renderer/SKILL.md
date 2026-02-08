---
name: typst-renderer
description: "Compile structured resume JSON into single-page PDF using Typst templates with auto-fit. Use when you need to: (1) Render resume content as PDF, (2) Apply a specific template design, (3) Ensure one-page output with auto-fit sizing, (4) Validate PDF page count, (5) List available templates. This skill handles ALL formatting and layout concerns—the LLM never needs to think about fonts, spacing, or page limits."
---

# Typst Renderer - Resume Compilation Skill

A tool skill that compiles structured JSON resume data into professionally formatted single-page PDF resumes using Typst templates.

## Overview

The Typst Renderer eliminates layout concerns from the resume generation workflow. The LLM generates pure content as structured JSON, and this skill handles all formatting, sizing, and page fitting automatically.

**Key Principle**: The LLM is a content writer, not a layout engineer. Never think about character counts, line widths, font sizes, or page limits when generating resume content.

## Quick Reference

| Task | Command |
|------|---------|
| List templates | `python scripts/list_templates.py` |
| Compile resume | `python scripts/compile.py content.json template-name output.pdf` |
| Validate PDF | `python scripts/validate_pdf.py resume.pdf` |
| Convert JSON | `python scripts/json_to_typst.py content.json data.typ` |

## Core Scripts

### 1. compile.py - Main Compilation Orchestrator

Converts JSON content → Typst data → PDF in one step.

```bash
python scripts/compile.py content.json simple-technical-resume output.pdf [min_font_size]
```

**What it does:**
1. Loads JSON resume content
2. Converts to Typst data format
3. Injects into selected template
4. Compiles with Typst CLI
5. Validates output (page count, content)
6. Reports success/warnings/errors

**Parameters:**
- `content.json` - Structured resume data (see JSON Schema below)
- `template-name` - Template directory name (e.g., "simple-technical-resume")
- `output.pdf` - Destination for compiled PDF
- `min_font_size` - Minimum font size after auto-fit (default: 9.0pt)

**Output:**
```json
{
  "success": true,
  "output": "path/to/resume.pdf",
  "pages": 1,
  "errors": [],
  "warnings": ["Font size reduced to 9.5pt to fit content"]
}
```

**Error Handling:**
- If compilation fails: Check JSON schema validity
- If page count > 1: Content needs trimming (ask LLM to reduce bullet points)
- If font < min: Content is too dense (ask LLM to trim 2-3 bullets)

### 2. list_templates.py - Template Discovery

Lists all available Typst templates with metadata.

```bash
python scripts/list_templates.py              # Brief listing
python scripts/list_templates.py --verbose    # Detailed metadata
python scripts/list_templates.py --json       # JSON output
```

**Use this to:**
- Present template options to users
- Get template metadata programmatically
- Verify template availability before compiling

### 3. json_to_typst.py - Data Converter

Converts JSON to Typst data declarations. Usually called by compile.py automatically, but can be used standalone.

```bash
python scripts/json_to_typst.py resume.json data.typ
```

**Handles:**
- String escaping (quotes, special characters)
- Nested dictionaries and arrays
- None/null values
- Unicode content

### 4. validate_pdf.py - PDF Validation

Validates compiled PDF meets resume requirements.

```bash
python scripts/validate_pdf.py resume.pdf [max_pages]
```

**Checks:**
- File exists and is not empty
- Page count ≤ max_pages
- Pages have text content
- Content density (word count)

## JSON Schema

The LLM should generate content in this format:

```json
{
  "header": {
    "name": "Full Name",
    "location": "City, State",
    "email": "email@example.com",
    "phone": "+1 (123) 456-7890",
    "linkedin": "linkedin.com/in/username",
    "github": "github.com/username",
    "website": "example.com"
  },
  "summary": "Optional 1-2 sentence professional summary",
  "education": [
    {
      "institution": "University Name",
      "degree": "M.S. / B.S. / etc.",
      "field": "Field of Study",
      "location": "City, State",
      "start_date": "YYYY-MM",
      "end_date": "YYYY-MM or 'Present'",
      "gpa": "3.8/4.0 (optional)",
      "details": [
        "Relevant coursework, awards, or details"
      ]
    }
  ],
  "experience": [
    {
      "company": "Company Name",
      "role": "Job Title",
      "location": "City, State",
      "start_date": "YYYY-MM",
      "end_date": "YYYY-MM or 'Present'",
      "bullets": [
        "Achievement-focused bullet point with metrics",
        "Another impact statement with specific results"
      ]
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "subtitle": "Optional tagline",
      "dates": "Optional date range",
      "bullets": [
        "What you built and the impact"
      ]
    }
  ],
  "skills": {
    "languages": ["Python", "Java", "SQL"],
    "frameworks": ["TensorFlow", "React", "Django"],
    "tools": ["Git", "Docker", "AWS"],
    "concepts": ["Machine Learning", "A/B Testing", "CI/CD"]
  }
}
```

**Field Notes:**
- All fields are optional except `header.name`
- Dates should be `YYYY-MM` format or "Present"
- `bullets` arrays should have 3-5 items per role
- Skills can be organized differently per template

## Auto-Fit Behavior

Templates implement auto-fit logic to guarantee single-page output:

1. **Default Rendering**: Start at default font size (e.g., 10.5pt)
2. **Overflow Detection**: Check if content exceeds one page
3. **Progressive Reduction**: Shrink font size in small steps (0.5pt)
4. **Minimum Threshold**: Stop at minimum font (e.g., 9pt)
5. **Overflow Report**: If still overflows, report to orchestrator

**When auto-fit reports font too small:**
- DO NOT try to manually adjust font sizes
- DO NOT worry about character counts or line widths
- DO ask the LLM to trim 2-3 bullet points
- DO recompile with trimmed content
- Iterate max 2-3 times—content should fit easily with reasonable volume

## Workflow Integration

### Phase 2: Resume Tailoring (Simplified)

```
Step 1: Job Analysis (ats-analyzer)
  ↓
Step 2: Coverage Mapping (coverage-mapper)
  ↓
Step 3: Template Selection
  → python list_templates.py
  → User picks template
  ↓
Step 4: Content Generation (content-generator)
  → LLM outputs structured JSON
  → NO formatting concerns, NO word counting
  ↓
Step 5: Typst Compilation (THIS SKILL)
  → python compile.py content.json template-name output.pdf
  → Auto-fit ensures 1-page output
  ↓
Step 6: Quality Check
  → If font < 9pt: trim content, recompile
  → hr-critic evaluates content quality
  ↓
Step 7: Deliver PDF
```

## Template Management

### Available Templates

Run `list_templates.py` to see current templates. Initial templates:
- `simple-technical-resume` - Clean, ATS-friendly, single-column

### Adding New Templates

See `templates/README.md` for template authoring guide. New templates must:
1. Accept the standard JSON schema
2. Implement auto-fit logic
3. Provide metadata.json
4. Generate single-page output

## Dependencies

**Required:**
- Typst CLI (v0.11+) - Install: `brew install typst` (macOS) or see https://typst.app
- pdfplumber - Install: `pip install pdfplumber`

**Optional:**
- python-docx - Only if still needed for Phase 1 DOCX parsing

## Troubleshooting

### "Typst CLI not found"
Install Typst: `brew install typst` (macOS), or download from https://github.com/typst/typst

### "Template not found"
Run `list_templates.py` to see available templates. Check spelling matches exactly.

### "Invalid JSON"
Validate JSON schema matches the format above. Common issues:
- Missing required `header.name` field
- Malformed dates (should be YYYY-MM)
- Unescaped quotes in strings

### "Resume overflows 1 page"
The auto-fit reduced font to minimum but content still doesn't fit. Ask LLM to:
- Remove 2-3 least relevant bullet points
- Condense lengthy bullets to 1-2 sentences
- Consider removing optional "projects" section if space-constrained

### "PDF is empty"
Typst compiled but output has no visible content. Check:
- JSON data has actual content (not empty strings)
- Template is compatible with data schema
- No errors in Typst compilation output

## Performance

- Typst compilation: ~50-100ms per resume
- JSON conversion: ~5ms
- PDF validation: ~10-50ms
- **Total pipeline: < 200ms** (extremely fast, iteration is cheap)

## Important Reminders for LLMs

1. **Never count words or characters** when generating content
2. **Never worry about page fitting** — the template handles it
3. **Never add formatting instructions** to content (bold, italic, spacing)
4. **Focus on quality and relevance** — let auto-fit handle quantity
5. **If font too small:** trim content and recompile (iteration is fast)
6. **Trust the pipeline** — it's deterministic and reliable

## Examples

### Typical Workflow

```python
# 1. LLM generates content (content-generator agent)
content = {
    "header": {"name": "Jane Doe", ...},
    "experience": [...],
    ...
}

# 2. Save to JSON
with open("content.json", "w") as f:
    json.dump(content, f)

# 3. Compile with typst-renderer
result = subprocess.run([
    "python", "skills/typst-renderer/scripts/compile.py",
    "content.json",
    "simple-technical-resume",
    "output.pdf"
])

# 4. Check result
if result.returncode == 0:
    print("✓ Resume compiled successfully")
else:
    print("✗ Compilation failed, check errors")
```

### Handling Overflow

```python
# If compile reports font too small or overflow:
# → Ask LLM to trim content

# Re-generate with fewer bullets
trimmed_content = ask_llm_to_trim(content, reduce_by=3)

# Recompile
compile_resume(trimmed_content, template, output)
```

## See Also

- `templates/README.md` - Template authoring guide
- `agents/content-generator.md` - JSON content generation
- `skills/rescume/SKILL.md` - Main workflow orchestrator
