Streamlit Host: https://ai-paramedic-scientist.streamlit.app/

# 🚑 Paramedic AI Scientist

An experimental AI-powered research assistant designed to explore **paramedicine, emergency medical services (EMS), prehospital medicine, and clinical research questions**.

The project combines literature search, AI-generated hypotheses, simulated experiments, result analysis, and automated research reporting into a single Streamlit application.

> ⚠️ **Educational / Research Prototype**
>
> This project is not a medical device, clinical decision-support system, or substitute for a qualified clinician, paramedic, physician, medical director, or local EMS protocol. It should not be used to make real-world patient-care decisions.

---

## 🧠 What It Does

The Paramedic AI Scientist follows an experimental research pipeline:

```text
Research Question
       │
       ▼
📚 Literature Search
       │
       ▼
🧠 Hypothesis Generation
       │
       ▼
🔬 Experiment Selection
       │
       ▼
🐍 Python Experiment
       │
       ▼
📊 Results
       │
       ▼
🔎 Scientific Analysis
       │
       ▼
📄 Research Report
```

The goal is to make an AI system capable of behaving more like a **research assistant** than a conventional chatbot.

---

## 🚑 Parametic / EMS Focus

The project is being developed toward research and educational applications involving:

* Prehospital medicine
* Emergency medical services
* Paramedicine
* Emergency medicine
* Patient assessment
* Vital signs
* Clinical prediction concepts
* EMS protocols
* Triage research
* Treatment comparisons
* Airway management research
* Trauma research
* Cardiac arrest research
* Sepsis research
* Medication research
* EMS operations
* Clinical education
* Simulation-based learning

The long-term goal is to allow users to ask questions such as:

> "What factors are associated with deterioration in patients with suspected sepsis?"

or:

> "What does the current literature say about different approaches to prehospital airway management?"

and have the system investigate the question systematically.

---

# 🔬 Current Architecture

The project currently contains several major components.

### Literature Search

The system searches scientific literature using arXiv.

### Hypothesis Generation

Groq-powered language models generate multiple testable hypotheses from the research question and available literature.

### Experiment Selection

The system evaluates the available hypotheses and chooses a potentially informative experiment.

### Experiment Generation

The AI generates Python code for controlled research experiments.

Current experiments are designed around libraries such as:

* NumPy
* Pandas
* SciPy
* scikit-learn
* Matplotlib

### Experiment Execution

Generated Python experiments can be executed by the application with basic safety restrictions and execution time limits.

### Scientific Analysis

The AI reviews experimental output and identifies:

* Important findings
* Numerical results
* Whether the hypothesis was supported
* Limitations
* Potential confounders
* Possible follow-up experiments

### Research Reports

The system generates a structured Markdown report containing:

* Abstract
* Research Question
* Literature Context
* Hypotheses
* Methods
* Results
* Discussion
* Limitations
* Conclusion
* Future Experiments

---

# 🛠️ Technology Stack

## Frontend

**Streamlit**

Provides the interactive research interface.

## AI

**Groq**

Used to run the language-model component of the research system.

The current model configuration uses:

```text
openai/gpt-oss-120b
```

## Literature

**arXiv**

Used for experimental literature retrieval.

## Scientific Python

The project currently uses:

```text
numpy
pandas
scikit-learn
matplotlib
scipy
```

## Configuration

Environment variables are loaded using:

```text
python-dotenv
```

---

# 📁 Project Structure

A typical project structure looks like:

```text
paramedic-ai-scientist/
│
├── app.py
├── scientist.py
├── requirements.txt
├── .env
├── README.md
│
├── ems/
│   ├── __init__.py
│   └── models.py
│
└── experiments/
    └── ...
```

### `app.py`

The Streamlit user interface and research workflow.

### `scientist.py`

The AI research engine.

Contains functionality for:

* Groq interaction
* Literature search
* Hypothesis generation
* Experiment selection
* Experiment generation
* Result analysis
* Report generation
* Experiment storage

### `ems/`

EMS-specific data models and functionality.

### `experiments/`

Saved experimental runs and results.

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd paramedic-ai-scientist
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
streamlit
groq
python-dotenv
arxiv
numpy
pandas
scikit-learn
matplotlib
scipy
```

---

# 🔑 Configuration

Create a `.env` file in the project directory:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Do **not** commit your `.env` file to Git.

Your `.gitignore` should contain:

```text
.env
.venv/
__pycache__/
*.pyc
```

---

# ▶️ Running the Application

Start Streamlit:

```powershell
streamlit run app.py
```

The application should open in your browser.

---

# 🧪 Example Research Question

Try a general research question first:

```text
Can Random Forest outperform a Decision Tree on a classification dataset?
```

The system will attempt to:

1. Find relevant literature
2. Generate hypotheses
3. Select an experiment
4. Generate Python
5. Run the experiment
6. Analyze the results
7. Generate a final report

---

# 🚑 Future EMS Research Mode

The long-term direction of the project is to move beyond generic machine-learning experiments.

A future EMS research workflow could look like:

```text
EMS Research Question
        │
        ▼
