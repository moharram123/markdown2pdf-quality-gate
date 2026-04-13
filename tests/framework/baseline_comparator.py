
def normalize_text(text):
    lines = [line.strip().lower() for line in text.splitlines() if line.strip()]
    return lines


def find_differences(expected_text, actual_text):
    expected_lines = normalize_text(expected_text)
    actual_lines = set(normalize_text(actual_text))
    missing = []
    for line in expected_lines:
        if line not in actual_lines:
            missing.append(line)

    return missing