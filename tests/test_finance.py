import pytest
import finance.database as dat
import finance.register as reg
import finance.investments as inv

@pytest.fixture(scope="module")
def database():
    db = dat.create('test.db')
    cursor = dat.cursor(db)
    yield cursor
    db.commit()
    db.close()

def test_tables(database):
    assert reg.createTransactionsTable(database) == True
    assert inv.createInvestmentsTable(database) == True

def test_accounts(database):
    assert reg.addAccount(database, 'SAVINGS') == True

def test_valid_transaction(database):
    assert reg.addTransaction(database, 2026, 4, 25, 100.00, 'SAVINGS', 'INCOME', 'NONE') == True
    totals = reg.getAccountTotals(database)
    series = totals.loc[totals['account'] == 'SAVINGS', 'total']
    assert len(series) == 1
    assert series.iloc[0] == 100.00

def test_invalid_transaction(database):
    assert reg.addTransaction(database, 2026, 4, 25, 100.00, 'CHECKING', 'INCOME', 'NONE') == False

def test_investments(database):
    assert inv.addInvestment(database, 2026, 4, 25, 'VTSAX', 500, 1.0) == True
    assert inv.addInvestment(database, 2026, 4, 25, 'FXAIX', 1000, 2.0) == True

    totals = inv.getInvestments(database)

    series = totals.loc[totals['Ticker'] == 'VTSAX', 'Shares']
    assert len(series) == 1
    assert series.iloc[0] == 1.0

    series = totals.loc[totals['Ticker'] == 'FXAIX', 'Shares']
    assert len(series) == 1
    assert series.iloc[0] == 2.0
