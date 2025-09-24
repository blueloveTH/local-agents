from agents.common.models import get_model
from agents.common.utils import msg, read_file
from agents.common.utils import MirrorProcessor

from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate.from_messages(
    [
        msg('system', [
            '你是一个分析代码的专家。',
            '现在你正在执行一项重要任务，给用户的代码仓库生成一个准确且全面的wiki文档。',
            '在开始生成之前，用户会逐个向你提供代码仓库中的每一个源文件的内容，你需要从每个文件中提取关键信息，并以你认为合适的方式进行提炼和总结。',
            '你的总结将会被用户存储下来，用于后续指导「你自己」下一步生成整个代码仓库的wiki的过程。',
            '你的总结将被用于检索信息，回答用户后续的提问，因此你需要在总结中包含关键的函数、类或变量的名称和作用，以便检索。',
            '你的总结要尽可能简洁，不要复制用户的源代码，字数越少越好。',
            '现在用户会向你提供第一个源文件的内容，请你开始你的工作。',
        ]),
        msg('user', [
            '文件 `{file_path}` 的内容如下:',
            '```\n{source_code}\n```'
        ]),
    ]
)

def build_index(in_file: str) -> str:
    prompt_value = prompt_template.invoke({
        'file_path': in_file,
        'source_code': read_file(in_file),
    })

    model = get_model()
    resp = model.stream(prompt_value.to_messages())
    data = []
    for chunk in resp:
        print(chunk.content, end='', flush=True)
        data.append(chunk.content)
    return ''.join(data)


class IndexBuilder(MirrorProcessor):
    def filter(self, src_path) -> bool:
        return src_path.endswith('.py')

    def process(self, src_path):
        return build_index(src_path)