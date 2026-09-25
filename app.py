from ems.models import PatientCase, VitalSigns
from ems.safety import research_disclaimer

import os
import subprocess
import tempfile

import streamlit as st

from scientist import (
    search_papers,
    generate_hypotheses,
    choose_experiment,
    generate_experiment,
    analyze_results,
    save_experiment,
    generate_final_report,
    clean_python_code,
)


st.set_page_config(
    page_title="Paramedic AI Scientist",
    page_icon="🧪",
    layout="wide",
)


from ems.models import PatientCase, VitalSigns
from ems.safety import research_disclaimer

import os
import subprocess
import tempfile

import streamlit as st


# ------------------------------------------------------------
# DIAGNOSTIC IMPORT
# ------------------------------------------------------------

try:
    from scientist import (
        search_papers,
        generate_hypotheses,
        choose_experiment,
        generate_experiment,
        analyze_results,
        save_experiment,
        generate_final_report,
        clean_python_code,
    )

except Exception as e:
    st.error("Could not import scientist.py")
    st.exception(e)
    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "papers" not in st.session_state:
    st.session_state.papers = []

if "hypotheses" not in st.session_state:
    st.session_state.hypotheses = []


# ============================================================
# HELPERS
# ============================================================

def validate_experiment_code(code):
    blocked_patterns = [
        "os.system",
        "subprocess",
        "shutil",
        "socket",
        "requests",
        "urllib",
        "httpx",
        "exec(",
        "eval(",
        "__import__",
        "import os",
        "import sys",
        "import subprocess",
    ]

    code_lower = code.lower()

    for pattern in blocked_patterns:
        if pattern.lower() in code_lower:
            return False, (
                f"Blocked potentially unsafe operation: {pattern}"
            )

    return True, ""



def run_experiment_code(code):
    code = clean_python_code(code)

    safe, message = validate_experiment_code(code)

    if not safe:
        return False, f"Experiment blocked:\n{message}"

    filename = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8",
        ) as f:
            f.write(code)
            filename = f.name

        # Force UTF-8 output on Windows so AI-generated
        # experiments can safely print Unicode characters.
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        result = subprocess.run(
            ["python", filename],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            timeout=60,
        )

        output = result.stdout.strip()

        if result.returncode != 0:
            error = result.stderr.strip()

            output += (
                "\n\n--- EXPERIMENT ERROR ---\n"
                + error[-4000:]
            )

            return False, output

        if result.stderr.strip():
            output += (
                "\n\n--- WARNINGS ---\n"
                + result.stderr[-2000:]
            )

        return True, output

    except subprocess.TimeoutExpired:
        return (
            False,
            "Experiment stopped because it exceeded "
            "the 60-second time limit.",
        )

    except Exception as e:
        return False, f"Experiment execution failed:\n{e}"

    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except OSError:
                pass


# ============================================================
# HEADER
# ============================================================

st.title("🚑 Paramedic AI Scientist")

st.write(
    "AI research assistant for EMS evidence review, "
    "clinical research, simulation, and data analysis."
)

st.caption(
    research_disclaimer()
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.header("Research Settings")

    experiment_count = st.slider(
        "Number of experiments",
        min_value=1,
        max_value=5,
        value=1,
    )

    st.caption(
        "Use 1–3 experiments with the current API limits."
    )

research_mode = st.selectbox(
    "Research Mode",
    [
        "Clinical Evidence Review",
        "EMS Protocol Research",
        "Clinical Prediction Model",
        "Patient Simulation",
        "Retrospective Data Analysis",
        "Quality Improvement",
    ],
)

# ============================================================
# QUESTION
# ============================================================

question = st.text_area(
    "🔬 Research Question",
    placeholder=(
        "Example: Can Random Forest outperform "
        "a Decision Tree on the Iris dataset?"
    ),
    height=120,
)


run_research = st.button(
    "🚀 Run Research",
    type="primary",
    use_container_width=True,
)


# ============================================================
# RESEARCH
# ============================================================

st.divider()

st.header("🧑‍⚕️ EMS Case")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        value=65,
    )

