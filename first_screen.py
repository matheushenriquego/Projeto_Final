from account import *
import os

def login_register_screen():
    account_ini = Conta()
    
    while True:
        print("Welcome to TaskNico! Your personal task manager. Lets start!")
        print("Please login or register to start using the app.")
        print("For login type 'login'")
        print("For register type 'register'")
        print("For exit type 'exit'")
        choice = str(input("Type your choice: ")).lower()

        if choice == "login":
            db = find_DB_user()
            cuser = account_ini.login(db)
            if cuser != None:
                return db, cuser
        
        elif choice == "register":
            db = find_DB_user()
            db, cuser = account_ini.register(db)
            if cuser != None:
                return db, cuser

        elif choice == "exit":
            print("Exiting...")
            input("Press Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')
            exit()

        else:
            print("Invalid choice. Try again.")
            input("Press Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')