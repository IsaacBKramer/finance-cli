import sqlite3

def create(name:str) -> sqlite3.Connection:
    return sqlite3.connect(name)

def cursor(db:sqlite3.Connection) -> sqlite3.Cursor:
    return db.cursor()

def shutdown(db:sqlite3.Connection) -> None:
    db.commit()
    db.close()
