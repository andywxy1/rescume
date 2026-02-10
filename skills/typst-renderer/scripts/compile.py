#!/usr/bin/env python3
"""
Typst Resume Compilation Script for Rescume v2.0

Main orchestrator for compiling structured JSON resume content into
single-page PDF using Typst templates with automatic font size adjustment.

Usage:
    compile.py <content.json> <template-name> <output.pdf>
"""

import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Dict, Any, Tuple

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber not installed. Run: pip install pdfplumber", file=sys.stderr)
    sys.exit(1)


# Configuration
TYPST_CLI = Path.home() / ".local" / "bin" / "typst"
TEMPLATES_DIR = Path.home() / ".claude" / "skills" / "rescume" / "templates"
MIN_FONT_SIZE = 9.0
MAX_FONT_SIZE = 11.0
FONT_STEP = 0.5


def get_pdf_page_count(pdf_path: Path) -> int:
    """Get number of pages in PDF."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return len(pdf.pages)
    except Exception as e:
        print(f"Error reading PDF: {e}", file=sys.stderr)
        return -1


def load_json_content(json_path: Path) -> Dict[str, Any]:
    """Load and validate JSON content."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Basic validation
        if not isinstance(data, dict):
            raise ValueError("JSON must be an object/dictionary")

        if "header" not in data:
            raise ValueError("JSON must contain 'header' field")

        return data

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"Error loading JSON: {e}", file=sys.stderr)
        sys.exit(2)


def create_typst_main_file(template_name: str, data_typ_filename: str,
                           template_typ_filename: str, font_size: float) -> str:
    """
    Create main Typst file that imports template and data.
    Assumes template and data files are copied into the same directory.

    Returns the Typst content as a string.
    """
    typst_content = f"""// Main resume file - auto-generated
#import "{template_typ_filename}": resume
#import "{data_typ_filename}": resume_data

// Call template with data and font size
// Note: Typst function calls need exact parameter matching
#resume(
  font-size: {font_size}pt,
  name: resume_data.header.name,
  email: resume_data.header.at("email", default: none),
  phone: resume_data.header.at("phone", default: none),
  location: resume_data.header.at("location", default: none),
  linkedin: resume_data.header.at("linkedin", default: none),
  github: resume_data.header.at("github", default: none),
  website: resume_data.header.at("website", default: none),
  summary: resume_data.at("summary", default: none),
  education: resume_data.at("education", default: ()),
  experience: resume_data.at("experience", default: ()),
  projects: resume_data.at("projects", default: ()),
  skills: resume_data.at("skills", default: none),
)
"""
    return typst_content


