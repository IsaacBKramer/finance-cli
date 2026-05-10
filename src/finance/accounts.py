import sqlite3
import pandas as pd

def createAccountsTable(db:sqlite3.Cursor) -> bool:
    """create table in database for accounts"""
    createAccounts = (
        'CREATE TABLE IF NOT EXISTS accounts ('
        'name TEXT UNIQUE)'
    )

    db.execute(createAccounts)
    db.execute("PRAGMA foreign_keys = ON")

    return True

def addAccount(db:sqlite3.Cursor, account:str) -> bool:
    """add a new account to the accounts table in database"""
    sql = 'INSERT INTO accounts (name) VALUES (?)'
    values = (account.strip(),)
    db.execute(sql, values)
    return True

def getAccounts(db:sqlite3.Connection) -> pd.DataFrame:
    """view all accounts currently in accounts table in database"""
    return pd.read_sql_query("SELECT * FROM accounts", db)
