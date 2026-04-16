import yfinance as yf
import sqlite3

vtsax = yf.Ticker("VTSAX")
history = vtsax.history(period='1mo')
print(history)


def createInvestmentsTable(db):

    createInvestments = (
        'CREATE TABLE IF NOT EXISTS investments ('
        'id INTEGER PRIMARY KEY NOT NULL,'
        'year INTEGER NOT NULL,'
        'month INTEGER NOT NULL,'
        'day INTEGER NOT NULL,'
        'ticker TEXT NOT NULL'
        'value REAL NOT NULL,'
        'shares REAL NOT NULL'
        ')'
    )

    db.execute(createInvestments)

def addInvestment(db, year:int, month:int, day:int, ticker:str, value:float, shares:float):
    sql = 'INSERT INTO investments (year, month, day, ticker, value, shares) VALUES (?,?,?,?,?,?)'
    values = (year, month, day, ticker.strip(), value, shares)
    db.execute(sql, values)
