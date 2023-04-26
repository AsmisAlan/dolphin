from typing import List


class DuckDuckGoInput():
    '''Input for the ddg search operator'''

    def __init__(self, query: str):
        self.query = query


class Page():
    """Page object gathered from the search engine"""

    def __init__(self, title, href, body) -> None:
        self.title = title
        self.href = href
        self.body = body


class DuckDuckGoOutput():
    '''Output for the ddg search operator'''

    def __init__(self, pages: List[Page]):
        self.pages = pages
