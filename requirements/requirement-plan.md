# LLM-Driven Diagram Generation with Local PlantUML Jar

## Overview

We will integrate a Large Language Model (LLM) to automatically generate PlantUML diagram code from a user's description, **while continuing to use the local PlantUML JAR for rendering**. This ensures that **diagram image generation remains offline and internal**. The only external call will be the LLM API request; the rendering will use the same internal process as the existing editor.

**Key Changes in Approach:**

* **LLM Integration:** Use an LLM to convert natural-language diagram descriptions into PlantUML syntax.
* **Local Rendering:** feed the LLM-generated PlantUML text into the local PlantUML JAR (just as the current editor does) to produce an SVG image.
* **Frontend Trigger:** The front-end will initiate this process when the user provides a description and requests a diagram.

This revised plan preserves the existing rendering workflow and minimizes external dependencies. Below, we detail the end-to-end process and the modifications required in both the frontend and backend.

## Frontend – Triggering Diagram Generation

The front-end will provide a new interface (e.g. a text input or modal) for users to describe their desired diagram in natural language. Key steps and UI/flow changes:

* **User Input:** Add a text area or dialog where the user enters a **diagram description** (for example, *"A sequence diagram with User and Server where User requests data and Server responds"*).

* **Generate Diagram Button:** Provide a button (e.g. "Generate Diagram") that the user clicks to submit this description.

* **API Call Initiation:** On click, the frontend JavaScript will send an HTTP POST request to a new backend endpoint (say, `/generateDiagram`) with the description in JSON format. This is similar to how the existing editor sends diagram code to the `/render` endpoint. For example:

  ```js
  // Pseudo-code for triggering generation
  const description = userDescriptionInput.value;
  fetch("/generateDiagram", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description: description })
  }).then(response => response.text())
    .then(svgContent => {
        // Display the SVG returned by the backend
        diagramContainer.innerHTML = svgContent;
    });
  ```

* **Loading Indicator:** Reuse or extend the existing loading overlay (`toggleLoadingOverlay()` is already in use during rendering) to give feedback while the LLM and rendering are processing.

* **Display Result:** When the response arrives, inject the returned SVG into the page (e.g., by setting `innerHTML` of the diagram container, as done in `fetchSvgFromPlantUml()`). The diagram will then appear just as if it had been produced by manual code input.

After generation, we will also **populate the code editor with the generated PlantUML text**. This will let users see or tweak the UML code. The frontend will receive both the SVG and the PlantUML text (perhaps by returning a JSON with both) and call the existing `setPuml()` function to load the code into the editor. This ensures the user can fine-tune the diagram using the familiar editor if needed.

## Backend – Flask Endpoint for LLM and Rendering

On the backend, we'll implement a new Flask route (e.g., `/generateDiagram`) to handle the description-to-diagram workflow. The steps on the server side are:

1. **Receive Description:** The Flask endpoint parses the incoming JSON for the `description` field (similar to how `/render` reads the `plantuml` field). For example:

   ```python
   @plantuml.route("/generateDiagram", methods=["POST"])
   def generate_diagram():
       data = request.get_json()
       user_desc = data.get("description", "")
       # ... use user_desc in next steps
   ```

2. **Call LLM for PlantUML Text:** Use the LLM API or model call to transform the `user_desc` into PlantUML code. This involves:

   * **Prompt Construction:** Format a prompt for the LLM that instructs it to output a PlantUML diagram. For instance: *"Convert the following description into a PlantUML diagram. Only output valid PlantUML code between ****************************`@startuml`**************************** and ****************************`@enduml`****************************."* Then include the user description.
   * **LLM API Request:** Send this prompt to the chosen LLM (e.g., via OpenAI API or a local model) and await the response.
   * **Extract Diagram Text:** Retrieve the PlantUML text from the LLM's response. We must ensure the text includes the proper `@startuml` and `@enduml` tags and follows PlantUML syntax. (If not, we may prepend/append them or validate the syntax before rendering.)

   *Implementation note:* This step is the **only external call** in the process (if using an external LLM API). Ensure to handle network timeouts or errors gracefully. If the LLM fails to produce output, return a clear error message to the user.

3. **Render with PlantUML JAR:** Once we have the PlantUML diagram text from the LLM, feed it into the local PlantUML JAR to generate the SVG:

   * We will **reuse the existing rendering logic**. The project already defines a helper function `_create_svg_from_uml(uml:str)` that runs the PlantUML jar via a subprocess. This function uses the environment variable `PLANTUML_JAR` and the `java` command with `-pipe` to accept UML text from stdin, outputting SVG (`-tsvg`).
   * Call `_create_svg_from_uml(diagram_text)` to get the SVG content. This is the same function used by the current `/render` endpoint, ensuring our new route produces identical results as the manual workflow.

4. **Return SVG Response:** Return the SVG content directly as the HTTP response. Since `_create_svg_from_uml` already returns SVG text, we can do: `return _create_svg_from_uml(diagram_text)`. The Flask route will return a text/HTML response containing the raw `<svg>...</svg>` string. The front-end will insert this into the DOM to display the image.

## Diagram Generation Flow Summary

Bringing it all together, the end-to-end flow with the revised plan is:

1. **User Action:** User enters a diagram description and clicks "Generate Diagram" on the frontend.
2. **Frontend Request:** Browser sends a POST request to the Flask backend (`/generateDiagram`) with the description (JSON payload).
3. **LLM Conversion (Backend):** Flask handler receives the description, calls the LLM to get corresponding PlantUML code.
4. **Local Rendering (Backend):** The generated PlantUML text is passed into the local PlantUML JAR (via `_create_svg_from_uml`), producing an SVG image (as text).
5. **Response:** The backend returns the SVG content to the frontend (over HTTP).
6. **Display (Frontend):** The browser injects the SVG into the page, displaying the diagram. Optionally, the PlantUML code can be loaded into the code editor panel for user reference or editing.

All steps after the LLM call mirror the existing editor behavior, so the user experience (instant diagram preview, interactive capabilities) remains consistent. The difference is that the user now has an AI-assisted way to create the initial diagram code.

## Summary

In summary, this feature plan streamlines the diagram generation pipeline: **the frontend triggers an LLM to generate diagram text, and the backend uses the local PlantUML JAR to render the SVG**, exactly as the existing editor does for user-written UML. This approach requires minimal changes to the current codebase, leverages proven components, and keeps the entire process (aside from the LLM call) self-contained. By doing so, we maintain a smooth user experience while adding the powerful new capability of AI-driven diagram creation.

**References:** The implementation will utilize existing functions and endpoints in the codebase for rendering and integration:

* PlantUML Jar invocation (`java -jar ... -tsvg`) for SVG generation.
* Current `/render` endpoint logic which returns the SVG text directly to the client.
* Frontend fetching of `/render` and inserting SVG content (to be mirrored in the new generation flow).
