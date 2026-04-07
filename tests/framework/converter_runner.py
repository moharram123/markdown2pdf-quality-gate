from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ConverterConfig:
    """
    Uses environment variables:

    - M2P_COMMAND (required):
        Example: md2pdf
        Example: dotnet;C:\\path\\Markdown2Pdf.Console.dll  (not needed if md2pdf works)

    - M2P_ARGS_TEMPLATE (optional, ';' separated tokens):
        Default: "{input}"
    """
    command: list[str]
    args_template: list[str]

    @staticmethod
    def from_env() -> "ConverterConfig":
        raw_cmd = os.environ.get("M2P_COMMAND", "").strip()
        if not raw_cmd:
            raise RuntimeError(
                "Missing env var M2P_COMMAND. Example: set M2P_COMMAND=md2pdf"
            )

        # ';' separator so Windows paths like C:\... don't break
        command = [p.strip() for p in raw_cmd.split(";") if p.strip()]

        raw_tpl = os.environ.get("M2P_ARGS_TEMPLATE", "").strip()
        if raw_tpl:
            args_template = [p.strip() for p in raw_tpl.split(";") if p.strip()]
        else:
            # robust default for md2pdf variants: only pass input path
            args_template = ["{input}"]

        return ConverterConfig(command=command, args_template=args_template)


class ConverterRunner:
    @staticmethod
    def convert_markdown_to_pdf(
        input_md: str | Path,
        output_pdf: str | Path,
        config: ConverterConfig | None = None,
        timeout_seconds: int = 180,
    ) -> None:
        config = config or ConverterConfig.from_env()

        in_path = Path(input_md).resolve()
        out_path = Path(output_pdf).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if not in_path.exists():
            raise FileNotFoundError(f"Markdown input not found: {in_path}")

        args = [a.format(input=str(in_path), output=str(out_path)) for a in config.args_template]
        cmd = config.command + args

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            cwd=str(out_path.parent),
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Markdown2Pdf conversion failed.\n"
                f"Command: {cmd}\n"
                f"exit_code: {result.returncode}\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}\n"
            )

        candidate_outputs = [
            out_path.parent / f"{in_path.stem}.pdf",
            in_path.with_suffix(".pdf"),
        ]
        for default_pdf in candidate_outputs:
            if default_pdf.exists() and default_pdf != out_path:
                default_pdf.replace(out_path)
                break

        if not out_path.exists():
            raise RuntimeError(f"Output PDF not found: {out_path}")