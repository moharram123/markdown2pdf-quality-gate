import pytest

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PILOT_DIR = BASE_DIR / "data" / "pilot-dataset"
REGRESSION_DIR = BASE_DIR / "data" / "regressions"
OUTPUT_DIR = BASE_DIR / "results" / "generated-pdfs"


# ===== Core Conversion Tests =====

def test_conversion_control_full(convert, extract_text):
    """Verify control_full.md converts to PDF without errors."""
    input_md = PILOT_DIR / "control_full.md"
    output_pdf = OUTPUT_DIR / "control_full.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    # Verify basic content is present
    assert "Sample Document" in text


def test_heading_preserved(convert, extract_text):
    """Verify headings are preserved during conversion."""
    input_md = PILOT_DIR / "control_full.md"
    output_pdf = OUTPUT_DIR / "control_full_heading.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "Sample Document" in text
    assert "Introduction" in text
    assert "Features" in text


def test_table_preserved(control_full_pdf, extract_text):
    """Verify table content is preserved in PDF."""
    text = extract_text(control_full_pdf)

    assert "Name" in text
    assert "Alice" in text
    assert "Tester" in text


def test_list_preserved(control_full_pdf, extract_text):
    """Verify list items are preserved in PDF."""
    text = extract_text(control_full_pdf)

    assert "Item one" in text
    assert "Item two" in text
    assert "Item three" in text


def test_codeblock_preserved(control_full_pdf, extract_text):
    """Verify code block content is preserved in PDF."""
    text = extract_text(control_full_pdf)

    assert "Hello PDF" in text


# ===== Regression Detection Tests =====

def test_missing_heading_detected(convert, extract_text, regression_dir, output_dir):
    """Verify missing heading is detected in regression."""
    input_md = regression_dir / "reg_missing_heading.md"
    output_pdf = output_dir / "missing_heading.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "Introduction" not in text


def test_broken_table_detected(convert, extract_text, regression_dir, output_dir):
    """Verify broken table is detected in regression."""
    input_md = regression_dir / "reg_broken_table.md"
    output_pdf = output_dir / "broken_table.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "Bob" not in text
    assert "Alice" in text


def test_missing_list_detected(convert, extract_text, regression_dir, output_dir):
    """Verify missing list is detected in regression."""
    input_md = regression_dir / "reg_missing_list.md"
    output_pdf = output_dir / "missing_list.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "Item one" not in text
    assert "Item two" not in text
    assert "Item three" not in text


def test_missing_codeblock_detected(convert, extract_text, regression_dir, output_dir):
    input_md = regression_dir / "reg_missing_codeblock.md"
    output_pdf = output_dir / "missing_codeblock.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "Code Example" in text
    assert "Hello PDF" not in text