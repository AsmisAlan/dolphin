from typing import Any
from common.object_mapper import mapper
from modules.natural_language.openia_chat_gpt.domain.chat_gpt_data import ChatGPTInput, ChatGPTOutput
from modules.search_engine.duck_duck_go.domain.duck_duk_go_data import DuckDuckGoOutput
from modules.web_scrapping.beautiful_soup.domain.beautiful_soup_data import BeautifulSoupOutput
import json


# Creates basics mappings
mapper.add(str, ChatGPTInput, lambda source: ChatGPTInput(content=source))

# Chat gpt mappers
mapper.add(ChatGPTOutput, ChatGPTInput,
           lambda source: ChatGPTInput(content=source['content']))

# Duck duck go mappers
mapper.add(DuckDuckGoOutput, ChatGPTInput, lambda source: ChatGPTInput(
    content=json.dumps(source.__dict__)))


# beautiful soup mappers
def map_bf_output_to_chat_gpt_input(source: BeautifulSoupOutput) -> ChatGPTInput:
    content = ""
    for l in source.urlsContent:
        content += f'{l[1]} \n'

    return ChatGPTInput(content=content)


mapper.add(BeautifulSoupOutput, ChatGPTInput, map_bf_output_to_chat_gpt_input)


def map_to_chat_gpt_input(input: Any) -> ChatGPTInput:
    return mapper.map(ChatGPTInput, input)
