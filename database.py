import sqlite3

def create(name:str):
    return sqlite3.connect(name)

def cursor(db:sqlite3.Connection):
    return db.cursor()

def shutdown(db:sqlite3.Connection):
    db.commit()
    db.close()