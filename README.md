# EHR Clinical Data Reconciliation Engine Demo

A full-stack take-home project that simulates an AI-assisted EHR review workflow for clinicians. The application allows a user to review patient records, run medication reconciliation, evaluate data quality, and inspect AI-generated reasoning, confidence, and recommended actions.

![Website Display](https://i.gyazo.com/6636bd58a2d0c101df8d1004276ddb44.gif)

# Overview

This project includes:

- A FastAPI backend for reconciliation and data quality scoring
- A React frontend for patient review and result visualization
- OpenAI integration for reasoning and safety-aware decision support
- Basic Bearer token authentication
- Unit tests for core backend logic

The goal was to build a simple but clinician-friendly dashboard that presents AI suggestions clearly and allows a provider to review, approve, or reject them.

# Tech Stack
## Backend
### Python 3.13
- FastAPI — API routing and backend framework
- FastAPI TestClient / pytest — backend unit testing
- Pydantic — request and response validation
- OpenAI — LLM-based reasoning and medication judgment
### Security
- Simple Bearer token authentication is required for API access
### Testing
- Includes 8 backend unit tests
- Patching is used to avoid unnecessary live LLM calls during tests

## Frontend
### JavaScript
- React
- Vite
- Tailwind CSS

# APIs

## POST /api/reconcile/medication
Accepts conflicting medication records and returns a reconciled result with confidence and reasoning.
## POST /api/validate/data-quality
Accepts a patient record and returns data quality scores plus detected issues.

# Setup

1. Clone the repository.
2. Install Python dependencies using the pyproject.toml file.
3. Create an .env file in the backend directory.

```cs
OPENAI_API_KEY="your_openai_api_key_here"
API_TOKEN="your_bearer_token_here"
```

4. Run the Backend on terminal. 

```bash
uvicorn main:app --reload
```

5. Backend docs will be available at: http://127.0.0.1:8000/docs

6. Create a new terminal, and cd to frontend.

```bash
cd frontend
npm install
npm run dev
```

7. Frontend will be available at: http://localhost:5173

8. To perform tests, cd to backend folder and run the following command.

```bash
pytest
```

# Architecture Design

I chose Python FastAPI because it provides a clean way to define request/response models, structure modular routes, and quickly expose interactive API docs during development. I chose React / Vite / Tailwind for the frontend because they allowed me to build a fast, component-based UI with minimal overhead and simple visual polish.

For the LLM integration, I used the OpenAI API over Claude LLM due to its cost compared to Claude, and that it provides many models and options for its API. 

# Reconciliation Approach
The reconciliation logic combines simple weighted heuristics with LLM-generated reasoning.

Factors considered include:
- Recency of records
- Source reliability
- Medication dose conflicts
- Agreement between sources
- Clinical context, such as age, conditions, and labs
- Clinical concern, which can reduce confidence when the data is riskier or less consistent

The LLM is then used to generate the clinician-facing reasoning and recommended next steps.

# Data Quality Scoring Approach

The data quality validator evaluates:
- Demographics
- Medications
- Allergies
- Conditions
- Vital signs
- Last updated date

It scores four required dimensions:
- Completeness
- Accuracy
- Timeliness
- Clinical plausibility

The overall score is based on the breakdown and severity of detected issues. Severity levels are used to drive deductions:

The assignment asked for effective prompts with clinical context, human-readable explanations, and implausibility detection.

# Prompt Engineering
To support that, I designed prompts that include:
- Patient context
- The conflicting source records
- Reliability and recency information
- Structured output expectations
- A request for concise clinician-facing reasoning

# Future Improvements

If I had more time, I would have setup Docker containerization and deployment for easier setup. In addition, I would have included Postgres SQL database to store information. 

# Time Spent: 
25 hours and 44 minutes total between Friday to Sunday.
- 12 hours on backend logic and endpoint setup.
- 2 hours on OpenAI LLM integration
- 4 hours on test cases.
- 1 hour on authentication
- 6 hours on frontend setup and events. 

