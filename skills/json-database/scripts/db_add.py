#!/usr/bin/env python3
"""Add new entry to resume database with auto-generated ID."""

import argparse
import json
import sys
from pathlib import Path


def generate_id(entries: list, prefix: str) -> str:
    """Generate unique ID for new entry."""
    if not entries:
        return f"{prefix}_001"
    
    # Extract existing IDs and find max number
    existing_nums = []
    for entry in entries:
        if 'id' in entry:
            try:
                num = int(entry['id'].split('_')[1])
                existing_nums.append(num)
            except (IndexError, ValueError):
                pass
    
    max_num = max(existing_nums) if existing_nums else 0
    new_num = max_num + 1
    
    return f"{prefix}_{new_num:03d}"


def add_entry(db_path: str, entry_type: str, data: dict) -> str:
    """Add new entry to database."""
    db_path = Path(db_path)
    
    # Map type to file and key
    type_map = {
        "experience": ("experiences.json", "experiences", "exp"),
        "skill": ("skills.json", "skills", "skill"),
        "project": ("projects.json", "projects", "project"),
        "education": ("education.json", "education", "edu")
    }
    
    if entry_type not in type_map:
        raise ValueError(f"Invalid type: {entry_type}. Must be: {', '.join(type_map.keys())}")
    
    filename, key, prefix = type_map[entry_type]
    filepath = db_path / filename
    
    # Load existing data
    if filepath.exists():
        with open(filepath, 'r') as f:
            db_data = json.load(f)
    else:
        db_data = {key: []}
    
    entries = db_data.get(key, [])
    
    # Generate ID and add to data
    new_id = generate_id(entries, prefix)
    data['id'] = new_id
    
    # Add to entries
    entries.append(data)
    db_data[key] = entries
    
    # Save
    with open(filepath, 'w') as f:
        json.dump(db_data, f, indent=2)
    
    return new_id


def main():
    parser = argparse.ArgumentParser(description="Add entry to resume database")
    parser.add_argument("--db-path", required=True, help="Database directory path")
    parser.add_argument("--type", required=True, help="Entry type (experience, skill, project, education)")
    parser.add_argument("--data", required=True, help="JSON data for new entry")
    
    args = parser.parse_args()
    
    try:
        data = json.loads(args.data)
        new_id = add_entry(args.db_path, args.type, data)
        print(f"Added entry with ID: {new_id}")
        return 0
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit(main())
