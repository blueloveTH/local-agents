from loguru import logger
import os, sys, time
from argparse import ArgumentParser

from agents.common.models import Model
from agents.common.utils import Timer, write_file

from .config import Context
from .index_build import IndexBuilder
from .overview_gen import gen_overview
from .page_gen import gen_page

arg_parser = ArgumentParser()
arg_parser.add_argument('--output_dir', type=str, default='./tmp', help='输出目录')
arg_parser.add_argument('--sleep_on_end', action='store_false', help='在流程结束后让Windows进入睡眠')
args = arg_parser.parse_args()

timer = Timer()

# qwen3-coder:30b-a3b-q8_0
# qwen3:30b-a3b-thinking-2507-q8_0
# qwen3:30b-a3b-instruct-2507-q8_0

# deepseek-r1:32b-qwen-distill-q8_0
# deepseek-r1:32b-qwen-distill-q4_k_m

# huggingface.co/Intel/Qwen3-Next-80B-A3B-Thinking-int4-mixed-AutoRound
ctx = Context(
    model=Model('qwen3:30b-a3b-thinking-2507-q8_0', 'ollama'),
    source_dir="G:\\repos\\brogue-rpg\\backend",
    output_dir=str(args.output_dir),
)

logger.add(ctx.log_path, rotation='1 MB')
logger.info('DeepWiki 生成流程启动！')

timer.record("初始化模型")

builder = IndexBuilder(ctx)
builder()

timer.record("构建索引")

gen_overview(ctx)

timer.record("生成大纲")

gen_page(ctx)

logger.info("DeepWiki 生成流程结束！")
time.sleep(5)

# 让windows睡眠
if sys.platform == 'win32' and args.sleep_on_end:
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
