from extractor import extract_quote_data_from_page_range
from storage import create_table, insert_into_db, select_all, select_quotes_per_author


def test_db():
    create_table()
    quotes = extract_quote_data_from_page_range(first_page=1, last_page=1)
    for quote in quotes:
        insert_into_db(quote)
    print(select_all())
    print(select_quotes_per_author())

if __name__ == '__main__':
    test_db()