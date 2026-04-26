import sqlite3
import pandas as pd

def createAccountsTable(db:sqlite3.Cursor):
    createAccounts = (
        'CREATE TABLE IF NOT EXISTS accounts ('
        'name TEXT UNIQUE)'
    )

    db.execute(createAccounts)
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
