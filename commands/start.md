---
name: start
description: Start the Rescume resume tailoring workflow for a specific job
usage: /rescume start [job-title] or just say "tailor my resume for [job]"
aliases: ["begin", "tailor"]
---

# Start Rescume Workflow

Initiates the complete resume tailoring process.

## Usage

You can trigger Rescume in multiple ways:

### Option 1: Slash Command
```
/rescume start Senior Data Analyst at PCI Energy
```

### Option 2: Natural Language (Recommended)
```
Tailor my resume for Senior Data Analyst at PCI Energy
```
```
I want to apply for Data Scientist role at Google
```
```
Help me customize my resume for this job [paste JD]
```

**Note**: The rescume skill automatically triggers when you mention tailoring, customizing, or applying for a job. You don't need to use slash commands unless you prefer them!

## What Happens

1. **Database Check**: Verifies your resume database exists
   - If empty: Prompts you to upload resumes first
   - If exists: Proceeds to JD analysis

2. **Job Description**: Asks for JD (paste or upload)

3. **Analysis**: ATS analyzer extracts requirements

4. **Coverage Check**: Maps your experiences to requirements

5. **Gap Filling**: If skills are missing, asks follow-up questions

6. **Content Generation**: Creates tailored resume draft

7. **Quality Review**: HR Critic evaluates content

8. **Compression**: Optimizes to one page

9. **Validation**: Final quality check

10. **Delivery**: DOCX + PDF files

## Parameters

- `[job-title]`: Optional. Can specify job title inline
- `--skip-coverage`: Skip coverage check (not recommended)
- `--target-words <N>`: Override default target word count (475)

## Examples

```bash
# Start with job title
/rescume start Data Analyst

# Start and paste JD
/rescume start
[Then paste job description when prompted]

# Natural language (best)
"I want to tailor my resume for the Senior Data Analyst role at PCI Energy"
```

## First Time Using Rescume?

If you haven't built your database yet:

```
/rescume parse
[Upload your DOCX resumes]
```

Then come back and use `/rescume start`!
