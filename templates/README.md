# Rescume Templates

This directory contains Typst resume templates used by the Rescume plugin to render tailored resumes as PDFs.

## Available Templates

### simple-technical-resume
- **Description**: Clean, ATS-friendly single-column resume
- **Best for**: Software engineers, data scientists, technical roles
- **Auto-fit**: Yes (9pt - 10.5pt)
- **Package**: Based on `@preview/simple-technical-resume:0.1.1`

## Template Structure

Each template directory must contain:

```
template-name/
├── template.typ      # Main template file with auto-fit logic
├── metadata.json     # Template metadata (name, description, features)
├── example.pdf       # Preview/example output
└── main.typ          # Example usage (optional)
```

## How Templates Work

1. **Content Generation**: The LLM generates structured JSON content (via `content-generator` agent)
2. **Data Conversion**: `json_to_typst.py` converts JSON to Typst data format
3. **Template Rendering**: The template file renders the data using Typst's layout engine
4. **Auto-Fit**: Templates adjust font size/spacing to ensure single-page output
5. **PDF Output**: Typst compiles to PDF (~50ms)

## Auto-Fit Logic

All templates must implement auto-fit behavior:

- Try to render at default font size (e.g., 10.5pt)
- If content overflows one page, progressively reduce font size
- Stop at minimum font size (default: 9pt)
- Report if content cannot fit even at minimum size

The auto-fit function can use heuristics (bullet count, content length) or Typst's `measure()` and `context` features for precise layout calculation.

## Adding New Templates

To add a new template:

1. Create a new directory: `templates/your-template-name/`
2. Create `template.typ` with an `auto-fit-resume(data, ...)` function
3. Ensure it accepts the standard JSON schema (see below)
4. Create `metadata.json` with template information
5. Generate `example.pdf` by compiling with sample data
6. Test with various content volumes to verify auto-fit works

## JSON Schema

Templates receive data in this format:

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
  "summary": "string (optional)",
  "education": [
    {
      "institution": "string",
      "degree": "string",
      "field": "string",
      "location": "string",
      "start_date": "YYYY-MM",
      "end_date": "YYYY-MM or 'Present'",
      "gpa": "string (optional)",
      "details": ["string"]
    }
  ],
  "experience": [
    {
      "company": "string",
      "role": "string",
      "location": "string",
      "start_date": "YYYY-MM",
      "end_date": "YYYY-MM or 'Present'",
      "bullets": ["string"]
    }
  ],
  "projects": [
    {
      "name": "string",
      "subtitle": "string (optional)",
      "dates": "string (optional)",
      "bullets": ["string"]
    }
  ],
  "skills": {
    "languages": ["string"],
    "frameworks": ["string"],
    "tools": ["string"],
    "concepts": ["string"]
  }
}
```

Not all fields are required. Templates should handle missing optional fields gracefully.

## Testing Templates

To test a template manually:

```bash
cd templates/your-template-name/
typst compile main.typ output.pdf
```

To test with the Rescume pipeline:

```bash
# Use the typst-renderer skill
python skills/typst-renderer/scripts/compile.py \
  --template your-template-name \
  --data sample_data.json \
  --output test_resume.pdf
```

## Dependencies

- Typst CLI (v0.11+)
- Templates may depend on Typst packages from `@preview`
- Fonts must be either bundled or available system-wide

## Resources

- [Typst Documentation](https://typst.app/docs)
- [Typst Universe](https://typst.app/universe) (template library)
- [simple-technical-resume package](https://typst.app/universe/package/simple-technical-resume/)
