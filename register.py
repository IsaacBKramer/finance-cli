import pandas as pd
import sqlite3

class Register:
    index = 0

    def __init__(self):
        self.connection = sqlite3.connect('transactions.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS transactions (id integer, year integer, month integer, day integer, value real, account text)')

    def addTransaction(self):
        date = input("Date YYYYMMDD: ")
        year = int(date[0:4])
        month = int(date[4:6])
        day = int(date[6:])
        value = float(input("Value: "))
        account = str(input("Account Name: "))
        self.cursor.execute('SELECT COUNT(*) FROM transactions')
        length = self.cursor.fetchone()[0]
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
        command = int(input("(1)date (2)value (3)account"))
        if command == 1:
            date = int(input("Date YYYYMMDD: "))
            year = int(date[0:4])
            month = int(date[4:6])
            day = int(date[6:])
            set = f'SET year = {year}'
            set = f'SET month = {month}'
            set = f'SET day = {day}'
        elif command == 2:
            value = float(input("Value: "))
            set = f'SET value = {value}'
        elif command == 3:
            account = int(input("Account Name: "))
            set = f'SET account = {account}'
        else:
            return
        sql = f'UPDATE transactions {set} WHERE id = {id}'
        self.cursor.execute(sql)
        self.connection.commit()

    def viewTransactions(self):
        print(pd.read_sql_query("SELECT * FROM transactions", self.connection))

    def viewAnnualTotal(self):
        totals = {}
        self.cursor.execute('SELECT DISTINCT year FROM transactions')
        years = self.cursor.fetchall()
        years = [row[0] for row in years]
        for year in years:
            self.cursor.execute(f'SELECT SUM(value) FROM transactions WHERE year <= {year}')
            total = self.cursor.fetchone()
            totals[year] = total[0]
        print(totals)