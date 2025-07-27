# Product Requirements Document (PRD)
**Feature:** AI Assistant for PlantUML Interactive Editor  
**Revision:** v0.1 (2025‑07‑27)  
**Author:** Draft (ChatGPT)

---

## 1  Introduction / Overview
The **AI Assistant** adds a natural‑language "diagram‑from‑description" capability to the existing PlantUML Interactive Editor. It lets users type a plain‑English description (e.g., "Two classes – User and Account – with a one‑to‑many relationship") and instantly receive:

1. Valid PlantUML code inserted into the editor.
2. The rendered SVG diagram—generated locally via the editor’s current PlantUML JAR pipeline.

This feature solves two problems:

* **Lower entry barrier:** Users unfamiliar with PlantUML syntax can still create diagrams.
* **Faster prototyping:** Power users can sketch ideas quickly, then fine‑tune with the existing interactive tools.

---

## 2  Goals (SMART)
| # | Goal | Metric / Target |
|---|------|----------------|
| G1 |Enable users to create a first‑draft diagram *without writing PlantUML code*.|≥ 80 % of onboarding test users produce a diagram via AI Assistant in ≤ 2 minutes.|
| G2 |Maintain existing rendering performance.|AI‑generated diagram appears in ≤ 2 s (±10 % of current render time).|
| G3 |Preserve local / offline rendering security.|**0** external calls for rendering (only LLM API call permitted).|
| G4 |Achieve high code accuracy.|≥ 90 % of AI‑generated diagrams render without syntax errors.|
| G5 |Collect feedback for improvement.|In‑app “Was this helpful?” prompt ≥ 25 % response rate during beta.|

---

## 3  User Stories
| ID | Story |
|----|-------|
| US‑1 |As a **new UX designer**, I want to describe a flow in plain English so that I can see a UML diagram without learning PlantUML.|
| US‑2 |As a **software architect**, I want to quickly draft a sequence diagram from a high‑level scenario so that I can refine it with manual edits.|
| US‑3 |As a **teacher**, I want students to generate diagrams from prose requirements so that they focus on system thinking, not syntax.|
| US‑4 |As a **power user**, I want the AI Assistant to paste the generated PlantUML into the editor so that I can tweak labels and styles immediately.|
| US‑5 |As a **security‑conscious user**, I want all rendering to remain local so that my diagrams are not sent to external servers.|

---

## 4  Functional Requirements
| # | Requirement |
|---|-------------|
| FR‑1 |The UI **must** provide a text input (modal textarea) and a “Generate Diagram” button.|
| FR‑2 |On button press, the browser **must** POST JSON `{ description: <string> }` to `/generateDiagram`.|
| FR‑3 |The Flask route `/generateDiagram` **must**: a) validate input; b) call the LLM API; c) extract PlantUML code; d) pass code to existing `_create_svg_from_uml`; e) return JSON `{ plantuml, svg }`.|
| FR‑4 |The frontend **must** display a loading overlay during processing.|
| FR‑5 |On success, the Ace editor **must** load `plantuml` and the diagram container **must** render `svg`.|
| FR‑6 |Existing interactive editing **must** work on AI‑generated code.|
| FR‑7 |If rendering fails, the backend **must** return 422 with error; the UI **must** show the error popup.|
| FR‑8 |A telemetry hook **should** log anonymized generation events.|
| FR‑9 |The LLM API key **must not** be exposed to the client.|

---

## 5  Non‑Goals (Out of Scope)
* Integrating with external renderers (e.g., Kroki).
* Multi‑turn chat interface.
* Heuristic auto‑fixes for malformed diagrams beyond basic validation.
* Hosting an on‑device LLM model for offline inference (future work).

---

## 6  Design Considerations
* **Consistency:** Add a “🪄 AI” button to the existing Bootstrap toolbar.
* **Modal:** Reuse current modal styles for multi‑line descriptions.
* **Loading & Toasts:** Use existing overlay spinner and success toast (“Diagram generated — you can now edit it.”).
* **Error Handling:** Leverage existing red popup for syntax/LLM errors.
* **Accessibility:** Button `aria-label="Generate diagram with AI assistant"`.

---

## 7  Technical Considerations
| Topic | Notes |
|-------|-------|
|LLM Provider|Start with OpenAI GPT‑4o; wrap in `assistant.py` for easy swapping.|
|Prompt Template|"Create a PlantUML diagram. Output only PlantUML between @startuml and @enduml." + user description.|
|Rate Limiting|60 requests/min per IP on `/generateDiagram`.|
|Dependencies|Add `openai` to `pyproject.toml`.|
|Security|Validate/escape user input; cap LLM output to 5 000 chars.|
|Testing|Unit tests mock LLM; integration test ensures valid SVG returned.|
|Config|New env vars: `LLM_API_KEY`, `LLM_MODEL_NAME`, `LLM_TIMEOUT`.|

---

## 8  Success Metrics
| Metric | Target |
|--------|--------|
|Generation success rate|≥ 90 %|
|Median time click→diagram|≤ 2 s|
|New‑user activation|+20 % vs. baseline|
|User satisfaction|≥ 4 / 5 average|
|Support tickets about PlantUML syntax|‑30 % in first month|

---

## 9  Open Questions
1. Which LLM model tier will we fund (GPT‑4o vs.​ cheaper)?  
2. Do we need caching or quotas for cost control?  
3. Should we localize prompts for non‑English users?  
4. What telemetry granularity satisfies privacy guidelines?  
5. Timeline for exploring on‑device LLM hosting?

---

## 10  Next Steps
| When | Owner | Action |
|------|-------|--------|
|T+0 d|PM / Lead Dev|Review & approve PRD.|
|T+3 d|Frontend Dev|Add modal + AI button stub.|
|T+5 d|Backend Dev|Implement `/generateDiagram`, integrate LLM SDK.|
|T+8 d|QA|Add happy‑path and error test cases.|
|T+10 d|DevOps|Add `LLM_API_KEY` secret to CI/CD.|
|T+14 d|Team|Internal beta release.|