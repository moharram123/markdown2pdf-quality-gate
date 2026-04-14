from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
PILOT_DIR = BASE_DIR / "data" / "pilot-dataset"


def test_llm_control_full_converts(convert, extract_text, output_dir):
    input_md = PILOT_DIR / "control_full.md"
    output_pdf = output_dir / "llm_control_full.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "Sample Document" in text


def test_llm_heading_validation(control_full_pdf, extract_text):
    text = extract_text(control_full_pdf)

    assert "Sample Document" in text
    assert "Introduction" in text
    assert "Features" in text


def test_llm_table_validation(control_full_pdf, extract_text):
    text = extract_text(control_full_pdf)

    assert "Name" in text
    assert "Alice" in text
    assert "Tester" in text


def test_llm_list_validation(control_full_pdf, extract_text):
    text = extract_text(control_full_pdf)

    assert "Item one" in text
    assert "Item two" in text
    assert "Item three" in text


def test_llm_code_block_validation(control_full_pdf, extract_text):
    text = extract_text(control_full_pdf)

    assert "Hello PDF" in text


def test_llm_regression_missing_heading(convert, extract_text, regression_dir, output_dir):
    input_md = regression_dir / "reg_missing_heading.md"
    output_pdf = output_dir / "llm_missing_heading.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "Introduction" not in text


def test_llm_regression_broken_table(convert, extract_text, regression_dir, output_dir):
    input_md = regression_dir / "reg_broken_table.md"
    output_pdf = output_dir / "llm_broken_table.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "Bob" not in text
    assert "Alice" in text


def test_llm_regression_missing_list(convert, extract_text, regression_dir, output_dir):
    input_md = regression_dir / "reg_missing_list.md"
    output_pdf = output_dir / "llm_missing_list.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "Item one" not in text
    assert "Item two" not in text
    assert "Item three" not in text


def test_llm_regression_missing_code_block(convert, extract_text, regression_dir, output_dir):
    input_md = regression_dir / "reg_missing_codeblock.md"
    output_pdf = output_dir / "llm_missing_codeblock.pdf"

    convert(input_md, output_pdf)
    text = extract_text(output_pdf)

    assert "Code Example" in text
    assert "Hello PDF" not in text

