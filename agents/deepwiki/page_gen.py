from langchain_core.prompts import ChatPromptTemplate
import os, shutil
from loguru import logger

from agents.common.utils import msg, read_file, write_file
from agents.common.utils import file_tree_to_markdown
from agents.common.models import Model

from .config import COMMON_SYSTEM_PROMPT
from .utils import parse_overview

prompt_template = ChatPromptTemplate.from_messages(
    [
        msg('system', COMMON_SYSTEM_PROMPT + [
            '用户会依次向你提供如下信息，你需要根据这些信息为用户生成一个wiki页面。',
            '1. 代码仓库的文件结构',
            '2. wiki文档的大纲',
            '3. 当前需要生成的wiki页面的标题和文件名',
            '4. 该wiki页面涉及的主要源代码',
            '',
            '在获得这些信息后，你需要分析待生成的页面是哪一个，并从大纲中找到这个页面对应的目录结构和涉及的源代码路径。',
            '接着，你需要分析用户给出的源代码，进一步理解这些代码的功能和实现细节。',
            '结合以上这些内容，生成一个严谨、准确且内容全面的wiki页面。',
        ]),
        msg('user', [
            '# 代码仓库的文件结构',
            '{file_tree}',
            '',
            '# wiki文档的大纲如下',
            '{overview}',
            '',
            '# 当前需要生成的页面是',
            '- [{page_title}]({page_filename})',
            '{page_toc}',
            '',
            '# 该页面涉及的主要源代码',
            '{related_files}',
        ]),
    ]
)

def gen_page(model: Model, source_root: str, index_root: str):
    overview_path = os.path.join(index_root, 'overview.md')
    assert os.path.exists(overview_path)
    overview = read_file(overview_path)
    md, files = file_tree_to_markdown(index_root, lambda x: x[:-3] if x.endswith('.md') else x)
    
    output_dir = os.path.join(index_root, 'wiki')
    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir)

    for page in parse_overview(overview):
        logger.info(f'开始生成页面: {page.title} ({page.filename})')
        related_files = []
        for file in page.related_files:
            if file in files:
                related_files.extend([
                    '#### ' + file,
                    '```',
                    read_file(os.path.join(source_root, file)),
                    '```\n',
                ])
            else:
                logger.warning(f'page {page.title} is referring a missing file: {file}')
        prompt_value = prompt_template.invoke({
            'file_tree': md,
            'overview': overview,
            'page_title': page.title,
            'page_filename': page.filename,
            'page_toc': '\n'.join(f'  - {item}' for item in page.table_of_contents),
            'related_files': '\n'.join(related_files)
        })
        write_file(os.path.join(index_root, 'page_gen_prompt.md'), prompt_value.to_string())
        res = model.stream(prompt_value.to_messages())
        write_file(os.path.join(output_dir, page.filename), res)
