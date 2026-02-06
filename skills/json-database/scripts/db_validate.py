#!/usr/bin/env python3
"""Validate resume database structure and integrity."""

import argparse
import json
import sys
from pathlib import Path


def validate_database(db_path: str) -> tuple[bool, list]:
    """Validate database structure and return (is_valid, errors)."""
    db_path = Path(db_path)
    errors = []
    
    # Check directory exists
    if not db_path.exists():
        errors.append(f"Database directory not found: {db_path}")
        return False, errors
    
    # Check required files
    required_files = ["experiences.json", "skills.json", "projects.json", "education.json", "metadata.json"]
    
    for filename in required_files:
        filepath = db_path / filename
        if not filepath.exists():
            errors.append(f"Missing required file: {filename}")
            continue
        
        # Validate JSON
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in {filename}: {e}")
            continue
        
        # Validate structure
        if filename == "metadata.json":
            required_keys = ["name", "email"]
            for key in required_keys:
                if key not in data:
                    errors.append(f"Missing required key '{key}' in metadata.json")
        else:
            # Other files should have a key matching the filename
            key = filename.replace('.json', '')
            if key not in data:
                errors.append(f"Missing key '{key}' in {filename}")
            elif not isinstance(data[key], list):
                errors.append(f"Key '{key}' in {filename} should be a list")
            else:
                # Check for unique IDs
                ids = [entry.get('id') for entry in data[key] if 'id' in entry]
                if len(ids) != len(set(ids)):
                    errors.append(f"Duplicate IDs found in {filename}")
    
    is_valid = len(errors) == 0
    return is_valid, errors


def main():
    parser = argparse.ArgumentParser(description="Validate resume database")
    parser.add_argument("--db-path", required=True, help="Database directory path")
    
    args = parser.parse_args()
    
    try:
        is_valid, errors = validate_database(args.db_path)
        
        if is_valid:
            print("✓ Database is valid")
            return 0
        else:
            print("✗ Database validation failed:\n")
            for error in errors:
                print(f"  - {error}")
            return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit(main())
