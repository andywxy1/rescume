#!/usr/bin/env python3
"""
Template Lister
Lists all available Typst resume templates with their metadata.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any


def list_templates(plugin_root: Path = None) -> List[Dict[str, Any]]:
    """
    List all available Typst templates.

    Args:
        plugin_root: Root directory of rescume plugin (auto-detected if None)

    Returns:
        List of template metadata dictionaries
    """
    if plugin_root is None:
        plugin_root = Path(__file__).parent.parent.parent.parent
    plugin_root = Path(plugin_root)

    templates_dir = plugin_root / "templates"

    if not templates_dir.exists():
        return []

    templates = []

    for template_dir in sorted(templates_dir.iterdir()):
        if not template_dir.is_dir():
            continue

        # Skip hidden directories and README
        if template_dir.name.startswith('.') or template_dir.name == 'README.md':
            continue

        # Check for required files
        metadata_file = template_dir / "metadata.json"
        template_file = template_dir / "template.typ"

        if not template_file.exists():
            continue

        # Load metadata if available
        metadata = {
            "name": template_dir.name,
            "displayName": template_dir.name.replace('-', ' ').title(),
            "description": "No description available",
            "available": True
        }

        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    file_metadata = json.load(f)
                    metadata.update(file_metadata)
            except Exception as e:
                metadata["error"] = f"Failed to load metadata: {e}"

        # Check for preview
        preview_file = template_dir / "example.pdf"
        if preview_file.exists():
            metadata["preview"] = str(preview_file)
        else:
            metadata["preview"] = None

        templates.append(metadata)

    return templates


def print_templates(templates: List[Dict[str, Any]], verbose: bool = False):
    """Print templates in a human-readable format."""
    if not templates:
        print("No templates found.")
        return

    print(f"Available Templates ({len(templates)}):\n")

    for i, template in enumerate(templates, 1):
        print(f"{i}. {template['displayName']}")
        print(f"   Name: {template['name']}")

        if verbose:
            print(f"   Description: {template.get('description', 'N/A')}")

            if 'version' in template:
                print(f"   Version: {template['version']}")

            if 'author' in template:
                print(f"   Author: {template['author']}")

            if 'features' in template:
                print(f"   Features:")
                for feature in template['features']:
                    print(f"     - {feature}")

            if 'defaultFontSize' in template:
                print(f"   Default Font: {template['defaultFontSize']}")
                print(f"   Min Font: {template.get('minFontSize', 'N/A')}")

            if 'recommendedFor' in template:
                print(f"   Best for: {template['recommendedFor']}")

            if template.get('preview'):
                print(f"   Preview: {template['preview']}")

            if 'error' in template:
                print(f"   ⚠ Warning: {template['error']}")

        else:
            # Compact format
            desc = template.get('description', '')
            if len(desc) > 60:
                desc = desc[:57] + "..."
            print(f"   {desc}")

        print()  # Blank line between templates


def main():
    """CLI entry point."""
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    # List templates
    templates = list_templates()

    if '--json' in sys.argv:
        # JSON output for programmatic use
        print(json.dumps(templates, indent=2))
    else:
        # Human-readable output
        print_templates(templates, verbose=verbose)

    sys.exit(0 if templates else 1)


if __name__ == "__main__":
    main()
