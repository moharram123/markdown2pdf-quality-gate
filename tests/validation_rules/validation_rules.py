

# Normal Validation Rules


def validate_heading(text):
    """Check if all required headings exist."""
    return (
        "Sample Document" in text and
        "Introduction" in text and
        "Features" in text
    )


def validate_table(text):
    """Check if table content exists."""
    return (
        "Name" in text and
        "Alice" in text and
        "Bob" in text
    )


def validate_list(text):
    """Check if list items exist."""
    return (
        "Item one" in text and
        "Item two" in text and
        "Item three" in text
    )


def validate_code_block(text):
    """Check if code block content exists."""
    return "Hello PDF" in text


#  Regression Detection Rules

def detect_missing_heading(text):
    """Detect missing heading regression."""
    return "Introduction" not in text


def detect_broken_table(text):
    """Detect missing table row."""
    return "Bob" not in text


def detect_missing_list(text):
    """Detect missing list."""
    return (
        "Item one" not in text and
        "Item two" not in text and
        "Item three" not in text
    )


def detect_missing_code_block(text):
    """Detect missing code block."""
    return "Hello PDF" not in text