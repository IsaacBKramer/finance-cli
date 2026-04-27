import pandas as pd
import sqlite3


def createTransactionsTable(db:sqlite3.Cursor):
    
    createAccounts = (
        'CREATE TABLE IF NOT EXISTS accounts ('
        'name TEXT UNIQUE)'
    )
    createTransactions = (
        'CREATE TABLE IF NOT EXISTS transactions ('
        'id INTEGER PRIMARY KEY NOT NULL,'
        'year INTEGER NOT NULL,'
        'month INTEGER NOT NULL,'
        'day INTEGER NOT NULL,'
        'value REAL NOT NULL,'
        'account TEXT,'
        'category TEXT,'
        'tag TEXT,'
        'FOREIGN KEY (account) REFERENCES accounts(name)'
        ')'
    )

    db.execute(createAccounts)
    db.execute(createTransactions)
    db.execute("PRAGMA foreign_keys = ON")
    return True

def addAccount(db:sqlite3.Cursor, account:str):
    sql = 'INSERT INTO accounts (name) VALUES (?)'
    values = (account.strip(),)
    db.execute(sql, values)
    return True

def viewAccounts(db:sqlite3.Connection):
    df = pd.read_sql_query("SELECT * FROM accounts", db)
    print(df.to_markdown(index=False))

def addTransaction(db:sqlite3.Cursor, year:int, month:int, day:int, value:float, account:str, category:str, tag:str):
    sql = 'INSERT INTO transactions (year, month, day, value, account, category, tag) VALUES (?,?,?,?,?,?,?)'
    values = (year, month, day, value, account.strip(), category, tag)
    try:
        db.execute(sql, values)
    except sqlite3.IntegrityError as e:
        print(f"\nINVALID ACCOUNT NAME, TRANSACTION NOT ADDED")
        return False
    return True

def deleteTransaction(db:sqlite3.Cursor, id:int):
    sql = f'DELETE FROM transactions WHERE id={id}'
    db.execute(sql)
    return True

def modifyTransactionDate(db:sqlite3.Cursor, id:int, date):
    sql = f'UPDATE transactions SET year=? SET month=? SET day=? WHERE id=?'
    db.execute(sql,(date[0],date[1],date[2],id))
    return True

def modifyTransactionValue(db:sqlite3.Cursor, id:int, value:float):
    sql = f'UPDATE transactions SET value=? WHERE id=?'
    db.execute(sql,(value,id))
    return True

def modifyTransactionAccount(db:sqlite3.Cursor, id:int, account:str):
    sql = f'UPDATE transactions SET account=? WHERE id=?'
    try:
        db.execute(sql,(account.strip(),id))
    except sqlite3.IntegrityError as e:
        print(f"\n INVALID ACCOUNT NAME, TRANSACTION NOT MODIFIED, {e}")
        return False
    return True

def modifyTransactionCategory(db:sqlite3.Cursor, id:int, category:str):
    sql = f'UPDATE transactions SET category=? WHERE id=?'
    db.execute(sql,(category,id))
    return True

def modifyTransactionTag(db:sqlite3.Cursor, id:int, tag:str):
    sql = f'UPDATE transactions SET tag=? WHERE id=?'
    db.execute(sql,(tag,id))
    return True

def viewTransactions(db:sqlite3.Connection):
    df = pd.read_sql_query("SELECT * FROM transactions ORDER BY year ASC, month ASC, day ASC", db)
    print(df.to_markdown(index=False))

def getAnnualTotals(db:sqlite3.Cursor):
    db.execute('SELECT DISTINCT year FROM transactions')
    years = db.fetchall()
    years = [row[0] for row in years]
    totals = []
    for year in years:
        db.execute(f'SELECT SUM(value) FROM transactions WHERE year <= {year}')
        total = db.fetchone()
        totals.append(total[0])
    annualTotals = {'year' : years, 'total' : totals}
    return pd.DataFrame(annualTotals)

def getMonthlyTotals(db:sqlite3.Cursor):
    sql = 'WITH MonthlyTotals AS (SELECT year,month,SUM(value) AS total FROM transactions GROUP BY year,month) SELECT year,month,SUM(total) OVER(ORDER BY year ASC, month ASC) FROM MonthlyTotals'
    db.execute(sql)
    data = db.fetchall()
    years = [row[0] for row in data]
    months = [row[1] for row in data]
    totals = [row[2] for row in data]
    monthlyTotals = {'year' : years, 'month' : months, 'total' : totals}
    return pd.DataFrame(monthlyTotals)

def viewAnnualTotals(db:sqlite3.Cursor):
    df = getAnnualTotals(db)
    print(df.to_markdown(index=False))

def viewMonthlyTotals(db:sqlite3.Cursor):
    df = getMonthlyTotals(db)
    print(df.to_markdown(index=False))

def getAccountTotals(db:sqlite3.Cursor):
    totals = {}
    db.execute('SELECT DISTINCT account FROM transactions')
    accounts = db.fetchall()
    accounts = [row[0] for row in accounts]
    for account in accounts:
        db.execute(f'SELECT SUM(value) FROM transactions WHERE account = "{account}"')
        total = db.fetchone()
        totals[account] = total[0]
    return totals

def addTransactionsFromDf(db:sqlite3.Cursor, df):
    for index,row in df.iterrows():
        sql = 'INSERT INTO transactions (year, month, day, value, account, category, tag) VALUES (?,?,?,?,?,?,?)'
        values = (row['year'], row['month'], row['day'], row['value'], row['account'], row['category'], row['tag'])
        db.execute(sql, values)
