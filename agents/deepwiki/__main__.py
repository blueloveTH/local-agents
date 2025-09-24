from agents.common.models import Model
from agents.deepwiki.index_build import IndexBuilder
from agents.deepwiki.overview_gen import gen_overview

# qwen3-coder:30b-a3b-q8_0
# qwen3:30b-a3b-thinking-2507-q8_0
# qwen3:30b-a3b-instruct-2507-q8_0

# deepseek-r1:32b-qwen-distill-q8_0
# deepseek-r1:32b-qwen-distill-q4_k_m

# huggingface.co/Intel/Qwen3-Next-80B-A3B-Thinking-int4-mixed-AutoRound
model = Model('qwen3:30b-a3b-thinking-2507-q8_0', 'ollama')

# builder = IndexBuilder("G:\\repos\\brogue-rpg\\backend", './tmp/backend')
# builder()

overview = gen_overview(model, './tmp/backend')
with open('./tmp/overview.md', 'w', encoding='utf-8') as f:
    f.write(overview)
