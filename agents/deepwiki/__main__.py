from agents.common.models import Model
from agents.common.utils import write_file
from agents.deepwiki.index_build import IndexBuilder
from agents.deepwiki.overview_gen import gen_overview
from datetime import datetime
import os

class Timer:
    def __init__(self):
        self.start_time = datetime.now()
        self.logs = []

    def record(self, title: str):
        now = datetime.now()
        elapsed = now - self.start_time
        elapsed_seconds = int(elapsed.total_seconds())
        minutes, seconds = divmod(elapsed_seconds, 60)
        self.logs.append(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {title}: {minutes}分钟{seconds}秒")
        self.start_time = now

    def save_logs(self, file_path: str):
        write_file(file_path, '\n'.join(self.logs))

timer = Timer()

# qwen3-coder:30b-a3b-q8_0
# qwen3:30b-a3b-thinking-2507-q8_0
# qwen3:30b-a3b-instruct-2507-q8_0

# deepseek-r1:32b-qwen-distill-q8_0
# deepseek-r1:32b-qwen-distill-q4_k_m

# huggingface.co/Intel/Qwen3-Next-80B-A3B-Thinking-int4-mixed-AutoRound
model = Model('qwen3:30b-a3b-thinking-2507-q8_0', 'ollama')

timer.record("初始化模型")

builder = IndexBuilder(model, "G:\\repos\\brogue-rpg\\backend", './tmp/backend')
builder()

timer.record("构建索引")

overview = gen_overview(model, './tmp/backend')
with open('./tmp/overview.md', 'w', encoding='utf-8') as f:
    f.write(overview)

timer.record("生成大纲")
timer.save_logs('./tmp/main.log')

# 让windows睡眠
os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
