#!/usr/bin/env python3
"""
JSON to Typst Data Converter
Converts structured resume JSON into Typst variable declarations.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def escape_typst_string(s: str) -> str:
    """Escape special characters for Typst strings."""
    if s is None:
        return '""'
    # Escape backslashes first, then quotes
    s = str(s).replace('\\', '\\\\').replace('"', '\\"')
    # Handle newlines
    s = s.replace('\n', '\\n')
    return f'"{s}"'


def convert_list(items: List[Any]) -> str:
    """Convert Python list to Typst array."""
    if not items:
        return "()"

    converted_items = []
    for item in items:
        if isinstance(item, str):
            converted_items.append(escape_typst_string(item))
        elif isinstance(item, dict):
            converted_items.append(convert_dict(item))
        elif isinstance(item, list):
            converted_items.append(convert_list(item))
        elif isinstance(item, (int, float)):
            converted_items.append(str(item))
        elif isinstance(item, bool):
            converted_items.append("true" if item else "false")
        elif item is None:
            converted_items.append("none")
        else:
            converted_items.append(escape_typst_string(str(item)))

    # Single-item arrays need trailing comma in Typst
    if len(converted_items) == 1:
        return f"({converted_items[0]},)"
    return f"({', '.join(converted_items)})"


def convert_dict(data: Dict[str, Any], indent: int = 2) -> str:
    """Convert Python dict to Typst dictionary."""
    if not data:
        return "(:)"

    indent_str = " " * indent
    items = []

    for key, value in data.items():
        # Convert key (replace underscores with hyphens for Typst convention)
        typst_key = key.replace('_', '-')

        # Convert value
        if isinstance(value, str):
            typst_value = escape_typst_string(value)
        elif isinstance(value, dict):
            typst_value = convert_dict(value, indent + 2)
        elif isinstance(value, list):
            typst_value = convert_list(value)
        elif isinstance(value, (int, float)):
            typst_value = str(value)
        elif isinstance(value, bool):
            typst_value = "true" if value else "false"
        elif value is None:
            typst_value = "none"
        else:
            typst_value = escape_typst_string(str(value))

        items.append(f"{indent_str}{typst_key}: {typst_value}")

    return "(\n" + ",\n".join(items) + f"\n{' ' * (indent - 2)})"


def json_to_typst(json_data: Dict[str, Any]) -> str:
    """
    Convert JSON resume data to Typst variable declaration.

    Args:
        json_data: Dictionary containing resume data

    Returns:
        Typst code as string with data declarations
    """
    typst_code = [
        "// Auto-generated resume data from JSON",
        "// Do not edit manually - regenerate with json_to_typst.py",
        "",
    ]

    # Convert the entire data structure
    typst_dict = convert_dict(json_data, indent=2)
    typst_code.append(f"#let resume-data = {typst_dict}")

    return "\n".join(typst_code)


def main():
    """CLI entry point."""
    if len(sys.argv) != 3:
        print("Usage: python json_to_typst.py <input.json> <output.typ>", file=sys.stderr)
        print("\nExample:", file=sys.stderr)
        print("  python json_to_typst.py resume.json data.typ", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    # Validate input file exists
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Load JSON
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {input_path}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading {input_path}: {e}", file=sys.stderr)
        sys.exit(1)

    # Convert to Typst
    try:
        typst_code = json_to_typst(data)
    except Exception as e:
        print(f"Error converting JSON to Typst: {e}", file=sys.stderr)
        sys.exit(1)

    # Write output
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(typst_code)
        print(f"✓ Generated Typst data file: {output_path}")
    except Exception as e:
        print(f"Error writing {output_path}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
