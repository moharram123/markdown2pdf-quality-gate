import os
from pathlib import Path
import pdfplumber
import pytest

from tests.framework.converter_runner import run_markdown2pdf

BASE_DIR = Path(__file__).resolve().parent.parent

PILOT_DIR = BASE_DIR / "data" / "pilot-dataset"
REGRESSION_DIR = BASE_DIR / "data" / "regressions"
OUTPUT_DIR = BASE_DIR / "results" / "generated-pdfs"

M2P_COMMAND = os.getenv("M2P_COMMAND")


def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def convert(md_file, pdf_file):
    result = run_markdown2pdf(md_file, pdf_file)
    assert result.returncode == 0
    assert pdf_file.exists()
    assert pdf_file.stat().st_size > 0


@pytest.mark.skipif(not M2P_COMMAND, reason="M2P_COMMAND not set")
def test_conversion_control_full():
    input_md = PILOT_DIR / "control_full.md"
    output_pdf = OUTPUT_DIR / "control_full.pdf"

    convert(input_md, output_pdf)


@pytest.mark.skipif(not M2P_COMMAND, reason="M2P_COMMAND not set")
def test_heading_preserved():
    input_md = PILOT_DIR / "control_structure.md"
    output_pdf = OUTPUT_DIR / "control_structure.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "Structure Test" in text
    assert "First Section" in text
    assert "Second Section" in text


@pytest.mark.skipif(not M2P_COMMAND, reason="M2P_COMMAND not set")
def test_table_preserved():
    input_md = PILOT_DIR / "control_full.md"
    output_pdf = OUTPUT_DIR / "table_test.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "Name" in text
    assert "Alice" in text
    assert "Tester" in text


@pytest.mark.skipif(not M2P_COMMAND, reason="M2P_COMMAND not set")
def test_list_preserved():
    input_md = PILOT_DIR / "control_full.md"
    output_pdf = OUTPUT_DIR / "list_test.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "Item one" in text
    assert "Item two" in text


@pytest.mark.skipif(not M2P_COMMAND, reason="M2P_COMMAND not set")
def test_codeblock_preserved():
    input_md = PILOT_DIR / "control_full.md"
    output_pdf = OUTPUT_DIR / "codeblock_test.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "Hello PDF" in text


@pytest.mark.skipif(not M2P_COMMAND, reason="M2P_COMMAND not set")
def test_missing_heading_detected():
    input_md = REGRESSION_DIR / "reg_missing_heading.md"
    output_pdf = OUTPUT_DIR / "missing_heading.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "First Section" not in text


@pytest.mark.skipif(not M2P_COMMAND, reason="M2P_COMMAND not set")
def test_broken_table_detected():
    input_md = REGRESSION_DIR / "reg_broken_table.md"
    output_pdf = OUTPUT_DIR / "broken_table.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "|" not in text


@pytest.mark.skipif(not M2P_COMMAND, reason="M2P_COMMAND not set")
def test_missing_list_detected():
    input_md = REGRESSION_DIR / "reg_missing_list.md"
    output_pdf = OUTPUT_DIR / "missing_list.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "Item one" not in text


@pytest.mark.skipif(not M2P_COMMAND, reason="M2P_COMMAND not set")
def test_missing_codeblock_detected():
    input_md = REGRESSION_DIR / "reg_missing_codeblock.md"
    output_pdf = OUTPUT_DIR / "missing_codeblock.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "Hello PDF" in text  # content موجود ولكن format تبدل