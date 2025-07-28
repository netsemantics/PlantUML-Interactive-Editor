# Project Brief: PlantUML Interactive Editor AI Assistant

## Core Requirements and Goals

This project aims to enhance the existing PlantUML Interactive Editor by integrating an AI Assistant. The primary goal is to enable users to generate PlantUML diagrams from natural language descriptions, significantly lowering the entry barrier for new users and accelerating prototyping for experienced users.

The AI Assistant will:
- Accept natural language descriptions of diagrams.
- Convert these descriptions into valid PlantUML code.
- Utilize the existing local PlantUML JAR for rendering the generated code into SVG diagrams.
- Maintain existing rendering performance and ensure local/offline rendering security (only LLM API call is external).

For more in-depth requirements, refer to the documents in the `../requirements` folder.

## Project Scope

The scope includes:
- Frontend UI for text input and triggering AI generation.
- Backend Flask endpoint to handle AI requests, interact with LLM, and render PlantUML locally.
- Integration of LLM API (initially OpenAI GPT-4o).
- Error handling and loading indicators.
- Unit and integration tests for new components.
- Documentation updates.

Out of scope:
- External renderers (e.g., Kroki).
- Multi-turn chat interface.
- Heuristic auto-fixes for malformed diagrams beyond basic validation.
- On-device LLM model hosting.
