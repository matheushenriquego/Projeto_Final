import pandas as pd
import os
import hashlib

class Subject:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, message, user_data=None):
        for observer in self._observers:
            observer.update(message, user_data)

class Observer:
    def update(self, message, user_data):
        print(f"Notificação: {message} | Dados: {user_data}")

def find_DB_user():
    if os.path.exists("users.csv"):
        df = pd.read_csv("users.csv")
        return df
    else:
        df = pd.DataFrame(columns = ["Name", "Surname", "Username", "Email", "Password"])
        return df

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

class Conta:
    def __init__(self):
        self.account_notifier = Subject()
        self.name = ""
        self.surname = ""
        self.username = ""
        self.email = ""
        self.__password = ""  # Agora a senha é privada

    def set_password(self, password):
        """Define a senha aplicando hash para segurança."""
        self.__password = hash_password(password)

    def get_password(self):
        """Retorna a senha de forma segura (ou um hash para verificação)."""
        return self.__password  # Retorna apenas o hash para segurança

    def register(self, db):
        print("Register your account now!")
        self.name = str(input("Type your Name: "))
        self.surname = str(input("Type your Surname: "))
        self.username = str(input("Type your Username (without spaces): ")).lower()
        self.email = str(input("Type your Email: "))
        password = str(input("Type your Password: "))  # Captura senha do usuário
        self.set_password(password)  # Aplica hash antes de armazenar

        if self.username in db["Username"].values or self.email in db["Email"].values:
            print("Username or Email already exists. Try another one.")
            return db, None

        tempDB = pd.DataFrame({
            "Name": [self.name],
            "Surname": [self.surname],
            "Username": [self.username],
            "Email": [self.email],
            "Password": [self.get_password()]  # Armazena o hash no banco
        })
        db = pd.concat([db, tempDB], ignore_index=True)
        db.to_csv("users.csv", index=False)
        self.account_notifier.notify_observers(
            f"Novo usuário registrado: {self.username}",
            {"Email": self.email, "Name": self.name}
        )
        print("Account created successfully!")
        input("Press Enter to continue...")
        clear_terminal()
        return db, {"Name": self.name, "Surname": self.surname, "Username": self.username, "Email": self.email}

    def login(self, db):
        print("Login to your account now!")
        u = str(input("Type your Username: ")).lower()
        p = str(input("Type your Password: "))

        user_row = db[db["Username"] == u]
        if not user_row.empty and user_row.iloc[0]["Password"] == hash_password(p):
            print("Login successful!")
            #login_email(user_row["Email"].values[0], user_row["Name"].values[0], user_row["Surname"].values[0])
            input("Press Enter to continue...")
            clear_terminal()
            return {
                "Name": user_row["Name"].values[0],
                "Surname": user_row["Surname"].values[0],
                "Username": user_row["Username"].values[0],
                "Email": user_row["Email"].values[0]
            }
        else:
            print("Username or Password incorrect. Try again.")
            input("Press Enter to continue...")
            clear_terminal()
            return None
        
    def modify(self, db, cuser):
        print("Modify your account now!")
        while True:
            print("What do you want to modify?")
            choice = str(input().lower())
            choose = False

            if choice == "name":
                new_name = str(input("Type your new Name: "))
                db.loc[db["Name"] == cuser["Name"], "Name"] = new_name
                cuser["Name"] = new_name
                db.to_csv("users.csv", index = False)
                db = pd.read_csv("users.csv")
                choose = True
                print("Name modified sucessfully!")
            
            elif choice == "surname":
                new_surname = str(input("Type your new Surname: "))
                db.loc[db["Surname"] == cuser["Surname"], "Surname"] = new_surname
                cuser["Surname"] = new_surname
                db.to_csv("users.csv", index = False)
                db = pd.read_csv("users.csv")
                choose = True
                print("Surname modified sucessfully!")

            elif choice == "email":
                while True:
                    new_email = str(input("Type your new Email: "))
                    if new_email in db["Email"].values and "@" not in new_email:
                        print("Email already exists. Try another one.")

                    else:
                        db.loc[db["Email"] == cuser["Email"], "Email"] = new_email
                        cuser["Email"] = new_email
                        db.to_csv("users.csv", index = False)
                        db = pd.read_csv("users.csv")
                        choose = True
                        print("Email modified sucessfully!")
                        break

            else:
                print("Invalid choice. Try again.")
                choose = False
            
            if choose == True:
                print("Do you want to modify another field? (yes/no)")
                answer = str(input().lower())
                if answer == "no":
                    print("Account modified successfully!")
                    input("Press Enter to continue...")
                    clear_terminal()
                    break
        return db, cuser

    def logout(self, cuser):
        print("Do you want to logout? (yes/no)")
        choice = str(input().lower())
        if choice == "yes":
            print("Logging out...")
            #logout_email(cuser["Email"], cuser["Name"], cuser["Surname"])
            input("Press Enter to continue...")
            clear_terminal()
            return True
        else:
            input("Press Enter to continue...")
            clear_terminal()
            return False
        
    def delete(self, db, cuser):
        print("To delete your account, type your password.")
        p = str(input("Type your Password: "))

        user_row = db[db["Username"] == cuser["Username"]]

        if not user_row.empty and user_row.iloc[0]["Password"] == hash_password(p):
            #delete_email(cuser["Email"], cuser["Name"], cuser["Surname"])
            #delete_email(cuser["Email"], cuser["Name"], cuser["Surname"])
            db = db[db["Username"] != cuser["Username"]]  # Remove o usuário do banco
            db.to_csv("users.csv", index=False)

            project_file = f"{cuser['Username']}P.csv"
            task_file = f"{cuser['Username']}T.csv"

            if os.path.exists(project_file):
                os.remove(project_file)

            if os.path.exists(task_file):
                os.remove(task_file)

            print("Account deleted successfully!")
            input("Press Enter to continue...")
            clear_terminal()
            return True
        else:
            print("Password incorrect. Try again.")
            input("Press Enter to continue...")
            clear_terminal()
            return False