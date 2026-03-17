import pandas as pd
import sqlite3

class Register:

    def __init__(self):
        self.connection = sqlite3.connect('transactions.db')
        self.cursor = self.connection.cursor()
        createTable = 'CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY NOT NULL, year INTEGER, month INTEGER, day INTEGER, value REAL, account TEXT)'
        self.cursor.execute(createTable)

    def addTransaction(self):
        date = input("Date YYYYMMDD: ")
        year = int(date[0:4])
        month = int(date[4:6])
        day = int(date[6:])
        value = float(input("Value: "))
        account = str(input("Account Name: "))

        sql = 'INSERT INTO transactions (year, month, day, value, account) VALUES (?,?,?,?,?)'
        values = (year, month, day, value, account)
        self.cursor.execute(sql, values)
        self.connection.commit()
    
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
        df = pd.read_sql_query("SELECT * FROM transactions", self.connection)
        print(df.to_markdown(index=False))

    def getAnnualTotals(self):
        self.cursor.execute('SELECT DISTINCT year FROM transactions')
        years = self.cursor.fetchall()
        years = [row[0] for row in years]
        totals = []
        for year in years:
            self.cursor.execute(f'SELECT SUM(value) FROM transactions WHERE year <= {year}')
            total = self.cursor.fetchone()
            totals.append(total[0])
        annualTotals = {'year' : years, 'total' : totals}
        return pd.DataFrame(annualTotals)
    
    def viewAnnualTotals(self):
        df = self.getAnnualTotals()
        print(df.to_markdown(index=False))

    def viewAccountTotals(self):
        totals = {}
        self.cursor.execute('SELECT DISTINCT account FROM transactions')
        accounts = self.cursor.fetchall()
        accounts = [row[0] for row in accounts]
        for account in accounts:
            self.cursor.execute(f'SELECT SUM(value) FROM transactions WHERE account = "{account}"')
            total = self.cursor.fetchone()
            totals[account] = total[0]
        print(totals)
    
    def addTransactionsFromCsv(self, csvfile):
        df = pd.read_csv(csvfile)
        for index,row in df.iterrows():
            sql = 'INSERT INTO transactions (year, month, day, value, account) VALUES (?,?,?,?,?)'
            values = (row['year'], row['month'], row['day'], row['value'], row['account'])
            self.cursor.execute(sql, values)
        self.connection.commit()