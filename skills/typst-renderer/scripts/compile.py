#!/usr/bin/env python3
"""
Typst Resume Compiler
Orchestrates the compilation of JSON resume data into PDF using Typst templates.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional

# Import sibling modules
try:
    from json_to_typst import json_to_typst
    from validate_pdf import validate_pdf
except ImportError:
    # If running as script, add parent dir to path
    sys.path.insert(0, str(Path(__file__).parent))
    from json_to_typst import json_to_typst
    from validate_pdf import validate_pdf


def find_typst_binary() -> Optional[str]:
    """Find Typst CLI binary in system PATH."""
    import shutil
    typst_path = shutil.which("typst")
    if not typst_path:
        # Check common installation locations
        common_paths = [
            "/opt/homebrew/bin/typst",  # macOS Homebrew (Apple Silicon)
            "/usr/local/bin/typst",      # macOS Homebrew (Intel) / Linux
            Path.home() / ".local" / "bin" / "typst",  # Linux user install
        ]
        for path in common_paths:
            if Path(path).exists():
                return str(path)
    return typst_path


def compile_resume(
    content_json_path: Path,
    template_name: str,
    output_pdf_path: Path,
    plugin_root: Optional[Path] = None,
    typst_binary: Optional[str] = None,
    min_font_size: float = 9.0
) -> Dict[str, Any]:
    """
    Compile resume JSON to PDF using specified Typst template.

    Args:
        content_json_path: Path to JSON file with resume data
        template_name: Name of template in templates/ directory
        output_pdf_path: Path for output PDF
        plugin_root: Root directory of rescume plugin (auto-detected if None)
        typst_binary: Path to typst binary (auto-detected if None)
        min_font_size: Minimum acceptable font size after auto-fit

    Returns:
        Dictionary with compilation result:
        {
            "success": bool,
            "output": str (path to PDF),
            "pages": int,
            "errors": list,
            "warnings": list,
            "font_size": float (estimated)
        }
    """
    result = {
        "success": False,
        "output": None,
        "pages": 0,
        "errors": [],
        "warnings": [],
        "font_size": None
    }

    # Find plugin root
    if plugin_root is None:
        plugin_root = Path(__file__).parent.parent.parent.parent
    plugin_root = Path(plugin_root)

    # Find Typst binary
    if typst_binary is None:
        typst_binary = find_typst_binary()
        if not typst_binary:
            result["errors"].append(
                "Typst CLI not found. Install with: brew install typst (macOS) "
                "or visit https://github.com/typst/typst"
            )
            return result

    # Validate inputs
    if not content_json_path.exists():
        result["errors"].append(f"Content JSON not found: {content_json_path}")
        return result

    templates_dir = plugin_root / "templates"
    template_dir = templates_dir / template_name

    if not template_dir.exists():
        result["errors"].append(f"Template not found: {template_name}")
        result["errors"].append(f"Available templates: {', '.join([d.name for d in templates_dir.iterdir() if d.is_dir()])}")
        return result

    template_file = template_dir / "template.typ"
    if not template_file.exists():
        result["errors"].append(f"Template file not found: {template_file}")
        return result

    # Load JSON content
    try:
        with open(content_json_path, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
    except json.JSONDecodeError as e:
        result["errors"].append(f"Invalid JSON: {e}")
        return result
    except Exception as e:
        result["errors"].append(f"Failed to load JSON: {e}")
        return result

    # Convert JSON to Typst data file (create in plugin root for easier access)
    try:
        typst_data = json_to_typst(content_data)
        data_file = plugin_root / "data.typ"
        with open(data_file, 'w', encoding='utf-8') as f:
            f.write(typst_data)
    except Exception as e:
        result["errors"].append(f"Failed to convert JSON to Typst: {e}")
        return result

    # Create main.typ in plugin root that imports template and data
    main_typ = plugin_root / "main.typ"
    # Use relative paths from plugin root
    template_rel = template_file.relative_to(plugin_root)
    main_content = f"""// Auto-generated main file
#import "{template_rel}": *
#import "data.typ": resume-data

// Render resume with auto-fit
#auto-fit-resume(resume-data, min-font-size: {min_font_size}pt)
"""
    try:
        with open(main_typ, 'w', encoding='utf-8') as f:
            f.write(main_content)
    except Exception as e:
        result["errors"].append(f"Failed to create main.typ: {e}")
        return result

    # Compile with Typst (run from plugin root)
    try:
        compile_result = subprocess.run(
            [typst_binary, "compile", "main.typ", str(output_pdf_path.absolute())],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=plugin_root
        )

        if compile_result.returncode != 0:
            result["errors"].append(f"Typst compilation failed:\n{compile_result.stderr}")
            return result

    except subprocess.TimeoutExpired:
        result["errors"].append("Typst compilation timed out (30s limit)")
        return result
    except Exception as e:
        result["errors"].append(f"Failed to run Typst: {e}")
        return result
    finally:
        # Clean up temp files
        try:
            if data_file.exists():
                data_file.unlink()
            if main_typ.exists():
                main_typ.unlink()
        except:
            pass  # Ignore cleanup errors

    # Validate output PDF
    try:
        pdf_result = validate_pdf(output_pdf_path, max_pages=1)
        result["pages"] = pdf_result["pages"]
        result["warnings"].extend(pdf_result["warnings"])

        if not pdf_result["valid"]:
            result["errors"].extend(pdf_result["errors"])
            # If only error is page count, this is a soft error
            if len(pdf_result["errors"]) == 1 and "pages" in pdf_result["errors"][0].lower():
                result["warnings"].append(
                    "Resume content overflows 1 page. Consider trimming content or "
                    "reducing font size further."
                )
            else:
                return result

    except Exception as e:
        result["warnings"].append(f"PDF validation skipped: {e}")

    # Success!
    result["success"] = True
    result["output"] = str(output_pdf_path)

    return result


def main():
    """CLI entry point."""
    if len(sys.argv) < 4:
        print("Usage: python compile.py <content.json> <template_name> <output.pdf> [min_font_size]", file=sys.stderr)
        print("\nExample:", file=sys.stderr)
        print("  python compile.py resume.json simple-technical-resume output.pdf", file=sys.stderr)
        print("  python compile.py resume.json simple-technical-resume output.pdf 9.0", file=sys.stderr)
        sys.exit(1)

    content_json = Path(sys.argv[1])
    template_name = sys.argv[2]
    output_pdf = Path(sys.argv[3])
    min_font_size = float(sys.argv[4]) if len(sys.argv) > 4 else 9.0

    # Compile
    result = compile_resume(content_json, template_name, output_pdf, min_font_size=min_font_size)

    # Print results
    if result["success"]:
        print(f"✓ Resume compiled successfully")
        print(f"  Output: {result['output']}")
        print(f"  Pages: {result['pages']}")
        if result["warnings"]:
            print("\n⚠ Warnings:")
            for warning in result["warnings"]:
                print(f"  - {warning}")
        sys.exit(0)
    else:
        print(f"✗ Compilation failed")
        if result["errors"]:
            print("\nErrors:")
            for error in result["errors"]:
                print(f"  - {error}")
        if result["warnings"]:
            print("\nWarnings:")
            for warning in result["warnings"]:
                print(f"  - {warning}")
        sys.exit(1)


if __name__ == "__main__":
    main()
