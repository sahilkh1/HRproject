# models.py
import os
from langchain.chat_models import ChatOpenAI

class ModelHandler:
    def __init__(self, api_key_env_var="OPENAI_API_KEY"):
        self.api_key = os.getenv(api_key_env_var)
        if not self.api_key:
            raise EnvironmentError(f"{api_key_env_var} not set in environment variables.")
        
        self.llm = self.initialize_llm()

    def initialize_llm(self) -> ChatOpenAI:
        """Initialize and return the OpenAI language model."""
        return ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=self.api_key)
