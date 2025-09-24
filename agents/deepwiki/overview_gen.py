from agents.common.utils import msg, read_file, write_file
from agents.common.utils import file_tree_to_markdown
from langchain.chat_models.base import BaseChatModel

from langchain_core.prompts import ChatPromptTemplate
from .config import COMMON_SYSTEM_PROMPT

prompt_template = ChatPromptTemplate.from_messages(
    [
        msg('system', COMMON_SYSTEM_PROMPT + [
            '用户已经对仓库的每个源文件进行了简要分析的总结。',
            '请根据这些总结，设计出wiki包含的页面、子页面和每个页面的目录结构。',
            '这些页面和目录结构要尽可能全面且准确地反映代码仓库的内容。',
            '你需要以markdown格式，输出每个页面的标题和页面包含的目录结构，以及涉及的主要文件（最多不超过5个，越相关的文件排在越前面）。',
            '页面不超过10个，目录最多有一级，不要包含子目录。',
            '每个页面要包含高层次，全局性质的概括性内容，不要单纯的翻译用户提供的总结内容。',
            '对于页面，请同时生成一个文件名作为合法的链接，文件名要符合标识符的命名规范，只能包含字母、数字和下划线，不能包含空格和其他特殊字符。',
            '输出示例:',
            '- [页面1标题](filename_page1.md)',
            '  - 主要文件',
            '    - filename1.py',
            '    - filename2.py',
            '  - 目录1',
            '  - 目录2',
            '- [页面2标题](filename_page2.md)',
            '  - 主要文件',
            '    - filename1.py',
            '    - filename2.py',
            '  - 目录1',
            '  - 目录2',
        ]),
        msg('user', [
            '代码仓库的文件结构如下：',
            '{file_tree}',
        ]),
        msg('ai', '好的，我已经了解了代码仓库的文件结构。请继续提供每个源文件的分析总结。'),
        msg('user', '{summaries}')
    ]
)

def gen_overview(model: BaseChatModel, index_root: str):
    md, files = file_tree_to_markdown(index_root, lambda x: x[:-3] if x.endswith('.md') else x)
    prompt_value = prompt_template.invoke({
        'file_tree': md,
        'summaries': '\n\n'.join(
            f'文件 `{file}` 的分析如下:\n```\n{read_file(f"{index_root}/{file}")}\n```'
            for file in files
        ),
    })
    write_file('./tmp/prompt.md', prompt_value.to_string())
    resp = model.stream(prompt_value.to_messages())
    data = []
    for chunk in resp:
        print(chunk.content, end='', flush=True)
        data.append(chunk.content)
    return ''.join(data)

