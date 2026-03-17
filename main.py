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
        command = input("(1)add (2)delete (3)modify (4)register (5)totals (6)exit: ")
        if command == '1':
            command = input("(1)manual (2)csv: ")
            if command == '1':
                date = input("Date YYYYMMDD: ")
                year = int(date[0:4])
                month = int(date[4:6])
                day = int(date[6:])
                value = float(input("Value: "))
                account = str(input("Account Name: "))
                category = str(input("Category: "))
                tag = str(input("Tag: "))
                register.addTransaction(year,month,day,value,account,category,tag)
            elif command == '2': 
                command = input("filename: ")
                file = Path(command)
                if file.is_file():
                    register.addTransactionsFromCsv(command)
                else:
                    print(f'file {command} does not exist')
            else: 
                continue
        elif command == '2':
            id = int(input("id: "))
            register.deleteTransaction(id)
        elif command == '3':
            id = int(input("id: "))
            register.modifyTransaction(id)
        elif command == '4':
            register.viewTransactions()
        elif command == '5':
            command = input("(1)by year (2)by account: ")
            if command == '1':
                register.viewAnnualTotals()
                plotting.plotAnnualTotals(register)
            elif command == '2':
                register.viewAccountTotals()
        elif command == '6' or command == 'exit':
            shutdown(register)
        else: 
            continue
        

