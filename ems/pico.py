import json


def build_pico_prompt(question: str, patient_context: str) -> str:

    return f"""
You are an EMS research scientist.

Your job is to convert a research question into a
structured PICO framework.

PICO:

P = Population
I = Intervention or Exposure
C = Comparator
O = Outcome

Research question:
{question}

Patient/EMS context:
{patient_context}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "population": "",
    "intervention_or_exposure": "",
    "comparator": "",
    "outcome": "",
    "research_question": ""
}}

Important:

- Do not diagnose the patient.
- Do not prescribe treatment.
- Do not invent evidence.
- This is a research framework.
"""


def parse_pico_response(response: str) -> dict:

    response = response.strip()

    if response.startswith("```"):
        response = response.replace("```json", "")
        response = response.replace("```", "")

    try:
        result = json.loads(response)

    except json.JSONDecodeError:
        return {
            "population": "",
            "intervention_or_exposure": "",
            "comparator": "",
            "outcome": "",
            "research_question": "",
            "error": "Could not parse PICO response.",
        }

    required = [
        "population",
        "intervention_or_exposure",
        "comparator",
        "outcome",
        "research_question",
    ]

    for field in required:
        result.setdefault(field, "")

    return result