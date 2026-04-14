import os
from pathlib import Path
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "tests" / "experiments" / "test_llm_generated.py"

PROMPT = """
You are a software testing assistant.

Generate pytest integration tests for a project that converts Markdown files to PDF.
The generated tests must validate extracted PDF text for these cases:

1. Heading validation
2. Table validation
3. List validation
4. Code block validation
5. Regression detection for:
   - missing heading
   - broken table
   - missing list
   - missing code block

Assumptions:
- pytest fixtures already exist:
  convert, extract_text, pilot_dir, regression_dir, output_dir
- The project uses pdf text extraction after conversion
- Keep the tests simple and readable
- Return ONLY valid Python code
- No markdown fences
"""

def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is not set.")

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-5.2",
        input=PROMPT,
    )

    generated_code = response.output_text.strip()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(generated_code, encoding="utf-8")

    print(f"LLM-generated test file saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()