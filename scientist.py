
import os
import json
import arxiv
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY is missing. "
        "Add it to Streamlit Cloud Secrets."
    )

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-120b"


# ============================================================
# AI
# ============================================================

def ask_scientist(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a rigorous scientific research assistant. "
                    "Follow the requested output format exactly."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=2000,
        temperature=0.1,
    )

    return response.choices[0].message.content


# ============================================================
# JSON
# ============================================================

def parse_json(result):
    if not result:
        raise ValueError("AI returned an empty response.")

    cleaned = str(result).strip()

    # Remove Markdown fences
    cleaned = cleaned.replace("```json", "")
    cleaned = cleaned.replace("```", "")
    cleaned = cleaned.strip()

    # Try entire response
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Try JSON object
    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start >= 0 and end > start:
        try:
            return json.loads(
                cleaned[start:end + 1]
            )
        except json.JSONDecodeError:
            pass

    # Try JSON array
    start = cleaned.find("[")
    end = cleaned.rfind("]")

    if start >= 0 and end > start:
        try:
            return json.loads(
                cleaned[start:end + 1]
            )
        except json.JSONDecodeError:
            pass

    raise ValueError(
        "AI returned invalid JSON.\n\n"
        f"AI response:\n{cleaned[:5000]}"
    )


# ============================================================
# LITERATURE
# ============================================================

def search_papers(query, max_results=3):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    arxiv_client = arxiv.Client()

    papers = []

    for result in arxiv_client.results(search):
        papers.append(
            {
                "title": result.title,
                "authors": [
                    author.name
                    for author in result.authors[:5]
                ],
                "abstract": result.summary[:1000],
                "url": result.entry_id,
                "published": str(result.published),
            }
        )

    return papers


def format_papers(papers):
    if not papers:
        return "No literature found."

    output = []

    for i, paper in enumerate(papers[:3]):
        output.append(
            f"""
PAPER {i + 1}
Title: {paper.get("title", "")[:300]}
Authors: {", ".join(paper.get("authors", []))}
Abstract: {paper.get("abstract", "")[:1000]}
"""
        )

    return "\n".join(output)


# ============================================================
# HYPOTHESES
# ============================================================

def generate_hypotheses(question, papers=None):
    literature = format_papers(papers or [])

    prompt = f"""
You are an AI scientific research assistant.

Research question:
{question[:2000]}

Relevant literature:
{literature}

Generate exactly 3 testable hypotheses.

Base the hypotheses on the research question and supplied
literature.

Do not invent claims that are presented as established facts.

Return ONLY a valid JSON array.

The JSON must have exactly this structure:

[
  {{
    "hypothesis": "string",
    "reasoning": "string",
    "experiment": "string",
    "expected_result": "string",
    "falsification": "string",
    "novelty": "string"
  }},
  {{
    "hypothesis": "string",
    "reasoning": "string",
    "experiment": "string",
    "expected_result": "string",
    "falsification": "string",
    "novelty": "string"
  }},
  {{
    "hypothesis": "string",
    "reasoning": "string",
    "experiment": "string",
    "expected_result": "string",
    "falsification": "string",
    "novelty": "string"
  }}
]

Return JSON only.
"""

    result = ask_scientist(prompt)

    parsed = parse_json(result)

    if not isinstance(parsed, list):
        raise ValueError(
            "Expected a JSON array of hypotheses."
        )

    return parsed


# ============================================================
# CHOOSE EXPERIMENT
# ============================================================

def choose_experiment(
    question,
    hypotheses,
    previous_results=None,
):
    previous_results = previous_results or []

    prompt = f"""
You are an autonomous scientific researcher.

Question:
{question[:2000]}

Hypotheses:
{json.dumps(hypotheses)[:5000]}

Previous experiments:
{json.dumps(previous_results[-3:])[:5000]}

Choose the most informative next experiment.

Return ONLY valid JSON.

Required structure:

{{
  "selected_hypothesis": "string",
  "reason": "string",
  "experiment_goal": "string",
  "expected_result": "string",
  "success_metric": "string"
}}
"""

    return parse_json(
        ask_scientist(prompt)
    )


# ============================================================
# GENERATE EXPERIMENT
# ============================================================

def generate_experiment(
    question,
    hypothesis,
    experiment_goal,
):
    prompt = f"""
You are an AI scientist.

Question:
{question[:1500]}

Hypothesis:
{hypothesis[:1500]}

Experiment goal:
{experiment_goal[:1500]}

Write a complete Python experiment.

Allowed libraries:

numpy
pandas
scikit-learn
matplotlib

Requirements:

- Use a built-in sklearn dataset.
- Include a baseline.
- Print numerical metrics.
- Use a fixed random seed.
- Finish within 30 seconds.
- Do not access the internet.
- Do not access the filesystem.
- Do not use subprocess.
- Return ONLY Python code.
"""

    return ask_scientist(prompt)


# ============================================================
# ANALYZE RESULTS
# ============================================================

def analyze_results(
    question,
    hypothesis,
    output,
):
    prompt = f"""
You are a scientific reviewer.

Question:
{question[:1500]}

Hypothesis:
{hypothesis[:1500]}

Experiment results:
{output[:4000]}

Analyze:

1. What happened?
2. Important numbers
3. Was the hypothesis supported?
4. Limitations
5. Possible confounders
6. What should be tested next?

Do not claim that one experiment proves a scientific theory.
Only discuss results actually contained in the experiment output.
"""

    return ask_scientist(prompt)


# ============================================================
# SAVE
# ============================================================

def save_experiment(
    question,
    experiment_number,
    hypothesis,
    code,
    output,
    analysis,
):
    os.makedirs(
        "experiments",
        exist_ok=True,
    )

    filename = (
        f"experiments/"
        f"experiment_{experiment_number}.json"
    )

    data = {
        "question": question,
        "experiment_number": experiment_number,
        "hypothesis": hypothesis,
        "code": code,
        "output": output,
        "analysis": analysis,
    }

    with open(
        filename,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
        )

    return filename


# ============================================================
# FINAL REPORT
# ============================================================

def generate_final_report(
    question,
    papers,
    hypotheses,
    history,
):
    prompt = f"""
You are a rigorous scientific reviewer.

Research question:
{question[:2000]}

Literature:
{json.dumps(papers[:3])[:5000]}

Hypotheses:
{json.dumps(hypotheses)[:5000]}

Experiments:
{json.dumps(history)[:10000]}

Write a concise Markdown research report.

Use:

# Abstract
# Research Question
# Literature Context
# Hypotheses
# Methods
# Results
# Discussion
# Limitations
# Conclusion
# Future Experiments

Only report findings contained in the supplied results.

Do not invent numerical results.

Do not claim causation without evidence.

Return ONLY Markdown.
"""

    return ask_scientist(prompt)


# ============================================================
# CLEAN PYTHON
# ============================================================

def clean_python_code(code):
    code = str(code).strip()

    if "```" in code:
        parts = code.split("```")

        if len(parts) >= 2:
            code = parts[1].strip()

            lines = code.splitlines()

            if lines and lines[0].strip().lower() in (
                "python",
                "py",
            ):
                code = "\n".join(
                    lines[1:]
                )

    return code.strip()

