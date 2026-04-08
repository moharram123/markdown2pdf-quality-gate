from pathlib import Path


def load_baseline(baseline_path: Path) -> str:
    return baseline_path.read_text(encoding="utf-8")


def find_differences(actual: str, expected: str) -> list[str]:
    missing = []
    for line in expected.splitlines():
        line = line.strip()
        if line and line not in actual:
            missing.append(line)
    return missing