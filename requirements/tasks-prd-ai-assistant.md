## Relevant Files

- `src/plantuml_gui/app.py` - Main Flask application file, will contain the new API endpoint.
- `src/plantuml_gui/assistant.py` - New file to handle interaction with the LLM API.
- `src/plantuml_gui/templates/index.html` - Main HTML file to add the AI button and modal.
- `src/plantuml_gui/static/script.js` - Frontend JavaScript to handle user interaction and API calls.
- `pyproject.toml` - Project dependencies file, to add the `openai` library.
- `.env.example` - Example environment file to add new LLM-related configuration.
- `tests/test_app.py` - Integration tests for the Flask application.
- `tests/test_assistant.py` - Unit tests for the new LLM assistant module.
- `README.md` - Project README to be updated with the new feature.
- `FEATURES.md` - Feature list to be updated.

### Notes

- Unit tests should typically be placed alongside the code files they are testing (e.g., `MyComponent.tsx` and `MyComponent.test.tsx` in the same directory).
- Use `npx jest [optional/path/to/test/file]` to run tests. Running without a path executes all tests found by the Jest configuration.

## Tasks

- [ ] 1.0 Setup and Configuration
  - [ ] 1.1 Add `openai` to `pyproject.toml` dependencies.
  - [ ] 1.2 Add `LLM_API_KEY`, `LLM_MODEL_NAME`, and `LLM_TIMEOUT` to `.env.example`.
  - [ ] 1.3 Update configuration loading in the application to handle the new environment variables.
- [ ] 2.0 Backend Development: Implement AI Assistant API
  - [ ] 2.1 Create `src/plantuml_gui/assistant.py` to encapsulate LLM API logic.
  - [ ] 2.2 Implement the prompt template for generating PlantUML.
  - [ ] 2.3 Add the `/generateDiagram` route to `src/plantuml_gui/app.py`.
  - [ ] 2.4 Implement input validation and error handling for the new route.
  - [ ] 2.5 Integrate the `assistant.py` module with the `/generateDiagram` route.
  - [ ] 2.6 Implement rate limiting for the `/generateDiagram` endpoint.
- [ ] 3.0 Frontend Development: Integrate AI Assistant UI
  - [ ] 3.1 Add a "Generate with AI" button to the toolbar in `src/plantuml_gui/templates/index.html`.
  - [ ] 3.2 Create a modal with a textarea for the user's description in `index.html`.
  - [ ] 3.3 In `src/plantuml_gui/static/script.js`, add an event listener for the AI button.
  - [ ] 3.4 Implement the `fetch` call to the `/generateDiagram` endpoint.
  - [ ] 3.5 Add a loading indicator that displays while the request is in progress.
  - [ ] 3.6 On a successful response, update the Ace editor with the PlantUML code and render the SVG.
  - [ ] 3.7 On a failed response, display an error message to the user.
- [ ] 4.0 Testing: Add Coverage for AI Assistant
  - [ ] 4.1 Create `tests/test_assistant.py` to unit test the LLM wrapper, mocking the API call.
  - [ ] 4.2 Add integration tests to `tests/test_app.py` for the `/generateDiagram` endpoint, covering success and error cases.
- [ ] 5.0 Documentation: Update for AI Assistant Feature
  - [ ] 5.1 Update `README.md` to include a section on the new AI Assistant feature.
  - [ ] 5.2 Update `FEATURES.md` with a detailed description of the AI Assistant.
