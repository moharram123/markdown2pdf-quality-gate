from pathlib import Path
import pytest

from tests.framework.converter_runner import ConverterRunner


@pytest.mark.integration
def test_convert_markdown_to_pdf(tmp_path: Path):
    input_md = Path("data/pilot-dataset/sample.md")
    output_pdf = tmp_path / "sample.pdf"

    ConverterRunner.convert_markdown_to_pdf(input_md, output_pdf)

    assert output_pdf.exists()
    assert output_pdf.stat().st_size > 0
