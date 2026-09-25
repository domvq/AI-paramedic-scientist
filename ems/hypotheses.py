import json


def build_hypothesis_prompt(
    question: str,
    pico: dict,
    evidence: list,
) -> str:

    return f"""
You are an EMS research scientist.

Generate scientifically testable hypotheses for this
research question.

Research question:
{question}

PICO:
{json.dumps(pico, indent=2)}

Available evidence:
{json.dumps(evidence, indent=2)}

Generate 3 hypotheses.

Each hypothesis must contain:

1. hypothesis
2. reasoning
3. supporting_evidence
4. contradicting_evidence
5. experiment
6. expected_result
7. falsification
8. limitations

Return ONLY valid JSON.

Format:

[
    {{
        "hypothesis": "",
        "reasoning": "",
        "supporting_evidence": [],
        "contradicting_evidence": [],
        "experiment": "",
        "expected_result": "",
        "falsification": "",
        "limitations": []
    }}
]

Do not provide patient-specific treatment instructions.
These are research hypotheses.
"""


def parse_hypotheses(response: str) -> list:

    response = response.strip()

    if response.startswith("```"):
        response = response.replace("```json", "")
        response = response.replace("```", "")

    try:
        result = json.loads(response)

    except json.JSONDecodeError:
        return []

    if not isinstance(result, list):
        return [result]

    return result