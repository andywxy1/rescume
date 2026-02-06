# 🚀 Rescume - AI Resume Tailoring System

**"Rescue My Resume"** - An intelligent multi-agent system for tailoring resumes to specific job descriptions.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/andywxy1/rescume/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-purple.svg)](https://code.claude.com)

## 📋 Overview

Rescume is a Claude Code plugin that transforms your job application process. Upload your existing resumes once, and Rescume will:

- ✅ Parse and build a comprehensive resume database
- ✅ Analyze job descriptions for ATS keywords and requirements
- ✅ Map your experiences to job requirements
- ✅ Generate perfectly tailored one-page resumes
- ✅ Optimize for Applicant Tracking Systems (ATS)
- ✅ Guarantee 100% coverage of required skills
- ✅ Deliver both DOCX (editable) and PDF (submission) versions

## ✨ Features

### 🤖 7 Specialized AI Agents

1. **Resume Parser** - Extracts structured data from DOCX resumes
2. **ATS Analyzer** - Identifies job requirements and keywords
3. **Coverage Mapper** - Maps experiences to requirements, finds gaps
4. **Content Generator** - Creates tailored resume content
5. **HR Critic** - Evaluates quality from hiring manager perspective
6. **Compression Strategist** - Optimizes to fit one page
7. **Interview Conductor** - Asks intelligent follow-up questions

### 🛠️ 4 Custom Skills (Tools)

1. **Rescume Coordinator** - Orchestrates the entire workflow
2. **JSON Database** - Manages your resume data persistently
3. **Word Counter** - Section-by-section word tracking
4. **Coverage Tracker** - Verifies all required skills are present

### 🎯 Key Capabilities

- **Template Preservation**: Uses your resume formatting style
- **Section-Based Optimization**: Only edits Experience & Skills sections
- **Quality Assurance**: HR Critic ensures professional quality
- **Safety Checks**: Never loses required skills during compression
- **User Validation**: Always confirms page count before finalizing
- **Growing Database**: Each application enriches your database

## 🚀 Quick Start

### Installation

#### Option 1: Install via Claude Code CLI

```bash
claude plugin install https://github.com/andywxy1/rescume
```

#### Option 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/andywxy1/rescume.git
cd rescume

# Copy skills
cp -r skills/* ~/.claude/skills/user/

# Copy agents
cp -r agents/* ~/.claude/agents/

# Install Python dependencies
pip install python-docx --break-system-packages

# Restart Claude Code
```

### First Use

1. **Build Your Database** (One-time setup)
   ```
   "I want to build my resume database"
   ```
   - Upload your existing DOCX resumes
   - Answer follow-up questions to enrich data

2. **Tailor for a Job**
   ```
   "Tailor my resume for this [Job Title] role at [Company]"
   ```
   - Upload or paste job description
   - Review coverage and fill any gaps
   - Approve final resume

3. **Get Your Resume**
   - Download DOCX (editable)
   - Download PDF (for submission)

## 📖 How It Works

### Phase 1: Initial Setup (One-Time)

```
Upload DOCX Resumes
    ↓
Resume Parser → Extracts structure
    ↓
Interview Conductor → Asks questions
    ↓
Database Built (experiences, skills, projects, education)
```

### Phase 2: Tailoring (For Each Job)

```
Upload Job Description
    ↓
ATS Analyzer → Extracts requirements
    ↓
Coverage Mapper → Checks skill coverage (must reach 100%)
    ↓
    [If gaps] → Interview Conductor (gap filling)
    ↓
Content Generator → Creates initial draft (~600 words)
    ↓
HR Critic (comprehensive) → Evaluates quality
    ↓
Apply improvements (may exceed 1 page)
    ↓
Compression Strategist → Optimizes to ~475 words
    ↓
    [If stuck] → HR Critic (triage) → Makes strategic decision
    ↓
HR Critic (final validation) → Ship/no-ship decision
    ↓
Final Resume: DOCX + PDF
```

## 💡 Usage Examples

### Example 1: Complete Workflow

```
User: "I want to tailor my resume for Senior Data Analyst at PCI Energy"

Claude: [Uploads job description]
Claude (using Rescume):
  ✓ Analyzed JD: 20 requirements (12 must-have, 8 nice-to-have)
  ✓ Checked coverage: 85% (missing Kubernetes)
  
  Question: "This role requires Kubernetes. Do you have container 
  orchestration experience?"
  
User: "Yes, I used Docker extensively at Company X"

Claude:
  ✓ Updated database with Docker experience
  ✓ Coverage now 100%
  ✓ Generated initial draft (550 words)
  ✓ HR critique applied
  ✓ Compressed to 485 words
  ✓ Final validation: APPROVED (hire probability: 78%)
  
  Here's your tailored resume [DOCX + PDF]
```

### Example 2: Using Slash Commands

```bash
# Parse your resumes first
/rescume parse
[Upload resume_2024.docx, technical_resume.docx]

# Analyze a job description
/rescume analyze
[Paste job description]

# Start tailoring
/rescume start Senior Data Analyst
[Follow the prompts]
```

## 📂 File Structure

After using Rescume, you'll have:

```
data/
├── comprehensive_db/          # Your persistent resume database
│   ├── experiences.json       # Work experiences
│   ├── skills.json           # All skills
│   ├── projects.json         # Projects
│   ├── education.json        # Education
│   └── metadata.json         # Personal info
│
├── uploaded_resumes/         # Original DOCX templates
│   └── *.docx
│
└── job_applications/         # Per-job directories
    └── pci_energy_analyst_2024_02_05/
        ├── jd_original.txt
        ├── jd_analyzed.json
        ├── coverage_matrix.json
        ├── working_resume.docx
        ├── final_resume.docx
        └── final_resume.pdf
```

## ⚙️ Configuration

Customize Rescume settings in Claude Code preferences:

```json
{
  "rescume.targetWordCount": 475,
  "rescume.qualityThreshold": 7.0,
  "rescume.hireProbabilityThreshold": 0.70,
  "rescume.maxCompressionIterations": 10,
  "rescume.databasePath": "data/comprehensive_db",
  "rescume.autoBackup": true
}
```

## 🔧 Requirements

- **Claude Code**: 1.0.0 or higher
- **Python**: 3.8 or higher
- **python-docx**: 0.8.11 or higher
- **DOCX files**: Input must be Word documents (not PDF)

## 📚 Documentation

- [Getting Started Guide](docs/getting-started.md) *(coming soon)*
- [User Guide](docs/user-guide.md) *(coming soon)*
- [Architecture Overview](docs/architecture.md) *(coming soon)*
- [Troubleshooting](docs/troubleshooting.md) *(coming soon)*

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Coverage stuck at 90%"
- **Solution**: Answer gap-filling questions about missing skills

**Issue**: "Resume is 1.1 pages after compression"
- **Solution**: Provide feedback, system will compress further

**Issue**: "Database not found"
- **Solution**: Run initial setup first to build database: `/rescume parse`

**Issue**: "Cannot parse PDF resume"
- **Solution**: Rescume only works with DOCX files, convert PDF to DOCX first

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Andy (Xiangyi Wen)**
- Data Scientist specializing in Product Analytics
- M.S.E. in Data Science, University of Pennsylvania
- GitHub: [@andywxy1](https://github.com/andywxy1)
- Email: andywen718@gmail.com

## 🙏 Acknowledgments

- Built with [Claude Code](https://code.claude.com)
- Powered by Claude 4.5 Sonnet
- Inspired by the challenges of modern job applications

## 📊 Stats

- **7 AI Agents** with specialized expertise
- **4 Custom Skills** for resume processing
- **~2,500 lines** of carefully crafted prompts
- **100% skill coverage** guarantee
- **One-page optimization** using word count heuristics

## 🚀 Roadmap

- [ ] Support for multi-page resumes
- [ ] PDF input support (OCR-based)
- [ ] LinkedIn profile optimization
- [ ] Cover letter generation
- [ ] Interview preparation questions
- [ ] Job application tracking
- [ ] Resume templates library
- [ ] Multilingual support

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/andywxy1/rescume/issues)
- **Discussions**: [GitHub Discussions](https://github.com/andywxy1/rescume/discussions)
- **Email**: andywen718@gmail.com

---

**Ready to rescue your resume?** 🎉

Install Rescume today and transform your job application process!

**Star this repo** ⭐ if you find it helpful!
