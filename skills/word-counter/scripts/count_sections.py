#!/usr/bin/env python3
"""Count words by section in DOCX resume files."""

import argparse
import json
import sys
from pathlib import Path

try:
    from docx import Document
except ImportError:
    print("Error: python-docx not installed. Run: pip install python-docx", file=sys.stderr)
    sys.exit(1)


# Default section headers (case-insensitive matching)
DEFAULT_HEADERS = {
    "education": ["education", "academic background", "academic", "academics"],
    "experience": ["experience", "work experience", "professional experience", "employment"],
    "skills": ["skills", "technical skills", "core competencies", "expertise", "proficiencies"]
}


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def detect_section(paragraph_text: str, headers: dict) -> str:
    """Detect which section a paragraph belongs to."""
    text_lower = paragraph_text.lower().strip()
    
    for section, patterns in headers.items():
        for pattern in patterns:
            if text_lower.startswith(pattern) or text_lower == pattern:
                return section
    
    return None


def count_sections(docx_path: str, custom_headers: dict = None) -> dict:
    """Count words by section in DOCX file."""
    doc = Document(docx_path)
    
    headers = custom_headers if custom_headers else DEFAULT_HEADERS
    
    # Initialize sections
    sections = {
        "header": {"words": 0, "editable": False, "lines": []},
        "education": {"words": 0, "editable": False, "lines": []},
        "experience": {"words": 0, "editable": True, "lines": []},
        "skills": {"words": 0, "editable": True, "lines": []},
        "other": {"words": 0, "editable": False, "lines": []}
    }
    
    current_section = "header"
    
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        
        if not text:
            continue
        
        # Check if this is a section header
        detected = detect_section(text, headers)
        if detected:
            current_section = detected
            continue  # Don't count the header itself
        
        # Count words in this paragraph
        words = count_words(text)
        sections[current_section]["words"] += words
        sections[current_section]["lines"].append(i)
    
    # Calculate totals and targets
    total_words = sum(s["words"] for s in sections.values())
    experience_words = sections["experience"]["words"]
    skills_words = sections["skills"]["words"]
    
    # Set targets (based on 475 total target)
    fixed_words = sections["header"]["words"] + sections["education"]["words"] + sections["other"]["words"]
    available_for_content = 475 - fixed_words
    
    # Allocate 80% to experience, 20% to skills (rough heuristic)
    experience_target = int(available_for_content * 0.75)
    skills_target = int(available_for_content * 0.15)
    
    # Build result
    result = {}
    for section, data in sections.items():
        if data["words"] > 0:  # Only include non-empty sections
            result[section] = {
                "words": data["words"],
                "editable": data["editable"]
            }
            
            if section == "experience":
                result[section]["target"] = experience_target
            elif section == "skills":
                result[section]["target"] = skills_target
    
    # Add summary
    result["total"] = total_words
    result["target"] = 475
    result["reduction_needed"] = max(0, total_words - 475)
    result["estimated_pages"] = round(total_words / 500, 2)
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Count words by section in DOCX")
    parser.add_argument("docx_file", help="Path to DOCX file")
    parser.add_argument("--headers", help="JSON mapping of custom section headers")
    
    args = parser.parse_args()
    
    try:
        custom_headers = json.loads(args.headers) if args.headers else None
        result = count_sections(args.docx_file, custom_headers)
        print(json.dumps(result, indent=2))
        return 0
    except FileNotFoundError:
        print(f"Error: File not found: {args.docx_file}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit(main())
