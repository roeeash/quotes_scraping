import sqlite3

import pytest
import storage
from internal_types.Quote import Quote


@pytest.fixture(scope="session")
def db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    storage.conn = conn
    storage.cursor = cursor

    storage.create_table()

    yield storage

    conn.close()


@pytest.fixture
def sample_quotes():
    return [
        Quote(text="Life is what happens to us while we are making other plans.",
              author="John Lennon",
              tags=["life", "planning"]),
        Quote(text="The journey of a thousand miles begins with one step.",
              author="Lao Tzu",
              tags=["inspirational", "journey"]),
        Quote(text="To be or not to be, that is the question.",
              author="William Shakespeare",
              tags=["classic", "philosophy"]),
        Quote(text="All the world's a stage.",
              author="William Shakespeare",
              tags=["classic", "life"])
    ]