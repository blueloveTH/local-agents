import re
import os

from loguru import logger
from agents.common.utils import msg, read_file

from .config import Context

class Chatbot:
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.messages = [
            msg('system', [
                '你是一个分析代码的专家，你正在协助用户调研和理解一个代码库。',
                '用户会向你提供代码库的结构，请遵循用户的引导，帮助用户理解代码库的内容。',
                ]),
            msg('user', [
                '你好，代码库的目录结构如下：',
                read_file(ctx.overview_path),
                '',
                '我会就代码库的内容向你提问。',
                '',
                '当我提问后，请严谨和准确地回答我的问题，不要仅通过目录来猜测。',
                '如果你希望阅读某个代码文件，请简单回复「我需要查看`<文件相对根目录的全路径>`」，例如「我需要查看`test/main.py`」，不要解释理由，我会直接告诉你对应代码文件的内容。请注意，你一次只能查看一个文件。',
                '',
                '当我提问后，为了确保你回答的严谨和准确性，请至少通过回复「我需要查看`<文件相对根目录的全路径>`」查看3个相关代码文件之后，再给出最终回答。',
                '如果你的回答依据了某个代码文件，请指出依据文件的路径。',
                # 添加搜索关键词的指令
            ]),
        ]
        resp = self.ctx.model.stream(self.messages)
        self.messages.append(msg('ai', resp))
        
    def __call__(self, user_input: str):
        self.messages.append(msg('user', user_input))
        while True:
            resp = self.ctx.model.stream(self.messages)
            self.messages.append(msg('ai', resp))
            cat_match = re.search(r'我需要查看`([a-zA-Z0-9_\-./]+)`', resp)
            if not cat_match:
                break
            file_path = cat_match.group(1)

            optional_base = self.ctx.source_dir.split('/')[-1] + '/'
            if file_path.startswith(optional_base):
                file_path = file_path[len(optional_base):]
            try:
                file_content = read_file(os.path.join(self.ctx.source_dir, file_path))
                logger.info(f'正在将文件`{file_path}`的内容发送给AI...')
            except FileNotFoundError:
                file_content = f'文件 `{file_path}` 未找到，请检查路径是否正确。请注意，路径需要是相对于仓库根目录的全路径，而不是部分路径。'
                logger.warning(file_content)
            self.messages.append(msg('user', f'```\n{file_content}\n```'))
