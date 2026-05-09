import sqlite3

def setEnforceAccounts(db:sqlite3.Cursor, setting:bool):
    if setting: 
        db.execute("PRAGMA foreign_keys = ON")
    else:
        db.execute("PRAGMA foreign_keys = OFF")

def checkEnforceAccounts(db:sqlite3.Cursor):
    sql = 'PRAGMA foreign_keys'
    db.execute(sql)
    row = db.fetchone()
    if row is None:
        return False
    status = bool(row[0])
    return status