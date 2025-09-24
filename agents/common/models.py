import os
import re
from typing import Literal
from langchain.chat_models import init_chat_model

ModelProvider = Literal['openai', 'ollama']

def remove_think_tags(text: str) -> str:
    text = re.sub(r"<think>.*?</think>\n?", "", text, flags=re.DOTALL)
    return text.strip()

class Model:
    def __init__(self, provider: ModelProvider):
        if provider == 'ollama':
            self.model = init_chat_model('qwen3-coder:30b-a3b-q8_0', model_provider='ollama')
        else:
            assert 'OPENAI_API_KEY' in os.environ
            self.model = init_chat_model('gemini-2.5-pro', model_provider='openai')

    def stream(self, messages):
        data: list[str] = []
        for chunk in self.model.stream(messages):
            print(chunk.content, end='', flush=True)
            data.append(chunk.content)
        text = ''.join(data)
        return remove_think_tags(text)
    
    def invoke(self, prompt):
        resp = self.model.invoke(prompt)
        text = resp.content
        return remove_think_tags(text)
