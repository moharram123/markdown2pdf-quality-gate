"""
Tests for heading preservation in PDF conversion.

This module tests that section headings from Markdown source documents
are properly preserved in the generated PDF output.
"""


def test_headings_present_pilot(control_full_pdf, extract_text):
    """Verify all headings appear in PDF."""
    text = extract_text(control_full_pdf)

    # Check for main and section headings
    assert "Sample Document" in text
    assert "Introduction" in text
    assert "Features" in text
    assert "Table Section" in text
    assert "Code Example" in text


def test_heading_missing_detected(convert, extract_text, regression_dir, output_dir):
    """Verify missing heading is detected in regression file."""
    input_md = regression_dir / "reg_missing_heading.md"
    output_pdf = output_dir / "test_missing_heading.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    # The regression file is missing the "Introduction" heading
    assert "Sample Document" in text
    assert "Introduction" not in text
    assert "Features" in text