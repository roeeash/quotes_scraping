from typing import List


class Quote:
    def __init__(self, text: str, author: str, tags: List[str]):
        self.text = text
        self.author = author
        self.tags = tags