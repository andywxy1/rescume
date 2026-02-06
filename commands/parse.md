---
name: parse
description: Parse DOCX resumes into the Rescume database
usage: /rescume parse or "build my resume database"
aliases: ["build", "import", "add-resume"]
---

# Parse Resume Command

Parse DOCX resume files into your comprehensive resume database.

## Usage

### Option 1: Slash Command
```
/rescume parse
```

### Option 2: Natural Language
```
Build my resume database
```
```
Parse my resume
```
```
Import my resumes into the database
```

## What Happens

1. **Upload Prompt**: Asks you to upload DOCX files
   - Can upload multiple resumes at once
   - Accepts different versions (technical, general, etc.)

2. **Parsing**: Resume parser extracts:
   - Personal information (name, contact, etc.)
   - Education entries
   - Work experiences with bullets
   - Skills mentioned
   - Projects (if present)

3. **Database Storage**: Saves structured data to:
   - `data/comprehensive_db/experiences.json`
   - `data/comprehensive_db/skills.json`
   - `data/comprehensive_db/education.json`
   - `data/comprehensive_db/projects.json`
   - `data/comprehensive_db/metadata.json`

4. **Enrichment Questions**: Interview Conductor asks follow-up questions:
   - Specific technologies used
   - Team sizes and scope
   - Quantifiable metrics
   - Details not in original resume

5. **Confirmation**: Shows what was extracted and saved

## Supported Formats

- ✅ DOCX (Microsoft Word)
- ❌ PDF (not supported - convert to DOCX first)
- ❌ Google Docs (download as DOCX first)
- ❌ Plain text (needs DOCX formatting)

## Multiple Resumes

You can upload multiple resume versions:
- Different jobs (Data Analyst, Data Scientist, etc.)
- Different styles (Technical, General, Academic)
- Different time periods (Old vs Updated)

Rescume will merge unique experiences and keep the most recent/relevant data.

## After Parsing

Your database is ready! You can now:
- Tailor resumes for specific jobs: `/rescume start`
- Check what's in your database: View `data/comprehensive_db/`
- Add more resumes anytime: `/rescume parse` again

## Examples

```bash
# Parse first resume
/rescume parse
[Upload resume_2024.docx]

# Add more resumes to existing database
/rescume parse
[Upload technical_resume.docx, general_resume.docx]

# Natural language
"I want to build my resume database"
[Upload files when prompted]
```

## Troubleshooting

**Issue**: "Cannot parse PDF"
- **Solution**: Convert to DOCX using Microsoft Word, Google Docs, or online converter

**Issue**: "Missing sections"
- **Solution**: Ensure your resume has clear section headers (Education, Experience, Skills)

**Issue**: "Database already exists"
- **Solution**: Rescume will merge new data with existing database
