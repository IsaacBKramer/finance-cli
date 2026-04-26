import sys
import accounts
import register
import investments
import csvreader
import database
from pathlib import Path

def startup():
    db = database.create('database.db')
    cur = database.cursor(db)
    accounts.createAccountsTable(cur)
    register.createTransactionsTable(cur)
    investments.createInvestmentsTable(cur)
    print('\n########## WELCOME TO FINANCE-CLI ##########\n')
    print('Follow the prompts or type "exit" at any time to terminate the program.\n')
    return db, cur

def shutdown(db):
    database.shutdown(db)
    print('goodbye')
    sys.exit(0)

def readDate():
    while True:
        dateStr = input("Date YYYYMMDD: ")
        if len(dateStr) != 8:
            print("incorrect date format")
            continue
        try:
            year = int(dateStr[0:4])
        except ValueError:
            print(f"unexpected value for year {year}")
            continue
        try:
            month = int(dateStr[4:6])
        except ValueError:
            print(f"unexpected value for month {month}")
            continue    
        if month < 1 or month > 12:
            print(f"unexpected value for month {month}")
            continue
        try:
            day = int(dateStr[6:])
        except ValueError:
            print(f"unexpected value for day {day}")
            continue
        if day < 1 or day > 31:
            print(f"unexpected value for day {day}")
            continue
        return (year,month,day)

if __name__ == "__main__":
    db, cur = startup()
    while True:
        command = input("transactions investments accounts totals exit: ").lower()
        if command == 'transactions':
            while True:
                command = input("add delete modify view exit: ").lower()
                if command =='add':
                    command = input("manual csv: ").lower()
                    if command == 'manual':
                        date = readDate()
                        value = float(input("Value: "))
                        account = str(input("Account Name: "))
                        category = str(input("Category: "))
                        tag = str(input("Tag: "))
                        register.addTransaction(cur, date[0],date[1],date[2],value,account,category,tag)
                    elif command == 'csv': 
                        type = input("default quicken: ").lower()
                        account = input("account name: ")
                        file = input("filename: ")
                        file = Path(file)
                        if file.is_file():
                            if type == 'default':
                                df = csvreader.readDefaultCsv(file)
                                register.addTransactionsFromDf(cur, df)
                            elif type == 'quicken':
                                df = csvreader.readQuickenCsv(file, account)
                                register.addTransactionsFromDf(cur, df)
                            else:
                                continue
                        else:
                            print(f'file {file} does not exist')
                    else: 
                        continue
                elif command == 'delete':
                    id = int(input("id: "))
                    register.deleteTransaction(cur, id)
                elif command == 'modify':
                    id = int(input("id: "))
                    command = input("date value account category tag exit: ").lower()
                    if command == 'date':
                        register.modifyTransactionDate(cur, id, readDate())
                    elif command == 'value':
                        value = float(input("Value: "))
                        register.modifyTransactionValue(cur, id, value)
                    elif command == 'account':
                        account = str(input("Account Name: "))
                        register.modifyTransactionAccount(cur, id, account)
                    elif command == 'category':
                        category = str(input("Category: "))
                        register.modifyTransactionCategory(cur, id, category)
                    elif command == 'tag':
                        tag = str(input("Tag: "))
                        register.modifyTransactionTag(cur, id, tag)
                    elif command == 'exit':
                        break
                    else:
                        print("invalid input")
                        continue
                elif command == 'view':
                    register.viewTransactions(db)
                elif command == 'exit':
                    break
                else:
                    print('invalid input')
                    continue
        elif command == 'investments':
            while True:
                command = input("add view exit: ").lower()
                if command == 'add':
                    date = readDate()
                    ticker = input("Ticker: ").upper()
                    shares = float(input("Shares: "))
                    cost = float(input("Cost: "))
                    investments.addInvestment(cur,date[0],date[1],date[2],ticker,cost,shares)
                elif command == 'view':
                    command = input("security lots exit: ").lower()
                    if command == 'security':
                        investments.currentValue(cur)
                    elif command == 'lots':
                        df = investments.getLots(cur)
                        if df is not None: print(investments.getLots(cur))
                    elif command == 'exit':
                        break
                    else:
                        print('invalid input')
                        continue
                elif command == 'exit':
                    break
                else:
                    print('invalid input')
                    continue
        elif command == 'accounts':
            while True:
                command = input("add view exit: ").lower()
                if command == 'add':
                    accountName = input("account name: ")
                    accounts.addAccount(cur, accountName)
                elif command == 'view':
                    accounts.viewAccounts(db)
                elif command == 'exit':
                    break
                else:
                    print('invalid input')
                    continue
        elif command == 'totals':
            command = input("year month account: ").lower()
            if command == 'year':
                register.viewAnnualTotals(cur)
                # plotting.plotAnnualTotals(register)
            elif command == 'month':
                register.viewMonthlyTotals(cur)
            elif command == 'account':
                print(register.getAccountTotals(cur))
        elif command == 'exit':
            shutdown(db)
        else: 
            continue