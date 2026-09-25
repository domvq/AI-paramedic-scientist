def research_disclaimer() -> str:

    return (
        "This system is a research and educational tool. "
        "Its outputs are not a substitute for clinical judgment, "
        "medical direction, local EMS protocols, or validated "
        "clinical decision-support systems."
    )


def validate_research_output(text: str) -> list:

    warnings = []

    dangerous_patterns = [
        "definitively diagnose",
        "guaranteed treatment",
        "ignore protocol",
        "replace medical direction",
    ]

    lower_text = text.lower()

    for pattern in dangerous_patterns:

        if pattern in lower_text:
            warnings.append(
                f"Potentially unsafe claim detected: {pattern}"
            )

    return warnings