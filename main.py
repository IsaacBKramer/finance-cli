import sys
from register import Register

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
        

