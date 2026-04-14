import os
import shutil
import subprocess
import time
from pathlib import Path


def run_markdown2pdf(input_file: Path, output_file: Path) -> subprocess.CompletedProcess:
    command = os.getenv("M2P_COMMAND", "md2pdf")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    default_pdf = input_file.with_suffix(".pdf")

    if output_file.exists():
        output_file.unlink()

    if default_pdf.exists():
        default_pdf.unlink()

    result = subprocess.run(
        [command, str(input_file)],
        capture_output=True,
        text=True,
        shell=False,
        timeout=60,
    )

    if result.returncode == 0 and default_pdf.exists():
        for _ in range(10):
            try:
                shutil.move(str(default_pdf), str(output_file))
                break
            except PermissionError:
                time.sleep(0.5)
        else:
            raise PermissionError(
                f"Could not move generated PDF from {default_pdf} to {output_file}"
            )

    return result