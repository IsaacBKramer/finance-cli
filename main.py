import sys
from pathlib import Path
from register import Register
import csvreader
import plotting

def startup():
    register = Register()
    print('\n########## WELCOME TO FINANCE-CLI ##########\n')
    print('Follow the prompts or type "exit" at any time to terminate the program.\n')
    return register

def shutdown(register:Register):
    register.connection.commit()
    register.connection.close()
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
    register = startup()
    while True:
        command = input("transactions accounts totals exit: ").lower()
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
                        register.addTransaction(date[0],date[1],date[2],value,account,category,tag)
                    elif command == 'csv': 
                        type = input("default quicken: ").lower()
                        account = input("account name: ")
                        file = input("filename: ")
                        file = Path(file)
                        if file.is_file():
                            if type == 'default':
                                df = csvreader.readDefaultCsv(file, account)
                                register.addTransactionsFromDf(df)
                            elif type == 'quicken':
                                df = csvreader.readQuickenCsv(file, account)
                                register.addTransactionsFromDf(df)
                            else:
                                continue
                        else:
                            print(f'file {file} does not exist')
                    else: 
                        continue
                elif command == 'delete':
                    id = int(input("id: "))
                    register.deleteTransaction(id)
                elif command == 'modify':
                    id = int(input("id: "))
                    command = input("date value account category tag exit: ").lower()
                    if command == 'date':
                        register.modifyTransactionDate(id, readDate())
                    elif command == 'value':
                        value = float(input("Value: "))
                        register.modifyTransactionValue(id, value)
                    elif command == 'account':
                        account = str(input("Account Name: "))
                        register.modifyTransactionAccount(id, account)
                    elif command == 'category':
                        category = str(input("Category: "))
                        register.modifyTransactionCategory(id, category)
                    elif command == 'tag':
                        tag = str(input("Tag: "))
                        register.modifyTransactionTag(id, tag)
                    elif command == 'exit':
                        break
                    else:
                        print("invalid input")
                        continue
                elif command == 'view':
                    register.viewTransactions()
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
                    register.addAccount(accountName)
                elif command == 'view':
                    register.viewAccounts()
                elif command == 'exit':
                    break
                else:
                    print('invalid input')
                    continue
        elif command == 'totals':
            command = input("year month account: ").lower()
            if command == 'year':
                register.viewAnnualTotals()
                # plotting.plotAnnualTotals(register)
            elif command == 'month':
                register.viewMonthlyTotals()
            elif command == 'account':
                register.viewAccountTotals()
        elif command == 'exit':
            shutdown(register)
        else: 
            continue