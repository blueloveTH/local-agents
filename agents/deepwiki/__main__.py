from loguru import logger
import os, sys, time
from argparse import ArgumentParser

from agents.common.models import Model
from agents.common.utils import Timer, write_file

from .config import Context
from .index_build import IndexBuilder
from .overview_gen import gen_overview
from .chatbot import Chatbot

arg_parser = ArgumentParser()
arg_parser.add_argument('--output_dir', type=str, default='./tmp', help='输出目录')
arg_parser.add_argument('--sleep_on_end', action='store_false', help='在流程结束后让Windows进入睡眠')
args = arg_parser.parse_args()


os.environ['OPENAI_API_BASE'] = 'https://api.yuegle.com/v1'

timer = Timer()

ctx = Context(
    # qwen3:30b-a3b-thinking-2507-q4_k_m
    # model=Model('qwen3:4b-instruct-2507-q4_k_m', 'ollama'),
    model=Model('gemini-2.5-pro-cheap', 'openai'),
    source_dir="G:/repos/noita-data",
    output_dir=str(args.output_dir),
)

logger.add(ctx.log_path, rotation='1 MB')
logger.info('DeepWiki 生成流程启动！')

timer.record("初始化模型")

# builder = IndexBuilder(ctx)
# builder()

# timer.record("构建索引")

overview = gen_overview(ctx, with_index=False)

timer.record("生成大纲")

chatbot = Chatbot(ctx)

while True:
    text = input('>>> ').strip()
    if text:
        chatbot(text)

logger.info("DeepWiki 生成流程结束！")
# time.sleep(5)

# # 让windows睡眠
# if sys.platform == 'win32' and args.sleep_on_end:
#     os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


# noita-data中的法术增强的状态是怎么实现的？例如一个魔法弹加上冰霜晶石，可以给魔法弹增加冰系伤害和减速效果。