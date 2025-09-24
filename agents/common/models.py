import os
import re
from typing import Literal
from langchain.chat_models import init_chat_model

ModelProvider = Literal['openai', 'ollama']

def remove_think_tags(text: str) -> str:
    text = re.sub(r"<think>.*?</think>\n?", "", text, flags=re.DOTALL)
    return text.strip()

class Model:
    def __init__(self, model: str, model_provider: ModelProvider):
        self.model = init_chat_model(model=model, model_provider=model_provider)

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
