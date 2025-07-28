# Product Context: AI Assistant for PlantUML Interactive Editor

## Why this project exists

The existing PlantUML Interactive Editor is a powerful tool, but it has a steep learning curve for users unfamiliar with PlantUML syntax. This limits its accessibility and slows down initial diagram creation even for experienced users who might want to quickly sketch ideas.

## Problems it solves

1.  **Lower entry barrier:** New users can create diagrams without needing to learn PlantUML syntax upfront.
2.  **Faster prototyping:** Power users can rapidly generate initial diagrams from high-level descriptions, then refine them manually.

## How it should work

The AI Assistant will provide a simple text input where users describe their desired diagram in natural language. Upon submission, the system will:
1.  Send the description to an LLM (Large Language Model) to generate PlantUML code.
2.  Feed the generated PlantUML code into the existing local PlantUML JAR for rendering.
3.  Display the resulting SVG diagram in the editor's diagram view.
4.  Populate the Ace editor with the generated PlantUML code, allowing for immediate manual refinement.

## User experience goals

-   **Intuitive:** The process of generating a diagram from a description should be straightforward and easy to understand.
-   **Fast:** AI-generated diagrams should appear quickly (target ≤ 2 seconds).
-   **Seamless integration:** The AI-generated code and diagram should integrate seamlessly with the existing editor's functionality, allowing for continued interactive editing.
-   **Secure:** All diagram rendering must remain local, with only the LLM API call being external.
-   **Helpful:** The feature should genuinely assist users in creating diagrams more efficiently and with less friction.
