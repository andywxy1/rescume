#!/usr/bin/env python3
"""Check skill coverage in resume against job requirements."""

import argparse
import json
import sys
from pathlib import Path

try:
    from docx import Document
except ImportError:
    print("Error: python-docx not installed. Run: pip install python-docx", file=sys.stderr)
    sys.exit(1)


def extract_text_from_docx(docx_path: str) -> str:
    """Extract all text from DOCX file."""
    doc = Document(docx_path)
    return " ".join([para.text for para in doc.paragraphs])


def check_skill_in_text(skill: str, text: str) -> tuple[bool, float]:
    """
    Check if skill is mentioned in text.
    Returns (found, relevance_score).
    """
    text_lower = text.lower()
    skill_lower = skill.lower()
    
    # Exact match
    if skill_lower in text_lower:
        return True, 1.0
    
    # Check for common variations
    variations = {
        "ml": ["machine learning", "ml", "deep learning"],
        "a/b testing": ["a/b testing", "ab testing", "experimentation", "experiments"],
        "sql": ["sql", "structured query language", "database queries"],
        "aws": ["aws", "amazon web services", "s3", "ec2", "lambda"],
        "python": ["python", "py", "pandas", "numpy"]
    }
    
    if skill_lower in variations:
        for variant in variations[skill_lower]:
            if variant in text_lower:
                return True, 0.9
    
    # Check if any word from skill appears (weak match)
    skill_words = skill_lower.split()
    matches = sum(1 for word in skill_words if word in text_lower)
    if matches > 0:
        relevance = matches / len(skill_words)
        if relevance >= 0.5:
            return True, relevance
    
    return False, 0.0


def check_coverage(resume_path: str, requirements_path: str) -> dict:
    """Check coverage of required skills in resume."""
    
    # Load requirements
    with open(requirements_path, 'r') as f:
        requirements = json.load(f)
    
    # Extract resume text
    resume_text = extract_text_from_docx(resume_path)
    
    # Analyze coverage
    skill_coverage = {}
    must_have_skills = []
    nice_to_have_skills = []
    
    for req in requirements.get("required_skills", []):
        skill = req["skill"]
        category = req.get("category", "must_have")
        importance = req.get("importance", 5)
        
        # Check if skill is in resume
        found, relevance = check_skill_in_text(skill, resume_text)
        
        skill_coverage[skill] = {
            "required": True,
            "covered": found,
            "importance": importance,
            "relevance": relevance if found else 0.0,
            "category": category
        }
        
        if category == "must_have":
            must_have_skills.append(skill)
        else:
            nice_to_have_skills.append(skill)
    
    # Calculate coverage metrics
    total_required = len(skill_coverage)
    total_covered = sum(1 for s in skill_coverage.values() if s["covered"])
    
    must_have_total = len(must_have_skills)
    must_have_covered = sum(1 for s in must_have_skills if skill_coverage[s]["covered"])
    
    nice_to_have_total = len(nice_to_have_skills)
    nice_to_have_covered = sum(1 for s in nice_to_have_skills if skill_coverage[s]["covered"]) if nice_to_have_total > 0 else 0
    
    coverage_percentage = total_covered / total_required if total_required > 0 else 1.0
    must_have_coverage = must_have_covered / must_have_total if must_have_total > 0 else 1.0
    nice_to_have_coverage = nice_to_have_covered / nice_to_have_total if nice_to_have_total > 0 else 1.0
    
    # Find missing skills
    missing_skills = [skill for skill, data in skill_coverage.items() if not data["covered"]]
    
    # Determine status
    if must_have_coverage < 1.0:
        status = "critical_gaps"
    elif coverage_percentage < 0.8:
        status = "incomplete"
    else:
        status = "good"
    
    return {
        "skill_coverage": skill_coverage,
        "coverage_percentage": round(coverage_percentage, 2),
        "must_have_coverage": round(must_have_coverage, 2),
        "nice_to_have_coverage": round(nice_to_have_coverage, 2),
        "total_required": total_required,
        "total_covered": total_covered,
        "status": status,
        "missing_skills": missing_skills
    }


def main():
    parser = argparse.ArgumentParser(description="Check skill coverage in resume")
    parser.add_argument("--resume", required=True, help="Path to resume DOCX file")
    parser.add_argument("--requirements", required=True, help="Path to JD requirements JSON")
    
    args = parser.parse_args()
    
    try:
        result = check_coverage(args.resume, args.requirements)
        print(json.dumps(result, indent=2))
        
        # Exit code based on status
        if result["status"] == "critical_gaps":
            return 1  # Missing must-have skills
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit(main())
