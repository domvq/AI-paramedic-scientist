def validate_experiment_request(
    question: str,
    hypothesis: str,
) -> tuple[bool, str]:

    if not question.strip():
        return False, "Research question is empty."

    if not hypothesis.strip():
        return False, "Hypothesis is empty."

    return True, ""