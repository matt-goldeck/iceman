import openai

from llms.base import BaseLLMAgent, LLMInput
from services.constants import LLMModel
from settings import settings


class OpenAIAgent(BaseLLMAgent):
    def __init__(self, model: LLMModel, temperature: float = 0.7, *args, **kwargs):
        super().__init__(model, temperature, *args, **kwargs)

        api_key = kwargs.get("api_key", settings.OPEN_AI_API_KEY)
        self.client = openai.OpenAI(api_key=api_key)

    def get_response(self, input: list[LLMInput]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[i.model_dump() for i in input],
            temperature=self.temperature,
        )

        return response.choices[0].message.content
