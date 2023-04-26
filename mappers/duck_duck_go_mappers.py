from typing import Any
from common.object_mapper import mapper
from modules.natural_language.openia_chat_gpt.domain.chat_gpt_data import ChatGPTOutput
from modules.search_engine.duck_duck_go.domain.duck_duk_go_data import DuckDuckGoInput

# Creates basics mappings
mapper.add(DuckDuckGoInput, DuckDuckGoInput, lambda source: source)
mapper.add(ChatGPTOutput, DuckDuckGoInput,
           lambda source: DuckDuckGoInput(query=source.content))
mapper.add(str, DuckDuckGoInput, lambda source: DuckDuckGoInput(query=source))
mapper.add(int, DuckDuckGoInput, lambda source: DuckDuckGoInput(query=source))


def map_to_duck_duck_go_input(input: Any) -> DuckDuckGoInput:
    return mapper.map(DuckDuckGoInput, input)
