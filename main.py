import sys
from register import Register

def startup():
    print('\n########## WELCOME TO FINANCE-CLI ##########\n')
    print('Follow the prompts or type "exit" at any time to terminate the program.\n')

def shutdown():
    print('goodbye')
    sys.exit(0)

if __name__ == "__main__":
    register = Register()
    startup()
    while True:
        command = input("(1)add (2)delete (3)modify (4)register (5)totals (6)exit: ")
        if command == '1':
            register.addTransaction()
        elif command == '2':
            register.deleteTransaction()
        elif command == '3':
            register.modifyTransaction()
        elif command == '4':
            register.viewTransactions()
        elif command == '5':
            register.viewAnnualTotal()
        elif command == '6' or command == 'exit':
            register.connection.commit()
            register.connection.close()
            shutdown()
        else: 
            continue
        

