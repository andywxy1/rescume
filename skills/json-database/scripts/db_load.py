#!/usr/bin/env python3
"""Load data from resume database."""

import argparse
import json
import sys
from pathlib import Path


def load_database(db_path: str, file: str = None) -> dict:
    """Load database or specific file."""
    db_path = Path(db_path)
    
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")
    
    if file:
        # Load specific file
        filepath = db_path / f"{file}.json"
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(filepath, 'r') as f:
            return json.load(f)
    else:
        # Load all files
        files = ["experiences", "skills", "projects", "education", "metadata"]
        data = {}
        
        for filename in files:
            filepath = db_path / f"{filename}.json"
            if filepath.exists():
                with open(filepath, 'r') as f:
                    data[filename] = json.load(f)
        
        return data


def main():
    parser = argparse.ArgumentParser(description="Load resume database")
    parser.add_argument("--db-path", required=True, help="Database directory path")
    parser.add_argument("--file", help="Specific file to load (experiences, skills, etc.)")
    
    args = parser.parse_args()
    
    try:
        data = load_database(args.db_path, args.file)
        print(json.dumps(data, indent=2))
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit(main())
