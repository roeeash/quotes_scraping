def test_insert_and_select_all(db, sample_quotes):
    for q in sample_quotes:
        db.insert_into_db(q)

    all_quotes = db.select_all()
    assert len(all_quotes) == len(sample_quotes)

def test_filter_by_author(db, sample_quotes):
    for q in sample_quotes:
        db.insert_into_db(q)

    shakespeare = db.get_filtered_items(author="William Shakespeare")
    assert len(shakespeare) == 2
    for row in shakespeare:
        assert "Shakespeare" in row[2]

def test_select_quotes_per_author(db, sample_quotes):
    for q in sample_quotes:
        db.insert_into_db(q)
    counts = db.select_quotes_per_author()
    assert any(author == "William Shakespeare" for author, _ in counts)

def test_select_count_all(db, sample_quotes):
    for q in sample_quotes:
        db.insert_into_db(q)

    assert db.select_count_all() == len(sample_quotes)

def test_select_quotes_per_tag(db, sample_quotes):
    for q in sample_quotes:
        db.insert_into_db(q)

    counts = db.select_quotes_per_tag()
    tags = [tag for tag, _ in counts]
    assert "life" in tags
    assert "classic" in tags