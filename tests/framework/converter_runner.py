import os
import shutil
import subprocess
from pathlib import Path


def run_markdown2pdf(input_file: Path, output_file: Path) -> subprocess.CompletedProcess:
    command = os.getenv("M2P_COMMAND", "md2pdf")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    default_pdf = input_file.with_suffix(".pdf")

    if default_pdf.exists():
        default_pdf.unlink()

    result = subprocess.run(
        [command, str(input_file)],
        capture_output=True,
        text=True,
        shell=False,
    )

    if result.returncode == 0 and default_pdf.exists():
        shutil.move(str(default_pdf), str(output_file))

    return result