#!/usr/bin/env python3
"""
Template Manager Script for Rescume v2.0

Lists all available Typst resume templates with their metadata.

Usage:
    list_templates.py [--json]
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any


TEMPLATES_DIR = Path.home() / ".claude" / "skills" / "rescume" / "templates"


def list_templates() -> List[Dict[str, Any]]:
    """
    Scan templates directory and return list of available templates.

    Returns:
        List of template metadata dictionaries
    """
    templates = []

    if not TEMPLATES_DIR.exists():
        return templates

    # Scan for template directories
    for item in TEMPLATES_DIR.iterdir():
        if not item.is_dir():
            continue

        if item.name.startswith('.'):
            continue

        # Check for required files
        template_typ = item / "template.typ"
        metadata_json = item / "metadata.json"

        if not template_typ.exists():
            continue  # Not a valid template

        # Load metadata if available
        metadata = {
            "name": item.name,
            "description": "No description available",
            "template_file": str(template_typ),
            "preview": None,
            "default_font": "Unknown",
            "default_font_size": "11pt",
            "min_font_size": "9pt"
        }

        if metadata_json.exists():
            try:
                with open(metadata_json, 'r', encoding='utf-8') as f:
                    loaded_metadata = json.load(f)
                    metadata.update(loaded_metadata)

            except Exception as e:
                metadata["metadata_error"] = str(e)

        # Check for preview
        preview_pdf = item / "preview.pdf"
        if preview_pdf.exists():
            metadata["preview"] = str(preview_pdf)

        templates.append(metadata)

    # Sort by name
    templates.sort(key=lambda t: t["name"])

    return templates


def format_template_info(template: Dict[str, Any]) -> str:
    """Format template info as human-readable text."""
    lines = []
    lines.append(f"• {template['name']}")
    lines.append(f"  Description: {template['description']}")
    lines.append(f"  Font: {template['default_font']} ({template['default_font_size']})")

    if template.get("color_theme"):
        lines.append(f"  Theme: {template['color_theme']}")

    if template.get("preview"):
        lines.append(f"  Preview: {template['preview']}")

    if template.get("metadata_error"):
        lines.append(f"  ⚠️  Warning: {template['metadata_error']}")

    return "\n".join(lines)


def main():
    """CLI entry point."""
    json_output = "--json" in sys.argv

    templates = list_templates()

    if not templates:
        print("No templates found.", file=sys.stderr)
        print(f"Template directory: {TEMPLATES_DIR}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        # JSON output
        print(json.dumps(templates, indent=2))
    else:
        # Human-readable output
        print(f"Available resume templates ({len(templates)}):\n")
        for template in templates:
            print(format_template_info(template))
            print()

        print(f"Template directory: {TEMPLATES_DIR}")
        print("\nUsage:")
        print("  compile.py <content.json> <template-name> <output.pdf>")
        print("\nExample:")
        print(f"  compile.py resume.json {templates[0]['name']} final.pdf")

    sys.exit(0)


if __name__ == "__main__":
    main()
