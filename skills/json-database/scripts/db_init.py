#!/usr/bin/env python3
"""Initialize empty resume database structure."""

import argparse
import json
import os
from pathlib import Path


def create_empty_database(output_path: str) -> None:
    """Create empty database files with proper structure."""
    db_path = Path(output_path)
    db_path.mkdir(parents=True, exist_ok=True)
    
    # Empty structures
    empty_experiences = {"experiences": []}
    empty_skills = {"skills": []}
    empty_projects = {"projects": []}
    empty_education = {"education": []}
    empty_metadata = {
        "name": "",
        "email": "",
        "phone": "",
        "location": "",
        "linkedin": "",
        "github": "",
        "portfolio": "",
        "last_updated": ""
    }
    
    # Write files
    files = {
        "experiences.json": empty_experiences,
        "skills.json": empty_skills,
        "projects.json": empty_projects,
        "education.json": empty_education,
        "metadata.json": empty_metadata
    }
    
    for filename, data in files.items():
        filepath = db_path / filename
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Created: {filepath}")
    
    print(f"\n✓ Database initialized at: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Initialize resume database")
    parser.add_argument("--output", required=True, help="Output directory path")
    
    args = parser.parse_args()
    
    try:
        create_empty_database(args.output)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
