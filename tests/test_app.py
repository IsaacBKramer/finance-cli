import finance.database

def test_database():
    db = finance.database.create('test.db')
    db.commit()
    db.close()
    assert True