import os
from openai import OpenAI
from loguru import logger

class AIAssistant:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.model_name = os.getenv("LLM_MODEL_NAME", "gpt-4o")
        self.timeout = int(os.getenv("LLM_TIMEOUT", 30))
        self.client = OpenAI(api_key=self.api_key, timeout=self.timeout)

        if not self.api_key:
            logger.error("LLM_API_KEY environment variable not set.")
            raise ValueError("LLM_API_KEY is not set.")

    def generate_plantuml(self, description: str) -> str:
        """
        Generates PlantUML code from a natural language description using an LLM.
        """
        prompt = self._construct_prompt(description)
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that converts natural language descriptions into PlantUML diagrams. Only output valid PlantUML code between @startuml and @enduml tags."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=5000, # Cap LLM output as per PRD
            )
            plantuml_code = response.choices[0].message.content.strip()
            return self._extract_plantuml_block(plantuml_code)
        except Exception as e:
            logger.error(f"Error calling LLM API: {e}")
            raise RuntimeError(f"Failed to generate PlantUML: {e}")

    def _construct_prompt(self, description: str) -> str:
        """
        Constructs the full prompt for the LLM.
        """
        return f"Convert the following description into a PlantUML diagram:\n\n{description}\n\nOutput only valid PlantUML code between @startuml and @enduml tags."

    def _extract_plantuml_block(self, text: str) -> str:
        """
        Extracts the PlantUML block from the LLM's response.
        Ensures the output starts with @startuml and ends with @enduml.
        """
        start_tag = "@startuml"
        end_tag = "@enduml"

        if start_tag not in text:
            text = start_tag + "\n" + text
        if end_tag not in text:
            text = text + "\n" + end_tag

        # Ensure the tags are at the very beginning and end of the extracted block
        start_index = text.find(start_tag)
        end_index = text.rfind(end_tag) + len(end_tag)

        if start_index != -1 and end_index != -1 and end_index > start_index:
            return text[start_index:end_index].strip()
        else:
            # Fallback if tags are not found or malformed, return original text
            logger.warning("Could not extract proper PlantUML block. Returning full response.")
            return text.strip()
