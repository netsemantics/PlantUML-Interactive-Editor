import os
from openai import OpenAI

def generate_plantuml_code(description: str) -> str:
    """
    Generates PlantUML code from a natural language description using an LLM.
    """
    client = OpenAI(api_key=os.getenv("LLM_API_KEY"))
    model_name = os.getenv("LLM_MODEL_NAME", "gpt-4o")
    timeout = int(os.getenv("LLM_TIMEOUT", 60))

    prompt = (
        "Create a PlantUML diagram based on the following description. "
        "Output only valid PlantUML code, enclosed within `@startuml` and `@enduml` tags. "
        "Do not include any other text or explanations outside these tags.\n\n"
        f"Description: {description}"
    )

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates PlantUML code."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            timeout=timeout,
        )
        plantuml_code = response.choices[0].message.content
        
        # Extract content between @startuml and @enduml if the LLM includes extra text
        start_tag = "@startuml"
        end_tag = "@enduml"
        if start_tag in plantuml_code and end_tag in plantuml_code:
            start_index = plantuml_code.find(start_tag)
            end_index = plantuml_code.find(end_tag, start_index) + len(end_tag)
            plantuml_code = plantuml_code[start_index:end_index]
        
        return plantuml_code

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error generating PlantUML code: {e}")
        raise ValueError(f"Failed to generate PlantUML code: {e}")

if __name__ == "__main__":
    # Example usage for testing
    test_description = "A simple class diagram with a class named 'User' and a class named 'Account'. User has a one-to-many relationship with Account."
    try:
        generated_code = generate_plantuml_code(test_description)
        print("Generated PlantUML Code:\n", generated_code)
    except ValueError as e:
        print(f"Error: {e}")
