import sys
import sqlite3
import pandas as pd


class Register:
    index = 0

    def __init__(self):
        self.connection = sqlite3.connect('transactions.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS transactions (id integer, year integer, month integer, day integer, value real, account text)')

    def addTransaction(self):
        year = int(input("Year: "))
        month = int(input("Month: "))
        day = int(input("Day: "))
        value = float(input("Value: "))
        account = str(input("Account Name: "))
        self.cursor.execute('SELECT COUNT(*) FROM transactions')
        length = self.cursor.fetchone()[0]
        print(f"current table length is {length}")
        if length != 0:
            self.cursor.execute("SELECT MAX(id) from transactions")
            self.index = self.cursor.fetchone()[0] + 1
        sql = 'INSERT INTO transactions (id, year, month, day, value, account) VALUES (?,?,?,?,?,?)'
        values = (self.index, year, month, day, value, account)
        self.cursor.execute(sql, values)
        self.connection.commit()
        self.index = self.index + 1
    
    def deleteTransaction(self):
        id = int(input("id: "))
        sql = f'DELETE FROM transactions WHERE id={id}'
        self.cursor.execute(sql)
        self.connection.commit()

    def modifyTransaction(self):
        id = int(input("id: "))
        command = int(input("(1)year (2)month (3)day (4)value (5)account"))
        if command == 1:
            year = int(input("Year: "))
            set = f'SET year = {year}'
        elif command == 2:
            month = int(input("Month: "))
            set = f'SET month = {month}'
        elif command == 3:
            day = int(input("Day: "))
            set = f'SET day = {day}'
        elif command == 4:
            value = float(input("Value: "))
            set = f'SET value = {value}'
        elif command == 5:
            account = int(input("Account Name: "))
            set = f'SET account = {account}'
        else:
            return
        sql = f'UPDATE transactions {set} WHERE id = {id}'
        self.cursor.execute(sql)
        self.connection.commit()

    def viewTransactions(self):
        print(pd.read_sql_query("SELECT * FROM transactions", self.connection))

if __name__ == "__main__":
    register = Register()
    while True:
        command = int(input("(1)add (2)delete (3)modify (4)view (5)exit: "))
        if command == 1:
            register.addTransaction()
        elif command == 2:
            register.deleteTransaction()
        elif command == 3:
            register.modifyTransaction()
        elif command == 4:
            register.viewTransactions()
        elif command == 5:
            register.connection.commit()
            register.connection.close()
            sys.exit(0)
        else: 
            continue
        

