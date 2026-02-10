# Changelog - Rescume

All notable changes to the Rescume project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-10

### 🚀 Major Changes

- **BREAKING**: Switched from DOCX output to Typst-based PDF rendering
- **BREAKING**: Output format is now PDF (compiled by Typst), not DOCX
- **BREAKING**: LLM generates structured JSON content only, no formatting decisions
- **BREAKING**: Removed iterative word-count compression workflow

### ✨ Added

- **Auto-fit Typst templates** guarantee single-page output without iteration
- **typst-renderer skill** for PDF compilation with automatic font-size adjustment
- **Template selection system** with multiple professional Typst templates
- **JSON content schema** for structured resume data
- **Deterministic rendering** - same content always produces same PDF
- **templates/ directory** with extensible template system
- **Fast compilation** - complete pipeline in 50-200ms

### ❌ Removed

- **compression-strategist agent** - replaced by auto-fit templates
- **word-counter skill** - no longer needed (Typst measures actual content)
- **Iterative compression workflow** - auto-fit handles page fitting
- **Word count targets and tracking** (475 words, etc.)
- **HR triage mode** from hr-critic agent

### 🔄 Changed

- **content-generator** now outputs structured JSON instead of formatted DOCX
- **hr-critic** removed triage mode (only comprehensive and final_validation remain)
- **coverage-mapper** simplified (removed word budget logic)
- **Phase 2 workflow** significantly streamlined (7 steps → 7 simpler steps)
- **LLM role** changed from "layout engineer" to "content writer only"

### 📈 Improvements

- **10x faster workflow** - no compression iterations needed
- **More reliable** - deterministic Typst compilation vs. LLM guessing
- **Better quality** - LLM focuses on content, not layout constraints
- **Simpler codebase** - removed ~500 lines of compression logic
- **Easier to maintain** - separation of concerns (content vs. layout)

### 🛠 Technical

- Added dependency: **Typst CLI** (system binary) v0.14.2+
- Added dependency: **pdfplumber** (Python package)
- Added dependency: **jsonschema** (Python package)
- Removed dependency: DOCX-to-PDF conversion tools
- **Python 3.8+** required

### 📚 Documentation

- Updated rescume SKILL.md with v2.0 workflow
- Added AUTO_FIT_RESEARCH.md explaining approach
- Added content_schema.json and example
- Added AGENT_UPDATES_NEEDED.md for maintainers
- Updated coverage-tracker to remove compression references

### 🧪 Testing

- End-to-end pipeline tested with realistic resumes
- Auto-fit verified with overflow scenarios
- PDF validation working correctly
- Template system tested with multiple templates

---

## [1.0.0] - 2026-02-05

### Initial Release

- DOCX-based resume tailoring system
- Multi-agent architecture
- Word-count compression workflow
- coverage-tracker for skill verification
- json-database for resume data storage
- Support for job-specific resume generation

---

## Migration Guide

See [MIGRATION.md](MIGRATION.md) for guide on upgrading from v1.0 to v2.0.
