from enum import Enum
from pydantic import BaseModel

from services.constants import LLMModel


class LLMRole(str, Enum):
    system = "system"
    user = "user"


class LLMInput(BaseModel):
    role: LLMRole
    content: str


class BaseLLMAgent:
    def __init__(self, model: LLMModel, temperature: float, *args, **kwargs):
        self.model = model
        self.temperature = temperature

    def get_response(self, input: list[LLMInput]) -> dict:
        """
        Call the LLM with the given input and return a response
        """
        raise NotImplementedError("Subclasses must implement this method.")
