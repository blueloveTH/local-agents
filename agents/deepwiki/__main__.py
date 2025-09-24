from agents.common.models import get_model
from agents.deepwiki.index_build import IndexBuilder
from agents.deepwiki.overview_gen import gen_overview

model = get_model('ollama')

# builder = IndexBuilder("G:\\repos\\brogue-rpg\\backend", './tmp/backend')
# builder()

overview = gen_overview(model, './tmp/backend')
with open('./tmp/overview.md', 'w', encoding='utf-8') as f:
    f.write(overview)


