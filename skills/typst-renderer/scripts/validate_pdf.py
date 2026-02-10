#!/usr/bin/env python3
"""
PDF Validation Script for Rescume v2.0

Validates output PDFs: checks page count, readability, and metadata.

Usage:
    validate_pdf.py <pdf_file>
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber not installed. Run: pip install pdfplumber", file=sys.stderr)
    sys.exit(1)


def validate_pdf(pdf_path: Path) -> Dict[str, Any]:
    """
    Validate a PDF file.

    Returns:
        Dictionary with validation results
    """
    result = {
        "valid": False,
        "pages": 0,
        "readable": False,
        "file_size_kb": 0.0,
        "errors": []
    }

    # Check file exists
    if not pdf_path.exists():
        result["errors"].append(f"File not found: {pdf_path}")
        return result

    # Check file size
    try:
        file_size_bytes = pdf_path.stat().st_size
        result["file_size_kb"] = round(file_size_bytes / 1024, 2)

        if file_size_bytes == 0:
            result["errors"].append("File is empty (0 bytes)")
            return result

        if file_size_bytes > 10 * 1024 * 1024:  # 10 MB
            result["errors"].append(f"File is unusually large: {result['file_size_kb']} KB")

    except Exception as e:
        result["errors"].append(f"Could not read file size: {e}")
        return result

    # Try to open and read PDF
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Get page count
            result["pages"] = len(pdf.pages)

            if result["pages"] == 0:
                result["errors"].append("PDF has no pages")
                return result

            # Try to extract text from first page as readability check
            try:
                first_page = pdf.pages[0]
                text = first_page.extract_text()

                if text and len(text.strip()) > 0:
                    result["readable"] = True
                else:
                    result["errors"].append("Could not extract text from PDF")

            except Exception as e:
                result["errors"].append(f"Error reading PDF content: {e}")

    except Exception as e:
        result["errors"].append(f"Could not open PDF: {e}")
        return result

    # Overall validity
    result["valid"] = (
        result["pages"] > 0 and
        result["readable"] and
        len(result["errors"]) == 0
    )

    return result


def main():
    """CLI entry point."""
    if len(sys.argv) != 2:
        print("Usage: validate_pdf.py <pdf_file>")
        print("\nValidates a PDF file and reports:")
        print("  - Page count")
        print("  - Readability (can extract text)")
        print("  - File size")
        print("  - Any errors or warnings")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])

    # Validate
    result = validate_pdf(pdf_path)

    # Output result as JSON
    print(json.dumps(result, indent=2))

    # Summary
    if result["valid"]:
        print(f"\n✓ PDF is valid", file=sys.stderr)
        print(f"  Pages: {result['pages']}", file=sys.stderr)
        print(f"  Size: {result['file_size_kb']} KB", file=sys.stderr)
        sys.exit(0)
    else:
        print(f"\n✗ PDF validation failed", file=sys.stderr)
        for error in result["errors"]:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