Literature Retrieval
        │
        ▼
Evidence Extraction
        │
        ▼
Clinical Research Hypotheses
        │
        ▼
Study Design
        │
        ▼
Synthetic / Public Dataset
        │
        ▼
Statistical Analysis
        │
        ▼
Evidence Summary
        │
        ▼
Research Report
```

Potential future capabilities include:

### 📋 Patient Case Simulation

Generate synthetic EMS cases containing:

* Age
* Presenting complaint
* Vital signs
* History
* Physical findings
* Treatments
* Response to treatment
* Transport information

### 🫀 Physiological Modeling

Explore simulated relationships between:

* Heart rate
* Blood pressure
* Respiratory rate
* SpO₂
* Temperature
* Mental status
* Shock indicators

### 📚 Evidence Synthesis

Compare research findings across multiple papers instead of relying on a single source.

### 📊 Statistical Research

Automatically perform analyses such as:

* Descriptive statistics
* Confidence intervals
* Regression
* Classification
* Sensitivity/specificity
* ROC analysis
* Cross-validation
* Effect-size estimation

### 🧪 Research Planning

The AI could propose:

* Research questions
* Study designs
* Variables
* Inclusion/exclusion criteria
* Outcomes
* Statistical methods
* Potential confounders

---

# 🔐 Safety

This project can generate and execute AI-generated Python code.

That introduces security risks.

The current application includes basic restrictions intended to reduce obvious unsafe behavior, but **these protections should not be considered a secure sandbox**.

Do not run untrusted generated code on a machine containing sensitive information.

A future version should use:

* Container isolation
* Resource limits
* Network isolation
* Read-only filesystems
* CPU/memory limits
* Process isolation
* Explicit package allowlists
* Execution time limits

---

# 🏥 Clinical Safety

This project is intended for:

* Research
* Education
* Simulation
* Software experimentation

It is **not intended to diagnose, treat, triage, or manage real patients**.

AI-generated medical information can be incorrect, incomplete, outdated, or inappropriate for a specific patient.

Real-world patient care should follow:

* Local EMS protocols
* Medical direction
* Current clinical guidelines
* Applicable laws and regulations
* Professional training
* Appropriate clinical judgment

---

# 🔬 Research Philosophy

The project is designed around a simple principle:

> **An AI should not simply answer a research question. It should investigate it.**

Instead of:

```text
Question → AI Answer
```

the goal is:

```text
Question
   ↓
Evidence
   ↓
Hypotheses
   ↓
Experiment
   ↓
Results
   ↓
Critique
   ↓
Next Experiment
   ↓
Conclusion
```

This creates a foundation for experimenting with **AI-assisted scientific reasoning and EMS research**.

---

# 🚧 Current Status

This is an **early-stage research prototype**.

Current capabilities include:

* [x] Streamlit interface
* [x] Groq integration
* [x] Literature search
* [x] AI hypothesis generation
* [x] Experiment selection
* [x] Python experiment generation
* [x] Experiment execution
* [x] Result analysis
* [x] Research report generation
* [x] Experiment persistence
* [ ] Robust scientific evidence synthesis
* [ ] EMS-specific research datasets
* [ ] Advanced statistical analysis
* [ ] Secure experiment sandbox
* [ ] Clinical evidence validation
* [ ] Human review workflow

---

# 🤝 Contributing

Contributions are welcome.

Areas that would be particularly useful include:

* EMS datasets
* Statistical methods
* Literature retrieval
* Evidence synthesis
* Simulation environments
* Secure code execution
* Scientific evaluation
* Paramedic education
* Clinical research methodology

When contributing medical or clinical functionality, prioritize evidence, transparency, limitations, and patient safety.

---

# 📜 License

Add your preferred open-source license here.

For example:

```text
MIT License
```

---

# ⚠️ Disclaimer

This software is an experimental research and educational project.

It is not a medical device and has not been validated for clinical use.

The authors and contributors make no representation that information produced by the system is accurate, complete, current, or suitable for patient care.

**Never use this software as the sole basis for a real-world medical decision.**
