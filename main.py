import sys
from pathlib import Path
from register import Register
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

if __name__ == "__main__":
    register = startup()
    while True:
        command = input("transactions accounts totals exit: ")
        if command == 'transactions':
            while True:
                command = input("add delete modify view exit: ")
                if command =='add':
                    command = input("manual csv: ")
                    if command == 'manual':
                        date = input("Date YYYYMMDD: ")
                        year = int(date[0:4])
                        month = int(date[4:6])
                        day = int(date[6:])
                        value = float(input("Value: "))
                        account = str(input("Account Name: "))
                        category = str(input("Category: "))
                        tag = str(input("Tag: "))
                        register.addTransaction(year,month,day,value,account,category,tag)
                    elif command == 'csv': 
                        command = input("filename: ")
                        file = Path(command)
                        if file.is_file():
                            register.addTransactionsFromCsv(command)
                        else:
                            print(f'file {command} does not exist')
                    else: 
                        continue
                elif command == 'delete':
                    id = int(input("id: "))
                    register.deleteTransaction(id)
                elif command == 'modify':
                    id = int(input("id: "))
                    register.modifyTransaction(id)
                elif command == 'view':
                    register.viewTransactions()
                elif command == 'exit':
                    break
                else:
                    print('invalid input')
                    continue
        elif command == 'accounts':
            while True:
                command = input("add view exit: ")
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
            command = input("year account: ")
            if command == 'year':
                register.viewAnnualTotals()
                plotting.plotAnnualTotals(register)
            elif command == 'account':
                register.viewAccountTotals()
        elif command == 'exit':
            shutdown(register)
        else: 
            continue
        

