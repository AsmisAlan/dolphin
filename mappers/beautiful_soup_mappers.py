from typing import Any
from common.object_mapper import mapper
from modules.search_engine.duck_duck_go.domain.duck_duk_go_data import DuckDuckGoOutput
from modules.web_scrapping.beautiful_soup.domain.beautiful_soup_data import BeautifulSoupInput

# Creates basics mappings
mapper.add(str, BeautifulSoupInput,
           lambda source: BeautifulSoupInput(urls=[source]))
mapper.add(DuckDuckGoOutput, BeautifulSoupInput, lambda source: BeautifulSoupInput(
    urls=map(lambda x: x['href'], source.pages)))


# From search engines mappers

def map_to_beautiful_soup_input(input: Any) -> BeautifulSoupInput:
    return mapper.map(BeautifulSoupInput, input)
