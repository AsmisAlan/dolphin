from typing import List, Tuple


class BeautifulSoupInput():
    def __init__(self, urls: List[str]):
        self.urls = urls


class BeautifulSoupOutput():
    def __init__(self, urlsContent: List[Tuple[str, str]]):
        self.urlsContent = urlsContent
