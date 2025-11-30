# generator.py
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env automatically
load_dotenv()  # looks for a .env file in the same folder or parent folders

class MedicalGenerator:
    """
    Generates answers about medicines using Groq LLM and retrieved CSV data.
    Also handles general non-medicine queries gracefully.
    """

    def __init__(self, api_key=None, model_name=None, temperature=0.3):
        """
        Args:
            api_key (str): Groq API key (optional, defaults to GROQ_API_KEY in .env)
            model_name (str): LLM model name (optional, defaults to LLaMA 3.3 70B Versatile)
            temperature (float): LLM sampling temperature (0-1). Low = deterministic.
        """
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Groq API key must be provided via parameter or GROQ_API_KEY in .env"
            )

        self.model_name = model_name or os.environ.get(
            "LLM_MODEL_NAME", "llama-3.3-70b-versatile"
        )
        self.temperature = temperature
        self.client = Groq(api_key=self.api_key)

    def generate(self, query, retrieved_docs):
        """
        Generate an answer:
          - Focused on the medicine in the query if applicable
          - Uses retrieved CSV documents
          - Provides comparison with alternatives
          - Handles general queries if query is not medicine-related
        """
        context = "\n\n".join(retrieved_docs)

        system_message = (
            "You are a medical assistant. "
            "The user may ask about a specific medicine or general queries. "
            "If the question is about a medicine, use the provided context from CSV data "
            "including description, side effects, interactions, manufacturer, and composition. "
            "Provide comparison with alternative medicines mentioned in the context if relevant. "
            "If the question is general (like greetings, non-medical), respond appropriately but briefly. "
            "Be concise, factual, and polite."
        )

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query},
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature  # Low-medium for deterministic responses
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error calling Groq LLM API: {e}"
