"""
Shared pytest configuration and fixtures for all tests.
This file centralizes common functions and fixtures to avoid duplication.
"""
import os
from pathlib import Path
import pdfplumber
import pytest
import shutil

from tests.framework.converter_runner import run_markdown2pdf


# ===== Paths (accessible to all test files) =====
BASE_DIR = Path(__file__).resolve().parent.parent
PILOT_DIR = BASE_DIR / "data" / "pilot-dataset"
REGRESSION_DIR = BASE_DIR / "data" / "regressions"
OUTPUT_DIR = BASE_DIR / "results" / "generated-pdfs"

# Tool availability check
_cmd = os.getenv("M2P_COMMAND", "md2pdf")
M2P_AVAILABLE = shutil.which(_cmd) is not None


# ===== Shared Utilities =====

def _extract_text(pdf_path: Path) -> str:
    """Extract all text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def _convert(md_file: Path, pdf_file: Path) -> None:
    """Convert Markdown to PDF and assert success.
    
    Args:
        md_file: Path to source Markdown file
        pdf_file: Path to output PDF file
        
    Raises:
        AssertionError: If conversion fails or output is invalid
    """
    result = run_markdown2pdf(md_file, pdf_file)
    assert result.returncode == 0, f"Conversion failed: {result.stderr}"
    assert pdf_file.exists(), "PDF file was not created"
    assert pdf_file.stat().st_size > 0, "PDF file is empty"


# ===== Pytest Fixtures =====

@pytest.fixture(scope="session")
def control_full_pdf():
    """Session-scoped fixture: convert control_full.md once and reuse."""
    input_md = PILOT_DIR / "control_full.md"
    output_pdf = OUTPUT_DIR / "control_full.pdf"
    _convert(input_md, output_pdf)
    return output_pdf


@pytest.fixture
def extract_text():
    """Fixture that provides the extract_text function."""
    return _extract_text


@pytest.fixture
def convert():
    """Fixture that provides the convert function."""
    return _convert


@pytest.fixture
def output_directory():
    """Ensure output directory exists for each test."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


@pytest.fixture
def regression_dir():
    """Provide REGRESSION_DIR path."""
    return REGRESSION_DIR


@pytest.fixture
def output_dir():
    """Provide OUTPUT_DIR path."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


# ===== Pytest Marks & Auto-use Fixtures =====

@pytest.fixture(autouse=True)
def skip_if_no_converter():
    """Auto-use fixture: skip tests if md2pdf is not available."""
    if not M2P_AVAILABLE:
        pytest.skip(f"{_cmd} not found")
