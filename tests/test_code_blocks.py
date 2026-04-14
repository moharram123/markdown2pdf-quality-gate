"""
Tests for code block preservation in PDF conversion.

This module tests that code blocks from Markdown source documents
are properly preserved in the generated PDF output.
"""


def test_code_block_present_pilot(control_full_pdf, extract_text):
    """Verify code block content appears in PDF."""
    text = extract_text(control_full_pdf)
    assert "Hello PDF" in text
    assert "print" in text


def test_code_block_missing_regression(convert, extract_text, regression_dir, output_dir):
    input_md = regression_dir / "reg_missing_codeblock.md"
    output_pdf = output_dir / "missing_codeblock_regression.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "Code Example" in text
    assert "Hello PDF" not in text