# Changelog

All notable changes to the Rescume plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-05

### 🎉 Initial Release

**Rescume v1.0.0** - AI-Powered Resume Tailoring System

### Added

#### Core Features
- **7 Specialized AI Agents**:
  - `resume-parser`: Parse DOCX resumes into structured JSON
  - `ats-analyzer`: Analyze job descriptions for ATS keywords
  - `coverage-mapper`: Map experiences to job requirements
  - `content-generator`: Generate tailored resume content
  - `hr-critic`: Evaluate resume quality (3 modes: comprehensive, triage, final validation)
  - `compression-strategist`: Optimize word count to fit one page
  - `interview-conductor`: Generate intelligent follow-up questions

- **4 Custom Skills**:
  - `rescume`: Main coordinator orchestrating the workflow
  - `json-database`: Resume data management (5 Python scripts)
  - `word-counter`: Section-by-section word counting
  - `coverage-tracker`: Skill coverage verification

- **Database System**:
  - Persistent JSON storage for resume data
  - Automatic ID generation
  - Database validation and integrity checks
  - Backup system for data safety

- **Resume Optimization**:
  - Section-based word count tracking (Header, Education, Experience, Skills)
  - Target: 475 words for one-page format
  - Only edits Experience and Skills sections
  - Preserves user's original template formatting

- **Quality Assurance**:
  - HR Critic evaluation (1-10 scoring)
  - Hire probability estimation
  - ATS keyword optimization
  - 100% required skill coverage guarantee

- **User Experience**:
  - Natural language triggering ("tailor my resume for...")
  - Custom slash commands (`/rescume start`, `/rescume parse`, `/rescume analyze`)
  - Interactive follow-up questions
  - User validation loop before finalizing

#### Custom Commands
- `/rescume start`: Start tailoring workflow
- `/rescume parse`: Parse resume into database
- `/rescume analyze`: Analyze job description

#### Lifecycle Hooks
- `onInstall`: Initialize database and install dependencies
- `onUpdate`: Migrate database and backup data
- `onUninstall`: Clean up with user confirmation

#### Configuration Options
- `rescume.targetWordCount`: Target word count (default: 475)
- `rescume.qualityThreshold`: Minimum quality score (default: 7.0)
- `rescume.hireProbabilityThreshold`: Minimum hire probability (default: 0.70)
- `rescume.maxCompressionIterations`: Max compression iterations (default: 10)
- `rescume.databasePath`: Database location (default: data/comprehensive_db)
- `rescume.autoBackup`: Auto-backup database (default: true)

### Technical Details

- **Python Version**: 3.8+
- **Dependencies**: python-docx >= 0.8.11
- **File Format**: DOCX input/output (PDF not supported)
- **Storage**: Local JSON files (~50MB for plugin + variable for user data)

### Workflow

**Phase 1: Initial Setup (One-Time)**
1. User uploads DOCX resume(s)
2. Resume Parser extracts structured data
3. Interview Conductor asks enrichment questions
4. Comprehensive database built

**Phase 2: Tailoring (Per Job)**
1. User provides job description
2. ATS Analyzer extracts requirements
3. Coverage Mapper checks skill coverage
4. Interview Conductor fills gaps (if needed)
5. Content Generator creates draft (~550-600 words)
6. HR Critic evaluates and provides feedback
7. Compression Strategist optimizes to ~475 words
8. HR Critic final validation
9. Deliver DOCX + PDF

### Known Limitations

- DOCX files only (PDF conversion not supported)
- Requires manual user validation of page count
- One-page format only (multi-page support planned)
- English language only (multilingual support planned)

### Documentation

- README.md with installation and usage guide
- LICENSE (MIT)
- Command documentation (start.md, parse.md, analyze.md)
- Comprehensive inline documentation in agents and skills

---

## Unreleased

### Planned Features
- [ ] Multi-page resume support
- [ ] PDF input support (OCR-based)
- [ ] LinkedIn profile optimization
- [ ] Cover letter generation
- [ ] Interview preparation questions
- [ ] Resume templates library
- [ ] Multilingual support (Spanish, Mandarin)
- [ ] Job application tracking
- [ ] Browser extension for one-click apply
- [ ] Integration with job boards (LinkedIn, Indeed)

### Potential Improvements
- [ ] Performance optimization for large databases
- [ ] Cloud backup option
- [ ] Collaborative features (share database with career coach)
- [ ] A/B testing for resume variants
- [ ] Analytics dashboard (application success rate)
- [ ] Mobile app (iOS/Android)

---

## Version History Summary

- **v1.0.0** (2026-02-05): Initial public release

---

**Note**: For detailed commit history, see [GitHub Commits](https://github.com/andywxy1/rescume/commits/main)
