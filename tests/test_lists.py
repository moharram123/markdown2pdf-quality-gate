"""
Tests for list preservation in PDF conversion.

This module tests that list items from Markdown source documents
are properly preserved in the generated PDF output.
"""
import pytest


def test_list_items_present_pilot(control_full_pdf, extract_text):
    """Verify all list items appear in PDF."""
    text = extract_text(control_full_pdf)

    assert "Item one" in text
    assert "Item two" in text
    assert "Item three" in text


def test_list_items_missing_regression(convert, extract_text, regression_dir, output_dir):
    """Verify missing list items are detected in regression file."""
    input_md = regression_dir / "reg_missing_list.md"
    output_pdf = output_dir / "test_missing_list.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    # The regression file is missing all list items
    assert "Item one" not in text
    assert "Item two" not in text
    assert "Item three" not in text