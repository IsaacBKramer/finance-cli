import finance.database
import finance.register
import finance.investments

def test_database():
    db = finance.database.create('test.db')
    db.commit()
    db.close()

def test_tables():
    db = finance.database.create('test.db')
    cursor = finance.database.cursor(db)
    finance.register.createTransactionsTable(cursor)
    finance.investments.createInvestmentsTable(cursor)
    db.commit()
    db.close()

def test_transactions():
    finance.register.addTransaction()