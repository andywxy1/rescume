# 🚀 Rescume - AI Resume Tailoring System

**"Rescue My Resume"** - An intelligent multi-agent system with Typst-based PDF rendering for perfectly tailored resumes.

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/andywxy1/rescume/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Typst](https://img.shields.io/badge/typst-0.11+-orange.svg)](https://typst.app)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-purple.svg)](https://code.claude.com)

## 📋 Overview

Rescume is a Claude Code plugin that transforms your job application process with AI-powered resume tailoring and professional PDF rendering. Upload your existing resumes once, and Rescume will:

- ✅ Parse and build a comprehensive resume database
- ✅ Analyze job descriptions for ATS keywords and requirements
- ✅ Map your experiences to job requirements with 100% skill coverage
- ✅ Generate perfectly tailored single-page PDF resumes
- ✅ Auto-fit layout ensures content fits on one page
- ✅ Optimize for Applicant Tracking Systems (ATS)
- ✅ Deliver professional PDF output in <200ms

## ✨ What's New in v2.0

### 🎯 Typst-Based PDF Rendering

v2.0 introduces a revolutionary architecture shift:

- **No more DOCX formatting headaches** - Pure PDF output via Typst
- **Auto-fit templates** - Guaranteed single-page output
- **Lightning fast** - ~50-100ms compilation time
- **Deterministic rendering** - Same content → Same PDF, every time
- **LLM focuses on content** - No more word counting or layout concerns

**Migration from v1.0:** Database format unchanged. Just install Typst CLI and re-run tailoring for PDF output.

## ✨ Features

### 🤖 6 Specialized AI Agents

1. **Resume Parser** - Extracts structured data from DOCX/PDF resumes
2. **ATS Analyzer** - Identifies job requirements and keywords
3. **Coverage Mapper** - Maps experiences to requirements, finds gaps
4. **Content Generator** - Creates tailored resume content (JSON output)
5. **HR Critic** - Evaluates content quality from hiring manager perspective
6. **Interview Conductor** - Asks intelligent follow-up questions to enrich database

### 🛠️ 4 Custom Skills (Tools)

1. **Rescume Coordinator** - Orchestrates the entire workflow
2. **JSON Database** - Manages your resume data persistently
3. **Typst Renderer** - Compiles JSON content to professional PDF
4. **Coverage Tracker** - Verifies all required skills are present

### 🎨 Template System

- **Modular Typst templates** - Multiple professional designs
- **Auto-fit logic** - Automatically adjusts font size (9-10.5pt) to fit content
- **Simple Technical Resume** - Clean, ATS-friendly single-column layout (v2.0 default)
- **Extensible** - Easy to add custom templates

### 🎯 Key Capabilities

- **Intelligent Content Selection**: AI chooses most relevant experiences
- **ATS Optimization**: Exact keyword matching from job descriptions
- **Quality Assurance**: HR Critic ensures professional quality
- **Fast Iteration**: Typst renders in ~50ms, making revisions instant
- **Safety Checks**: Guarantees 100% coverage of required skills
- **Growing Database**: Each application enriches your resume database

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Typst CLI** (v0.11+)
- **Claude Code** (latest version)

### Installation

#### Step 1: Install Typst CLI

```bash
# macOS (via Homebrew)
brew install typst

# Linux
curl -fsSL https://typst.community | bash

# Windows
winget install --id Typst.Typst

# Verify installation
typst --version
```

#### Step 2: Install Rescume Plugin

**Via Claude Code Marketplace:**
```bash
# Add the marketplace
claude plugin marketplace add andywxy1/rescume

# Install the plugin
claude plugin install rescume@andy-plugins
```

**Or Manual Installation:**
```bash
# Clone repository
git clone https://github.com/andywxy1/rescume.git
cd rescume

# Install Python dependencies
pip install python-docx pdfplumber --break-system-packages

# The plugin is ready to use from this directory
```

#### Step 3: Verify Installation

```bash
# Check that Typst is accessible
typst --version

# List available templates
python skills/typst-renderer/scripts/list_templates.py
```

### First Use

#### Phase 1: Build Your Resume Database (One-Time Setup)

```
"I want to build my resume database"
```

1. Upload your existing resumes (DOCX format)
2. Rescume parses them into structured JSON
3. Answer follow-up questions to enrich your database
4. Database saved to `data/comprehensive_db/`

**What gets stored:**
- Work experiences with bullet points
- Education history
- Skills with proficiency levels
- Projects and achievements
- Contact information

#### Phase 2: Tailor Resume for a Job

```
"Tailor my resume for this [Job Title] role at [Company]"
```

1. **Provide Job Description** - Paste text or upload file
2. **ATS Analysis** - Identifies required skills and keywords
3. **Coverage Mapping** - Maps your experiences to requirements
4. **Content Generation** - Creates tailored JSON content
5. **Template Selection** - Choose from available templates
6. **PDF Rendering** - Typst compiles to single-page PDF
7. **Quality Check** - HR Critic evaluates content
8. **Download** - Get your optimized PDF resume

**Output:** `data/job_applications/[job_id]/resume.pdf`

## 📖 How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: Database Building (One-Time)                            │
│                                                                   │
│  DOCX Resume → resume-parser → Structured JSON Database          │
│                 ↓                                                 │
│            interview-conductor → Enriched Database                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: Resume Tailoring (Per Job Application)                  │
│                                                                   │
│  Job Description                                                  │
│       ↓                                                           │
│  ats-analyzer → Requirements JSON                                 │
│       ↓                                                           │
│  coverage-mapper → Coverage Matrix + Prioritized Experiences      │
│       ↓                                                           │
│  content-generator → Structured JSON Content                      │
│       ↓                                                           │
│  User selects Typst template                                      │
│       ↓                                                           │
│  typst-renderer → Single-Page PDF                                 │
│       ↓                                                           │
│  hr-critic → Quality Validation                                   │
│       ↓                                                           │
│  Deliver PDF Resume                                               │
└─────────────────────────────────────────────────────────────────┘
```

### Key Workflow Changes in v2.0

**v1.0 (DOCX-based):**
```
Generate DOCX → Count words → Too long? → Compress → Recount → Repeat...
❌ Slow, unpredictable, required ~10 iterations
```

**v2.0 (Typst-based):**
```
Generate JSON → Typst compile → PDF done! (~50ms)
✅ Fast, deterministic, single-pass rendering
```

**If content is too dense:**
```
Typst reports "font too small" → Trim 2-3 bullets → Recompile → Done!
✅ Simple, fast, no complex compression logic needed
```

## 🗂️ Project Structure

```
rescume/
├── .claude-plugin/
│   ├── plugin.json              # Plugin metadata
│   └── marketplace.json         # Marketplace configuration
│
├── agents/                      # AI agent definitions
│   ├── ats-analyzer.md          # Job requirement analysis
│   ├── content-generator.md     # JSON content generation
│   ├── coverage-mapper.md       # Requirement mapping
│   ├── hr-critic.md             # Quality evaluation
│   ├── interview-conductor.md   # Database enrichment
│   └── resume-parser.md         # DOCX parsing
│
├── skills/                      # Tool skills
│   ├── rescume/                 # Main coordinator
│   ├── json-database/           # Database management
│   ├── typst-renderer/          # PDF compilation (NEW v2.0)
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       ├── compile.py           # Main compiler
│   │       ├── json_to_typst.py     # JSON → Typst converter
│   │       ├── validate_pdf.py      # PDF validation
│   │       └── list_templates.py    # Template discovery
│   └── coverage-tracker/        # Skill verification
│
├── templates/                   # Typst resume templates (NEW v2.0)
│   ├── README.md                # Template authoring guide
│   └── simple-technical-resume/ # Default template
│       ├── template.typ         # Main template with auto-fit
│       ├── metadata.json        # Template info
│       ├── main.typ             # Example usage
│       └── example.pdf          # Preview
│
├── hooks/
│   └── hooks.json               # Installation hooks
│
├── data/                        # Runtime data (created on install)
│   ├── comprehensive_db/        # Your resume database
│   │   ├── experiences.json
│   │   ├── skills.json
│   │   ├── projects.json
│   │   ├── education.json
│   │   └── metadata.json
│   └── job_applications/        # Per-job outputs
│       └── [job_id]/
│           ├── jd_analyzed.json      # Job requirements
│           ├── coverage_matrix.json  # Skill mapping
│           ├── content.json          # Generated content
│           └── resume.pdf            # Final output
│
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## 🎨 Templates

Rescume v2.0 uses Typst templates for professional PDF rendering. Each template includes auto-fit logic to ensure single-page output.

### Available Templates

**simple-technical-resume** (Default)
- Clean, ATS-friendly single-column layout
- Auto-fit font sizing (9-10.5pt)
- Perfect for software engineers, data scientists, technical roles
- Based on Typst Universe package

### Adding Custom Templates

See `templates/README.md` for the template authoring guide.

Requirements:
- Accept standard JSON schema
- Implement auto-fit logic
- Provide metadata.json
- Generate single-page output

## 🔧 Configuration

Rescume works out-of-the-box with sensible defaults. Advanced users can customize via plugin settings.

### Plugin Settings

**Template Configuration:**
- `rescume.defaultTemplate`: Default template name (default: `"simple-technical-resume"`)
- `rescume.minFontSize`: Minimum font size after auto-fit (default: `9.0` pt)
- `rescume.typstPath`: Path to Typst CLI binary (default: `"typst"`)
- `rescume.templateDir`: Template directory path (default: `"templates/"`)

**Database Configuration:**
- `rescume.databasePath`: Resume database location (default: `"data/comprehensive_db"`)
- `rescume.autoBackup`: Auto-backup database after changes (default: `true`)

**Quality Thresholds:**
- `rescume.qualityThreshold`: Minimum HR Critic score (default: `7.0` out of 10)
- `rescume.hireProbabilityThreshold`: Minimum hire probability (default: `0.70`)

## 📚 Documentation

- **[CHANGELOG.md](CHANGELOG.md)** - Version history and migration notes
- **[RESCUME_V2_UPDATE_PLAN.md](RESCUME_V2_UPDATE_PLAN.md)** - v2.0 architecture rationale
- **[templates/README.md](templates/README.md)** - Template authoring guide
- **[skills/typst-renderer/SKILL.md](skills/typst-renderer/SKILL.md)** - Rendering pipeline docs

## 🐛 Troubleshooting

### "Typst CLI not found"

```bash
# Install Typst
brew install typst  # macOS
# Or visit https://typst.app for other platforms

# Verify
typst --version
```

### "pdfplumber not installed"

```bash
pip install pdfplumber --break-system-packages
```

### "Resume overflows 1 page"

The auto-fit template reports this when content is too dense even at minimum font size (9pt).

**Solution:** Ask the LLM to trim 2-3 bullet points:
```
"The resume is too long. Please remove 2-3 less relevant bullet points and recompile."
```

### "Invalid JSON schema"

Content generator produced invalid JSON. Check:
- All required fields present (`header.name` at minimum)
- Dates in `YYYY-MM` format
- No unescaped quotes in strings

## 🤝 Contributing

Contributions welcome! Areas of interest:

- **New Typst Templates** - Design new resume styles
- **Enhanced Parsers** - Support more input formats (PDF, LinkedIn, etc.)
- **Improved ATS Analysis** - Better keyword extraction
- **Multi-Page Support** - Option for longer resumes (CV format)
- **Internationalization** - Support for non-English resumes

See `CONTRIBUTING.md` for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Typst** - Modern typesetting system (https://typst.app)
- **simple-technical-resume** - Typst template by Himank Dave
- **Claude Code** - AI-powered development environment
- **Anthropic** - Claude Sonnet 4.5 AI model

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/andywxy1/rescume/issues)
- **Discussions:** [GitHub Discussions](https://github.com/andywxy1/rescume/discussions)
- **Email:** andywen718@gmail.com

---

**Built with ❤️ by Andy Wen**

*Rescue your resume, land your dream job!*