def compile_typst(main_typ_path: Path, output_pdf_path: Path) -> Tuple[bool, str]:
    """
    Compile Typst file to PDF.

    Returns: (success: bool, error_message: str)
    """
    try:
        result = subprocess.run(
            [str(TYPST_CLI), "compile", str(main_typ_path), str(output_pdf_path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return False, result.stderr

        return True, ""

    except subprocess.TimeoutExpired:
        return False, "Compilation timed out (>30s)"
    except FileNotFoundError:
        return False, f"Typst CLI not found at {TYPST_CLI}. Is it installed?"
    except Exception as e:
        return False, str(e)


def auto_fit_compile(
    content_json_path: Path,
    template_name: str,
    output_pdf_path: Path
) -> Dict[str, Any]:
    """
    Compile resume with automatic font size adjustment to fit 1 page.

    Returns result dictionary with status and metadata.
    """
    start_time = time.time()

    # Load JSON content
    json_data = load_json_content(content_json_path)

    # Create temporary working directory
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Step 1: Convert JSON to Typst data
        json_to_typst_script = Path(__file__).parent / "json_to_typst.py"
        data_typ_path = tmpdir_path / "data.typ"

        result = subprocess.run(
            [sys.executable, str(json_to_typst_script),
             str(content_json_path), str(data_typ_path)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": "Failed to convert JSON to Typst",
                "details": result.stderr
            }

        # Copy template file to temp directory
        template_source = TEMPLATES_DIR / template_name / "template.typ"
        if not template_source.exists():
            return {
                "success": False,
                "error": f"Template not found: {template_source}"
            }

        import shutil
        template_typ_path = tmpdir_path / "template.typ"
        shutil.copy(template_source, template_typ_path)

        # Step 2: Auto-fit loop
        current_font = MAX_FONT_SIZE
        iterations = 0
        max_iterations = int((MAX_FONT_SIZE - MIN_FONT_SIZE) / FONT_STEP) + 1

        while current_font >= MIN_FONT_SIZE and iterations < max_iterations:
            iterations += 1

            # Create main Typst file with current font size
            main_content = create_typst_main_file(
                template_name, "data.typ", "template.typ", current_font
            )

            main_typ_path = tmpdir_path / "main.typ"
            with open(main_typ_path, 'w', encoding='utf-8') as f:
                f.write(main_content)

            # Compile
            temp_pdf = tmpdir_path / f"output_{current_font}.pdf"
            success, error_msg = compile_typst(main_typ_path, temp_pdf)

            if not success:
                return {
                    "success": False,
                    "error": f"Compilation failed at font size {current_font}pt",
                    "details": error_msg
                }

            # Check page count
            pages = get_pdf_page_count(temp_pdf)

            if pages < 0:
                return {
                    "success": False,
                    "error": "Failed to read output PDF"
                }

            if pages == 1:
                # Success! Copy to final output
                shutil.copy(temp_pdf, output_pdf_path)

                elapsed_ms = int((time.time() - start_time) * 1000)

                return {
                    "success": True,
                    "pages": 1,
                    "font_size_used": current_font,
                    "output_path": str(output_pdf_path),
                    "iterations": iterations,
                    "compilation_time_ms": elapsed_ms
                }

            elif pages > 1:
                # Too much content, try smaller font
                current_font -= FONT_STEP
                current_font = round(current_font, 1)  # Avoid floating point issues
            else:
                # Should not happen (0 pages)
                return {
                    "success": False,
                    "error": f"Unexpected page count: {pages}"
                }

        # If we get here, couldn't fit even at minimum font
        elapsed_ms = int((time.time() - start_time) * 1000)

        # Estimate how much content to remove
        final_pages = get_pdf_page_count(temp_pdf)
        overflow_ratio = (final_pages - 1.0) / 1.0
        bullets_to_remove = max(2, int(overflow_ratio * 10))

        return {
            "success": False,
            "status": "overflow",
            "pages": final_pages,
            "min_font_reached": MIN_FONT_SIZE,
            "iterations": iterations,
            "compilation_time_ms": elapsed_ms,
            "recommendation": f"Content still overflows at minimum font size ({MIN_FONT_SIZE}pt). "
                            f"Please reduce content by approximately {bullets_to_remove}-{bullets_to_remove + 1} bullet points."
        }


def main():
    """CLI entry point."""
    if len(sys.argv) != 4:
        print("Usage: compile.py <content.json> <template-name> <output.pdf>")
        print("\nExample:")
        print("  compile.py resume_content.json basic-resume final_resume.pdf")
        print("\nAvailable templates:")
        print("  - basic-resume")
        print("  - modern-resume")
        sys.exit(1)

    content_json_path = Path(sys.argv[1])
    template_name = sys.argv[2]
    output_pdf_path = Path(sys.argv[3])

    if not content_json_path.exists():
        print(f"Error: Content file not found: {content_json_path}", file=sys.stderr)
        sys.exit(2)

    # Verify template exists
    template_dir = TEMPLATES_DIR / template_name
    if not template_dir.exists():
        print(f"Error: Template not found: {template_name}", file=sys.stderr)
        print(f"Template directory should be at: {template_dir}", file=sys.stderr)
        sys.exit(2)

    print(f"Compiling resume...")
    print(f"  Content: {content_json_path}")
    print(f"  Template: {template_name}")
    print(f"  Output: {output_pdf_path}")
    print()

    # Compile with auto-fit
    result = auto_fit_compile(content_json_path, template_name, output_pdf_path)

    # Output result
    print(json.dumps(result, indent=2))

    if result["success"]:
        print(f"\n✓ Success! Resume compiled to {output_pdf_path}")
        print(f"  Font size: {result['font_size_used']}pt")
        print(f"  Time: {result['compilation_time_ms']}ms")
        sys.exit(0)
    else:
        print(f"\n✗ Compilation failed", file=sys.stderr)
        if "recommendation" in result:
            print(f"  {result['recommendation']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