with col2:
    sex = st.selectbox(
        "Sex",
        [
            "Not specified",
            "Female",
            "Male",
            "Other",
        ],
    )

with col3:
    chief_complaint = st.text_input(
        "Chief Complaint",
        placeholder="Shortness of breath",
    )

st.subheader("Vital Signs")

v1, v2, v3, v4 = st.columns(4)

with v1:
    heart_rate = st.number_input(
        "HR",
        min_value=0,
        max_value=300,
        value=80,
    )

with v2:
    respiratory_rate = st.number_input(
        "RR",
        min_value=0,
        max_value=100,
        value=16,
    )

with v3:
    spo2 = st.number_input(
        "SpO₂",
        min_value=0,
        max_value=100,
        value=98,
    )

with v4:
    etco2 = st.number_input(
        "ETCO₂",
        min_value=0,
        max_value=100,
        value=35,
    )

history = st.text_area(
    "Relevant History",
    placeholder="COPD, CHF, diabetes...",
)

exam = st.text_area(
    "Physical Examination",
    placeholder="Wheezing, diaphoresis, edema...",
)

patient = PatientCase(
    age=age,
    sex=sex,
    chief_complaint=chief_complaint,

    history=[
        item.strip()
        for item in history.split(",")
        if item.strip()
    ],

    vital_signs=VitalSigns(
        heart_rate=heart_rate,
        respiratory_rate=respiratory_rate,
        spo2=spo2,
        etco2=etco2,
    ),

    physical_exam=exam,
)

