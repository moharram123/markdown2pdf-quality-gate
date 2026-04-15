import pytest
from pathlib import Path

# import validation rules
from tests.validation_rules.validation_rules import (
    validate_heading,
    validate_table,
    validate_list,
    validate_code_block,
    detect_missing_heading,
    detect_broken_table,
    detect_missing_list,
    detect_missing_code_block,
)

# paths
BASE_DIR = Path(__file__).resolve().parent.parent
PILOT_DIR = BASE_DIR / "data" / "pilot-dataset"
REGRESSION_DIR = BASE_DIR / "data" / "regressions"
OUTPUT_DIR = BASE_DIR / "results" / "generated-pdfs"

# Normal Validation Tests


def test_heading_validation(convert, extract_text):
    input_md = PILOT_DIR / "control_full.md"
    output_pdf = OUTPUT_DIR / "heading_test.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert validate_heading(text)


def test_table_validation(convert, extract_text):
    input_md = PILOT_DIR / "control_full.md"
    output_pdf = OUTPUT_DIR / "table_test.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert validate_table(text)


def test_list_validation(convert, extract_text):
    input_md = PILOT_DIR / "control_full.md"
    output_pdf = OUTPUT_DIR / "list_test.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert validate_list(text)


def test_codeblock_validation(convert, extract_text):
    input_md = PILOT_DIR / "control_full.md"
    output_pdf = OUTPUT_DIR / "code_test.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert validate_code_block(text)


# Regression Tests

def test_missing_heading_regression(convert, extract_text):
    input_md = REGRESSION_DIR / "reg_missing_heading.md"
    output_pdf = OUTPUT_DIR / "missing_heading.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert detect_missing_heading(text)


def test_broken_table_regression(convert, extract_text):
    input_md = REGRESSION_DIR / "reg_broken_table.md"
    output_pdf = OUTPUT_DIR / "broken_table.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert detect_broken_table(text)


def test_missing_list_regression(convert, extract_text):
    input_md = REGRESSION_DIR / "reg_missing_list.md"
    output_pdf = OUTPUT_DIR / "missing_list.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert detect_missing_list(text)


def test_missing_codeblock_regression(convert, extract_text):
    input_md = REGRESSION_DIR / "reg_missing_codeblock.md"
    output_pdf = OUTPUT_DIR / "missing_codeblock.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert detect_missing_code_block(text)