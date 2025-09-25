import re
from dataclasses import dataclass
from datetime import datetime
from loguru import logger

@dataclass
class WikiPage:
    title: str
    filename: str
    related_files: list[str]
    table_of_contents: list[str]

def is_identifier(s: str) -> bool:
    return re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', s) is not None

def parse_overview(text: str):
    pattern = r'^- \[(.+?)\]\((.+?)\)'
    pages: list[WikiPage] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = re.match(pattern, lines[i])
        if m:
            title = m.group(1)
            filename = m.group(2)
            if not filename.endswith('.md'):
                logger.warning(f'{filename} is not end with .md, auto append it.')
                filename += '.md'
            if not is_identifier(filename[:-3]):
                logger.warning(f'{filename} is not a valid identifier.')
                filename = re.sub(r'[^A-Za-z0-9_]', '_', filename)
            pages.append(
                WikiPage(
                    title=title,
                    filename=filename,
                    related_files=[],
                    table_of_contents=[]
                    )
                )
            i += 1
            continue

        if lines[i].startswith('  - 主要文件'):
            i += 1
            while lines[i].startswith('    - '):
                path = lines[i].lstrip(' -')
                path = path.strip(' `')
                pages[-1].related_files.append(path)
                i += 1
            continue

        if lines[i].startswith('  - '):
            content = lines[i].lstrip(' -').strip()
            pages[-1].table_of_contents.append(content)
            i += 1
            continue

        i += 1
    return pages

