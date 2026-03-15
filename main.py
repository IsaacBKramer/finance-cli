import sys
from register import Register
import plotting

def startup():
    register = Register()
    register.checkIndex()
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
            command = input("(1)add manual transaction (2) bulk import from csv: ")
            if command == '1':
                register.addTransaction()
            elif command == '2': 
                command = input("filename: ")
                register.addTransactionsFromCsv(command)
            else: 
                continue
        elif command == '2':
            register.deleteTransaction()
        elif command == '3':
            register.modifyTransaction()
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
        

