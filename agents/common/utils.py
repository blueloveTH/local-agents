import os
from typing import Literal, Callable

def msg(role: Literal['system', 'user', 'ai'], content: str | list[str]):
    if isinstance(content, str):
        content = [content]
    return (role, '\n'.join(content))

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


class MirrorProcessor:
    def __init__(self, src_dir, dst_dir):
        self.src_dir = os.path.abspath(src_dir)
        self.dst_dir = os.path.abspath(dst_dir)

    def __call__(self):
        for root, dirs, files in os.walk(self.src_dir):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, self.src_dir)
                dst_path = os.path.join(self.dst_dir, rel_path)

                if not self.filter(src_path):
                    continue
                res = self.process(src_path)
                if res is not None:
                    dst_path = dst_path + '.md'
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    write_file(dst_path, res)

    def filter(self, src_path) -> bool:
        raise NotImplementedError

    def process(self, src_path) -> str | None:
        raise NotImplementedError


def file_tree_to_markdown(root_path: str, f_process: Callable[[str], str] | None = None) -> tuple[str, list[str]]:
    f_process = f_process or (lambda x: x)
    files = []
    def _directory_to_markdown(path, indent=0):
        lines = []
        prefix = '  ' * indent
        for entry in sorted(os.listdir(path)):
            full_path = os.path.join(path, entry)
            entry = f_process(entry)
            if os.path.isdir(full_path):
                lines.append(f"{prefix}- `{entry}/`")
                lines.extend(_directory_to_markdown(full_path, indent + 1))
            else:
                lines.append(f"{prefix}- `{entry}`")
                files.append(os.path.relpath(full_path, root_path))
        return lines

    root_name = os.path.basename(os.path.abspath(root_path))
    lines = [f"- `{f_process(root_name)}/`"]
    lines.extend(_directory_to_markdown(root_path, indent=1))
    return (
        '\n'.join(lines),
        files
    )

