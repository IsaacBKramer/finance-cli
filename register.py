import pandas as pd
import sqlite3

class Register:

    def __init__(self):
        self.connection = sqlite3.connect('transactions.db')
        self.cursor = self.connection.cursor()

        createAccounts = (
            'CREATE TABLE IF NOT EXISTS accounts ('
            'name TEXT UNIQUE)'
        )
        createTransactions = (
            'CREATE TABLE IF NOT EXISTS transactions ('
            'id INTEGER PRIMARY KEY NOT NULL,'
            'year INTEGER NOT NULL,'
            'month INTEGER NOT NULL,'
            'day INTEGER NOT NULL,'
            'value REAL NOT NULL,'
            'account TEXT,'
            'category TEXT,'
            'tag TEXT,'
            'FOREIGN KEY (account) REFERENCES accounts(name)'
            ')'
        )

        self.cursor.execute(createAccounts)
        self.cursor.execute(createTransactions)
        self.cursor.execute("PRAGMA foreign_keys = ON");

    def addAccount(self, account:str):
        sql = 'INSERT INTO accounts (name) VALUES (?)'
        values = (account.strip(),)
        self.cursor.execute(sql, values)
        self.connection.commit()
    
    def viewAccounts(self):
        df = pd.read_sql_query("SELECT * FROM accounts", self.connection)
        print(df.to_markdown(index=False))

    def addTransaction(self, year:int, month:int, day:int, value:float, account:str, category:str, tag:str):
        sql = 'INSERT INTO transactions (year, month, day, value, account, category, tag) VALUES (?,?,?,?,?,?,?)'
        values = (year, month, day, value, account.strip(), category, tag)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            print(f"\nINVALID ACCOUNT NAME, TRANSACTION NOT ADDED")
  
    def deleteTransaction(self, id:int):
        sql = f'DELETE FROM transactions WHERE id={id}'
        self.cursor.execute(sql)
        self.connection.commit()
    
    def modifyTransactionDate(self, id:int, date):
        sql = f'UPDATE transactions SET year=? SET month=? SET day=? WHERE id=?'
        self.cursor.execute(sql,(date[0],date[1],date[2],id))
        self.connection.commit()
    
    def modifyTransactionValue(self, id:int, value:float):
        sql = f'UPDATE transactions SET value=? WHERE id=?'
        self.cursor.execute(sql,(value,id))
        self.connection.commit()

    def modifyTransactionAccount(self, id:int, account:str):
        sql = f'UPDATE transactions SET account=? WHERE id=?'
        try:
            self.cursor.execute(sql,(account.strip(),id))
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            print(f"\n INVALID ACCOUNT NAME, TRANSACTION NOT MODIFIED, {e}")

    def modifyTransactionCategory(self, id:int, category:str):
        sql = f'UPDATE transactions SET category=? WHERE id=?'
        self.cursor.execute(sql,(category,id))
        self.connection.commit()

    def modifyTransactionTag(self, id:int, tag:str):
        sql = f'UPDATE transactions SET tag=? WHERE id=?'
        self.cursor.execute(sql,(tag,id))
        self.connection.commit()

    def viewTransactions(self):
        df = pd.read_sql_query("SELECT * FROM transactions ORDER BY year ASC, month ASC, day ASC", self.connection)
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
    
    def getMonthlyTotals(self):
        self.cursor.execute('SELECT DISTINCT year, month FROM transactions ORDER BY year ASC, month ASC')
        data = self.cursor.fetchall()
        years = [row[0] for row in data]
        months = [row[1] for row in data]
        totals = []
        for month in data:
            self.cursor.execute(f'SELECT SUM(value) FROM transactions WHERE year <= {month[0]} AND month <={month[1]}')
            total = self.cursor.fetchone()
            totals.append(total[0])
        annualTotals = {'year' : years, 'month' : months, 'total' : totals}
        return pd.DataFrame(annualTotals)
    
    def viewAnnualTotals(self):
        df = self.getAnnualTotals()
        print(df.to_markdown(index=False))
    
    def viewMonthlyTotals(self):
        df = self.getMonthlyTotals()
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
            sql = 'INSERT INTO transactions (year, month, day, value, account, category, tag) VALUES (?,?,?,?,?,?,?)'
            values = (row['year'], row['month'], row['day'], row['value'], row['account'], row['category'], row['tag'])
            self.cursor.execute(sql, values)
        self.connection.commit()