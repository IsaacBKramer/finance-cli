import sqlite3

def create(name:str) -> sqlite3.Connection:
    """create a connection to a sqlite3 database"""
    return sqlite3.connect(name)

def cursor(db:sqlite3.Connection) -> sqlite3.Cursor:
    """create a database cursor from a database connection"""
    return db.cursor()

def shutdown(db:sqlite3.Connection) -> None:
    """commit and close a database"""
    db.commit()
    db.close()
