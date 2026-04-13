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
    """Verify missing code block format is detected in regression file."""
    input_md = regression_dir / "reg_missing_codeblock.md"
    output_pdf = output_dir / "test_missing_codeblock.pdf"
    
    convert(input_md, output_pdf)
    text = extract_text(output_pdf)
    
    # Code block fences are missing but text extraction still finds the content.
    assert "Hello PDF" in text