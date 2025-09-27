import os

from agents.common.utils import msg, read_file, write_file
from agents.common.utils import file_tree_to_markdown

from .config import Context

def convert_title(entry: str, full_path: str):
    if entry.endswith('.md'):
        return '`{}`: {}'.format(entry[:-3], read_file(full_path).strip())
    return '`{}`'.format(entry)

def gen_overview(ctx: Context, with_index=True):
    if with_index:
        md, files = file_tree_to_markdown(ctx.index_root, convert_title)
    else:
        def f_filter(entry: str, full_path: str) -> bool:
            if os.path.isdir(full_path):
                return True
            return entry.endswith('.lua') #or entry.endswith('.xml')
        md, files = file_tree_to_markdown(
            ctx.source_dir,
            lambda entry, full_path: '`{}`'.format(entry) if f_filter(entry, full_path) else None,
            )
    write_file(os.path.join(ctx.output_dir, 'overview.md'), md)
