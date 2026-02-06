#!/usr/bin/env python3
"""Save data to resume database."""

import argparse
import json
import sys
from pathlib import Path


def save_database(db_path: str, data: dict, file: str = None) -> None:
    """Save database or specific file."""
    db_path = Path(db_path)
    db_path.mkdir(parents=True, exist_ok=True)
    
    if file:
        # Save specific file
        filepath = db_path / f"{file}.json"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved: {filepath}")
    else:
        # Save all files (data should be dict with file names as keys)
        for filename, content in data.items():
            filepath = db_path / f"{filename}.json"
            with open(filepath, 'w') as f:
                json.dump(content, f, indent=2)
            print(f"Saved: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Save resume database")
    parser.add_argument("--db-path", required=True, help="Database directory path")
    parser.add_argument("--file", help="Specific file to save (experiences, skills, etc.)")
    parser.add_argument("--data", required=True, help="JSON data to save")
    
    args = parser.parse_args()
    
    try:
        data = json.loads(args.data)
        save_database(args.db_path, data, args.file)
        return 0
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit(main())
