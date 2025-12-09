from typing import List

from internal_types.Quote import Quote


def parse_quote_items(quote_data_parts: List[str]) -> Quote:
    raw_text = quote_data_parts[0]
    text = raw_text.strip().strip('“”')

    author = None
    if len(quote_data_parts) > 1:
        author_line = quote_data_parts[1].strip()
        if author_line.lower().startswith("by "):
            author_line = author_line[3:]
        if "(" in author_line:
            author_line = author_line.split("(")[0].strip()
        author = author_line

    tags = []
    if len(quote_data_parts) > 2:
        tags_line = quote_data_parts[2]
        if "Tags:" in tags_line:
            tags_line = tags_line.strip()[5:]
            tags_line = tags_line.strip().split(" ")
            tags = tags_line

    return Quote(text=text, author=author, tags=tags)
