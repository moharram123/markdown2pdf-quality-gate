import os
from pathlib import Path
import pytest
import pdfplumber

from tests.framework.converter_runner import run_markdown2pdf
from tests.framework.baseline_comparator import load_baseline, find_differences

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_MD = BASE_DIR / "data" / "pilot-dataset" / "sample.md"
OUTPUT_PDF = BASE_DIR / "results" / "generated-pdfs" / "sample.pdf"

REGRESSION_MD = BASE_DIR / "data" / "regressions" / "sample_missing_heading.md"
REGRESSION_PDF = BASE_DIR / "results" / "generated-pdfs" / "sample_missing_heading.pdf"
BASELINE_FILE = BASE_DIR / "data" / "baselines" / "sample_basic_expected.txt"

M2P_COMMAND = os.getenv("M2P_COMMAND")


def extract_text(pdf_path: Path) -> str:
    parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            parts.append(page.extract_text() or "")
    return "\n".join(parts)


@pytest.mark.skipif(not M2P_COMMAND, reason="M2P_COMMAND is not set")
def test_convert_markdown_to_pdf():
    result = run_markdown2pdf(INPUT_MD, OUTPUT_PDF)

    assert result.returncode == 0
    assert OUTPUT_PDF.exists()
    assert OUTPUT_PDF.stat().st_size > 0


@pytest.mark.skipif(not M2P_COMMAND, reason="M2P_COMMAND is not set")
def test_detect_missing_heading_regression():
    result = run_markdown2pdf(REGRESSION_MD, REGRESSION_PDF)

    assert result.returncode == 0
    assert REGRESSION_PDF.exists()
    assert REGRESSION_PDF.stat().st_size > 0

    actual_text = extract_text(REGRESSION_PDF)
    expected_text = load_baseline(BASELINE_FILE)

    differences = find_differences(actual_text, expected_text)

    assert "Introduction" in differences, (
        f"Regression was not detected correctly. Differences found: {differences}"
    )