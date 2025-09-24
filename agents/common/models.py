import os
from typing import Literal
from langchain.chat_models import init_chat_model

ModelProvider = Literal['openai', 'ollama']

def get_model(provider: ModelProvider):
    if provider == 'ollama':
        model = init_chat_model('qwen3-coder:latest', model_provider='ollama')
    else:
        assert 'OPENAI_API_KEY' in os.environ
        model = init_chat_model('gemini-2.5-pro', model_provider='openai')
    return model
