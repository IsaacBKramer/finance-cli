import sqlite3
import pandas as pd

def createCategoriesTable(db:sqlite3.Cursor) -> bool:
    """create table in database for categories"""
    createCategories = (
        'CREATE TABLE IF NOT EXISTS categories ('
        'name TEXT UNIQUE)'
    )

    db.execute(createCategories)
    addDefaultCategories(db)
    db.execute("PRAGMA foreign_keys = ON")

    return True

def addCategory(db:sqlite3.Cursor, account:str) -> bool:
    """add a new category to the categories table"""
    sql = 'INSERT INTO categories (name) VALUES (?)'
    values = (account.strip(),)
    db.execute(sql, values)
    return True

def getCategories(db:sqlite3.Connection) -> pd.DataFrame:
    """view all categories currently in categories table"""
    return pd.read_sql_query("SELECT * FROM categories", db)

def addDefaultCategories(db:sqlite3.Cursor) -> bool:
    """add a list of standard categories to categories table"""
    categories = ["TRANSIT", "FOOD", "HOUSING", "INCOME", "UTILITIES"]
    sql = 'INSERT INTO categories (name) VALUES (?)'
    try:
        db.executemany(sql, [(item,) for item in categories])
    except sqlite3.IntegrityError:
        pass
    return True
