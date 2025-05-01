from sqlalchemy import Enum


class LLMModel(str, Enum):
    pass


class OpenAIModel(LLMModel):
    """OpenAI models."""

    gpt_4_1_mini = "gpt-4.1-mini"
