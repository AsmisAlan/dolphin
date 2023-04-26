from typing import TypedDict


class DuckDuckGoConfiguration(TypedDict):
    '''Configuration for ddg search operator'''
    max_results: str
    output: str
