"""
Tests for table preservation in PDF conversion.

This module tests that table content from Markdown source documents
is properly preserved in the generated PDF output.
"""


def test_table_content_present_pilot(control_full_pdf, extract_text):
    """Verify table content appears in PDF."""
    text = extract_text(control_full_pdf)

    # Check for table header and data
    assert "Name" in text
    assert "Role" in text
    assert "Alice" in text
    assert "Tester" in text
    assert "Bob" in text
    assert "DevOps" in text


def test_table_broken_detected(convert, extract_text, regression_dir, output_dir):
    """Verify broken table format is detected in regression file."""
    input_md = regression_dir / "reg_broken_table.md"
    output_pdf = output_dir / "test_broken_table.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    # The regression file has a malformed table (missing Bob row)
    assert "Alice" in text  # First row still present
    assert "Bob" not in text  # Second row missing
    assert "Tester" in text
    assert "DevOps" not in text  # Since Bob is missing