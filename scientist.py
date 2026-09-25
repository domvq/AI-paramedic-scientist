
import os
import json
import arxiv
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY was not found. "
        "Create a .env file containing GROQ_API_KEY=your_key"
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
                    "You are a rigorous AI scientific research assistant. "
                    "Follow the requested output format exactly. "
                    "When JSON is requested, return valid JSON with "
                    "properly escaped quotation marks."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=2000,
        temperature=0.1
    )

    return response.choices[0].message.content



# ============================================================
# JSON PARSER
# ============================================================

def parse_json(result):
    if result is None:
        raise ValueError("AI returned an empty response.")

    cleaned = str(result).strip()

    # Remove Markdown code fences.
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()

        if lines:
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        cleaned = "\n".join(lines).strip()

    # First attempt: entire response.
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Second attempt: find JSON object.
    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start >= 0 and end > start:
        candidate = cleaned[start:end + 1]

        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    # Third attempt: find JSON array.
    start = cleaned.find("[")
    end = cleaned.rfind("]")

    if start >= 0 and end > start:
        candidate = cleaned[start:end + 1]

        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    # Give useful debugging information instead of the generic
    # "AI returned invalid JSON".
    preview = cleaned[:3000]

    raise ValueError(
        "AI returned invalid JSON.\n\n"
        "Actual AI response:\n"
        f"{preview}"
    )


# ============================================================
# LITERATURE SEARCH
# ============================================================

def search_papers(query, max_results=3):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    arxiv_client = arxiv.Client()
    papers = []

    for result in arxiv_client.results(search):
        papers.append({
            "title": result.title,
            "authors": [
                author.name
                for author in result.authors[:5]
            ],
            "abstract": result.summary[:1000],
            "url": result.entry_id,
            "published": str(result.published)
        })

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
Generate exactly 3 testable scientific hypotheses.

Research question:
{question[:2000]}

Relevant literature:
{literature}

Return a JSON OBJECT with a single key called "hypotheses".

The value of "hypotheses" must be an array containing exactly
3 objects.

Each object MUST contain these keys:

- hypothesis
- reasoning
- experiment
- expected_result
- falsification
- novelty

Example structure:

{{
  "hypotheses": [
    {{
      "hypothesis": "Example hypothesis",
      "reasoning": "Scientific reasoning",
      "experiment": "Proposed experiment",
      "expected_result": "Expected result",
      "falsification": "What result would falsify it",
      "novelty": "Why this is potentially novel"
    }},
    {{
      "hypothesis": "Example hypothesis 2",
      "reasoning": "Scientific reasoning",
      "experiment": "Proposed experiment",
      "expected_result": "Expected result",
      "falsification": "What result would falsify it",
      "novelty": "Why this is potentially novel"
    }},
    {{
      "hypothesis": "Example hypothesis 3",
      "reasoning": "Scientific reasoning",
      "experiment": "Proposed experiment",
      "expected_result": "Expected result",
      "falsification": "What result would falsify it",
      "novelty": "Why this is potentially novel"
    }}
  ]
}}

Return ONLY valid JSON.
"""

    result = ask_scientist(
        prompt,
        json_mode=True
    )

    parsed = parse_json(result)

    # Handle the new object format.
    if isinstance(parsed, dict) and "hypotheses" in parsed:
        return parsed["hypotheses"]

    # Also tolerate the old array format.
    if isinstance(parsed, list):
        return parsed

    raise ValueError(
        "AI returned JSON, but it did not contain "
        "a 'hypotheses' array."
    )


# ============================================================
# CHOOSE EXPERIMENT
# ============================================================

def choose_experiment(question, hypotheses, previous_results=None):
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

Return ONLY valid JSON with exactly these keys:

{{
  "selected_hypothesis": "...",
  "reason": "...",
  "experiment_goal": "...",
  "expected_result": "...",
  "success_metric": "..."
}}
"""

    result = ask_scientist(
        prompt,
        json_mode=True
    )

    return parse_json(result)


# ============================================================
# GENERATE EXPERIMENT
# ============================================================

def generate_experiment(question, hypothesis, experiment_goal):
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
- Return ONLY Python code.
"""

    return ask_scientist(prompt)


# ============================================================
# ANALYSIS
# ============================================================

def analyze_results(question, hypothesis, output):
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
"""

    return ask_scientist(prompt)


# ============================================================
# SAVE EXPERIMENT
# ============================================================

def save_experiment(
    question,
    experiment_number,
    hypothesis,
    code,
    output,
    analysis
):
    os.makedirs("experiments", exist_ok=True)

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
        "analysis": analysis
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return filename


# ============================================================
# FINAL REPORT
# ============================================================

def generate_final_report(question, papers, hypotheses, history):
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
                "py"
            ):
                code = "\n".join(lines[1:])

    return code.strip()