if run_research:

    if not question.strip():
        st.warning(
            "Please enter a research question first."
        )
        st.stop()

    # Clear previous run
    st.session_state.history = []


    # ========================================================
    # LITERATURE
    # ========================================================

    st.divider()
    st.header("📚 Literature Search")

    try:
        with st.spinner(
            "Searching arXiv..."
        ):
            papers = search_papers(
                question,
                max_results=3,
            )

        st.session_state.papers = papers

        st.success(
            f"Found {len(papers)} relevant papers."
        )

    except Exception as e:
        papers = []
        st.session_state.papers = []

        st.warning(
            f"Literature search failed: {e}"
        )


    for paper in papers:

        title = paper.get(
            "title",
            "Untitled paper",
        )

        with st.expander(title):

            st.write(
                paper.get(
                    "abstract",
                    "",
                )
            )

            authors = paper.get(
                "authors",
                [],
            )

            if authors:
                st.caption(
                    ", ".join(authors)
                )


    # ========================================================
    # HYPOTHESES
    # ========================================================

    st.divider()
    st.header("🧠 Hypotheses")

    try:

        with st.spinner(
            "Generating hypotheses..."
        ):

            hypotheses = generate_hypotheses(
                question,
                papers,
            )

        st.session_state.hypotheses = hypotheses

    except Exception as e:

        st.error(
            f"Hypothesis generation failed: {e}"
        )

        st.stop()


    if not isinstance(
        hypotheses,
        list,
    ):
        hypotheses = [hypotheses]


    for index, hypothesis in enumerate(
        hypotheses,
        start=1,
    ):

        if not isinstance(
            hypothesis,
            dict,
        ):
            continue

        title = hypothesis.get(
            "hypothesis",
            f"Hypothesis {index}",
        )

        with st.expander(
            f"Hypothesis {index}: {title}"
        ):

            st.write(
                "**Reasoning**"
            )

            st.write(
                hypothesis.get(
                    "reasoning",
                    "",
                )
            )

            st.write(
                "**Proposed experiment**"
            )

            st.write(
                hypothesis.get(
                    "experiment",
                    "",
                )
            )

            st.write(
                "**Expected result**"
            )

            st.write(
                hypothesis.get(
                    "expected_result",
                    "",
                )
            )

            st.write(
                "**Falsification**"
            )

            st.write(
                hypothesis.get(
                    "falsification",
                    "",
                )
            )


    # ========================================================
    # EXPERIMENT LOOP
    # ========================================================

    st.divider()
    st.header("🧪 Experiments")


    for experiment_number in range(
        experiment_count
    ):

        st.subheader(
            f"Experiment {experiment_number + 1}"
        )


        # ----------------------------------------------------
        # CHOOSE
        # ----------------------------------------------------

        try:

            with st.spinner(
                "Choosing experiment..."
            ):

                decision = choose_experiment(
                    question,
                    hypotheses,
                    st.session_state.history,
                )

        except Exception as e:

            st.error(
                f"Experiment selection failed: {e}"
            )

            break


        if not isinstance(
            decision,
            dict,
        ):
            st.error(
                "Scientist returned an invalid experiment plan."
            )
            break


        selected_hypothesis = decision.get(
            "selected_hypothesis",
            "",
        )

        experiment_goal = decision.get(
            "experiment_goal",
            decision.get(
                "goal",
                "",
            ),
        )


        st.write(
            "**Selected hypothesis:**"
        )

        st.info(
            selected_hypothesis
        )


        st.write(
            "**Experiment goal:**"
        )

        st.info(
            experiment_goal
        )


        # ----------------------------------------------------
        # GENERATE CODE
        # ----------------------------------------------------

        try:

            with st.spinner(
                "Generating Python experiment..."
            ):

                code = generate_experiment(
                    question,
                    selected_hypothesis,
                    experiment_goal,
                )

            # Critical: clean immediately.
            code = clean_python_code(code)

        except Exception as e:

            st.error(
                f"Experiment generation failed: {e}"
            )

            break


        with st.expander(
            "🐍 Generated Python",
            expanded=False,
        ):

            st.code(
                code,
                language="python",
            )


        # ----------------------------------------------------
        # EXECUTE
        # ----------------------------------------------------

        with st.spinner(
            "Running experiment..."
        ):

            success, output = run_experiment_code(
                code
            )


        if success:

            st.success(
                "Experiment completed successfully."
            )

        else:

            st.error(
                "Experiment failed."
            )


        with st.expander(
            "📊 Results",
            expanded=True,
        ):

            st.code(
                output or "(No output)",
                language="text",
            )


        # ----------------------------------------------------
        # ANALYZE
        # ----------------------------------------------------

        try:

            with st.spinner(
                "Analyzing results..."
            ):

                analysis = analyze_results(
                    question,
                    selected_hypothesis,
                    output,
                )

        except Exception as e:

            analysis = (
                f"Analysis failed: {e}"
            )


        with st.expander(
            "🔎 Scientific Analysis",
            expanded=True,
        ):

            st.markdown(
                analysis
            )


        # ----------------------------------------------------
        # HISTORY
        # ----------------------------------------------------

        record = {
            "experiment": experiment_number + 1,
            "hypothesis": selected_hypothesis,
            "goal": experiment_goal,
            "code": code,
            "output": output,
            "analysis": analysis,
        }

        st.session_state.history.append(
            record
        )


        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        try:

            save_experiment(
                question=question,
                experiment_number=(
                    experiment_number + 1
                ),
                hypothesis=selected_hypothesis,
                code=code,
                output=output,
                analysis=analysis,
            )

        except Exception as e:

            st.warning(
                f"Could not save experiment: {e}"
            )


    # ========================================================
    # FINAL REPORT
    # ========================================================

    if len(st.session_state.history) > 0:

        st.divider()
        st.header("📄 Final Research Report")


        try:

            with st.spinner(
                "Generating final report..."
            ):

                final_report = generate_final_report(
                    question=question,
                    papers=st.session_state.papers,
                    hypotheses=st.session_state.hypotheses,
                    history=st.session_state.history,
                )


            st.markdown(
                final_report
            )


            st.download_button(
                label="⬇️ Download Research Report",
                data=final_report,
                file_name="research_report.md",
                mime="text/markdown",
                use_container_width=True,
            )


        except Exception as e:

            st.error(
                f"Final report failed: {e}"
            )


# ============================================================
# PREVIOUS RESULTS
# ============================================================

if (
    not run_research
    and len(st.session_state.history) > 0
):

    st.divider()
    st.header("Previous Research")

    for item in st.session_state.history:

        number = item.get(
            "experiment",
            "?",
        )

        st.write(
            f"Experiment {number}"
        )
