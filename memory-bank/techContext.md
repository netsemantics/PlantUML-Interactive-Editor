# Technical Context: AI Assistant for PlantUML Interactive Editor

## Technologies Used

-   **Backend:** Python (Flask)
-   **Frontend:** HTML, CSS, JavaScript (with Ace Editor for PlantUML code, Bootstrap for UI components)
-   **LLM Integration:** OpenAI Python SDK (for GPT-4o, configurable)
-   **Dependency Management:** `pyproject.toml` (managed by `pip` or `uv`)
-   **Environment Variables:** `python-dotenv` for loading configuration from `.env.example`
-   **Diagram Rendering:** Local PlantUML JAR (Java-based)
-   **Testing:** `pytest` for Python unit and integration tests, `Jest` for JavaScript tests (though not directly used for this feature's JS tests yet).

## Development Setup

1.  **Virtual Environment:** A Python virtual environment (`.venv`) is created within the project root (`Cline/PlantUML-Interactive-Editor/`) to isolate dependencies.
2.  **Dependency Installation:** Dependencies are installed using `pip install -e .` from `pyproject.toml`. A `requirements.txt` file is generated for easier environment replication.
3.  **Environment Variables:** Critical configurations like `LLM_API_KEY`, `LLM_MODEL_NAME`, and `LLM_TIMEOUT` are loaded from `.env.example` using `python-dotenv`. Users must populate `LLM_API_KEY` for the AI Assistant to function.
4.  **PlantUML JAR:** The `PLANTUML_JAR` environment variable must point to the local PlantUML JAR file.

## Technical Constraints

-   **Local Rendering:** A strict requirement is that diagram rendering must remain local. Only the LLM API call is permitted to be external.
-   **LLM Output Format:** The LLM must be prompted to output only valid PlantUML code, enclosed within `@startuml` and `@enduml` tags.
-   **Rate Limiting:** The backend `/generateDiagram` endpoint will implement rate limiting (e.g., 60 requests/min per IP) to manage LLM costs and prevent abuse.
-   **Output Size:** LLM output will be capped (e.g., 5,000 characters) to prevent excessively large diagrams or malicious payloads.

## Dependencies

-   `flask`: Web framework for the backend.
-   `python-dotenv`: For loading environment variables.
-   `loguru`: For logging (already present).
-   `pyquery`: For HTML parsing (already present).
-   `openai`: Python SDK for interacting with OpenAI's API.

## Tool Usage Patterns

-   **`os.getenv()`:** Used to retrieve environment variables for configuration.
-   **`_create_svg_from_uml()`:** Existing utility function in `render.py` for invoking the PlantUML JAR. This function is critical for maintaining local rendering.
-   **Flask Blueprints:** The `plantuml` blueprint is used to organize routes.
-   **`request.get_json()`:** Used to parse incoming JSON payloads from frontend requests.
