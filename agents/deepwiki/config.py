from dataclasses import dataclass
from agents.common.models import Model
import os

COMMON_SYSTEM_PROMPT = [
    '你是一个分析代码的专家。',
    '现在你正在执行一项重要任务，给用户的代码仓库生成一个准确且全面的wiki文档。',
]

@dataclass
class Context:
    model: Model
    source_dir: str
    output_dir: str

    @property
    def overview_path(self):
        return os.path.join(self.output_dir, 'overview.md')
    
    @property
    def log_path(self):
        return os.path.join(self.output_dir, 'main.log')
    
    @property
    def wiki_root(self):
        return os.path.join(self.output_dir, 'wiki')
    
    @property
    def index_root(self):
        return os.path.join(self.output_dir, 'index')

