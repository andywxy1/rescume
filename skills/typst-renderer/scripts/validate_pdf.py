#!/usr/bin/env python3
"""
PDF Validation Script
Checks PDF page count and other properties for resume validation.
"""

import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber not installed. Run: pip install pdfplumber", file=sys.stderr)
    sys.exit(1)


def validate_pdf(pdf_path: Path, max_pages: int = 1) -> dict:
    """
    Validate a PDF file for resume requirements.

    Args:
        pdf_path: Path to PDF file
        max_pages: Maximum allowed pages (default: 1)

    Returns:
        Dictionary with validation results:
        {
            "valid": bool,
            "pages": int,
            "errors": list of str,
            "warnings": list of str
        }
    """
    result = {
        "valid": True,
        "pages": 0,
        "errors": [],
        "warnings": []
    }

    # Check file exists
    if not pdf_path.exists():
        result["valid"] = False
        result["errors"].append(f"PDF file not found: {pdf_path}")
        return result

    # Check file is not empty
    if pdf_path.stat().st_size == 0:
        result["valid"] = False
        result["errors"].append("PDF file is empty")
        return result

    try:
        # Open PDF and check page count
        with pdfplumber.open(pdf_path) as pdf:
            page_count = len(pdf.pages)
            result["pages"] = page_count

            # Validate page count
            if page_count == 0:
                result["valid"] = False
                result["errors"].append("PDF has no pages")
            elif page_count > max_pages:
                result["valid"] = False
                result["errors"].append(
                    f"PDF has {page_count} pages (maximum: {max_pages}). "
                    "Content needs to be trimmed or font size reduced."
                )

            # Check if pages have content
            for i, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if not text or len(text.strip()) < 10:
                    result["warnings"].append(f"Page {i} appears to be empty or has very little content")

            # Additional validations
            if page_count == 1:
                # Check approximate content density
                first_page = pdf.pages[0]
                text = first_page.extract_text() or ""
                word_count = len(text.split())

                if word_count < 100:
                    result["warnings"].append(
                        f"Resume seems very short ({word_count} words). "
                        "Consider adding more detail."
                    )
                elif word_count > 600:
                    result["warnings"].append(
                        f"Resume is very dense ({word_count} words). "
                        "Ensure readability with adequate spacing and font size."
                    )

    except Exception as e:
        result["valid"] = False
        result["errors"].append(f"Failed to read PDF: {str(e)}")

    return result


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python validate_pdf.py <resume.pdf> [max_pages]", file=sys.stderr)
        print("\nExample:", file=sys.stderr)
        print("  python validate_pdf.py resume.pdf      # Validates 1-page max", file=sys.stderr)
        print("  python validate_pdf.py resume.pdf 2    # Validates 2-page max", file=sys.stderr)
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    # Validate PDF
    result = validate_pdf(pdf_path, max_pages)

    # Print results
    if result["valid"]:
        print(f"✓ PDF validation passed")
        print(f"  Pages: {result['pages']}/{max_pages}")
        if result["warnings"]:
            print("\n⚠ Warnings:")
            for warning in result["warnings"]:
                print(f"  - {warning}")
        sys.exit(0)
    else:
        print(f"✗ PDF validation failed")
        print(f"  Pages: {result['pages']}/{max_pages}")
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
