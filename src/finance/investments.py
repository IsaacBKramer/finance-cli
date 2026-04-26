import yfinance as yf
import pandas as pd

def createInvestmentsTable(db):

    createInvestments = (
        'CREATE TABLE IF NOT EXISTS investments ('
        'id INTEGER PRIMARY KEY NOT NULL,'
        'year INTEGER NOT NULL,'
        'month INTEGER NOT NULL,'
        'day INTEGER NOT NULL,'
        'ticker TEXT NOT NULL,'
        'cost REAL NOT NULL,'
        'shares REAL NOT NULL'
        ')'
    )

    db.execute(createInvestments)
    return True

def addInvestment(db, year:int, month:int, day:int, ticker:str, value:float, shares:float):
    sql = 'INSERT INTO investments (year, month, day, ticker, cost, shares) VALUES (?,?,?,?,?,?)'
    values = (year, month, day, ticker.strip(), value, shares)
    db.execute(sql, values)
    return True

def getLots(db):
    sql = 'SELECT ticker, shares, cost FROM investments'
    db.execute(sql)
    lots = pd.DataFrame(db.fetchall(), columns=['Ticker','Shares','Basis'])
    if lots.empty: return None
    prices = downloadPrice(db)
    lots['Value'] = lots.apply(lambda row: row['Shares'] * prices.iloc[-1,prices.columns.get_loc(row['Ticker'])], axis=1)
    lots['PercentChange'] = (lots['Value']/lots['Basis']-1)*100
    return lots

def getInvestments(db):
    sql = 'SELECT ticker, SUM(shares) FROM investments GROUP BY ticker'
    db.execute(sql)
    return pd.DataFrame(db.fetchall(), columns=['Ticker','Shares'])

def getTickers(db):
    sql = 'SELECT DISTINCT ticker FROM investments'
    db.execute(sql)
    return [ticker[0] for ticker in db.fetchall()]

def downloadPrice(db):
    tickers = getTickers(db)
    if not tickers: return None
    data = yf.download(tickers, period='1mo')
    return data['Close']

def currentValue(db):
    prices = downloadPrice(db)
    if prices is None: return None
    investments = getInvestments(db)
    investments['Price'] = investments.apply(lambda row: prices.iloc[-1,prices.columns.get_loc(row['Ticker'])], axis=1)
    investments['Total'] = investments['Price'] * investments['Shares']
    print(investments)