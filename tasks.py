import pandas as pd
import os
from abc import ABC, abstractmethod
from account import Subject, Observer

# Adicione um Subject global para tarefas
task_notifier = Subject()

# Exemplo de Observer concreto (opcional)
class TaskLogger(Observer):
    def update(self, message, user_data):
        print(f"[LOG] Tarefa: {message} | Responsável: {user_data['Username']}")

# Registrar o logger (opcional)
task_notifier.add_observer(TaskLogger())


def find_DB_tasks(cuser):
    if os.path.exists(f"{cuser['Username']}T.csv"):
        df = pd.read_csv(f"{cuser['Username']}T.csv")
        return df
    else:
        df = pd.DataFrame(columns=["Task_Name", "Task_Description", "Task_Priority", "Task_Status", "Task_Manager", "Task_Colaborators", "Task_Type", "Task_Recurring", "Task_Recurring_Dates", "Task_Recurring_Time", "Task_Dini", "Task_Tini", "Task_Dend", "Task_Tend", "Task_Arquive"])
        df.to_csv(f"{cuser['Username']}T.csv", index=False)
        return df
#email
def find_DB_tasks_C(user):
    if os.path.exists(f"{user}T.csv"):
        df = pd.read_csv(f"{user}T.csv")
        return df
    else:
        df = pd.DataFrame(columns=["Task_Name", "Task_Description", "Task_Priority", "Task_Status", "Task_Manager", "Task_Colaborators", "Task_Type", "Task_Recurring", "Task_Recurring_Dates", "Task_Recurring_Time", "Task_Dini", "Task_Tini", "Task_Dend", "Task_Tend", "Task_Arquive"])
        return df

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def choice_task(db_task, db_users, cuser):
    print("Type 'Recurring' to add a recurring task or 'One_Time' to add a one-time task: ")
    choice = str(input().lower())
    while True:
        if choice == "recurring":
            call_task = R_Tasks()
            db_task = call_task.add_recurring_task(db_task, db_users, cuser)
            break
        elif choice == "one_time":
            call_task = O_Tasks()
            db_task = call_task.add_one_time_task(db_task, db_users, cuser)
            break
        else:
            print("Invalid choice. Try again.")
            choice = str(input().lower())
    return db_task

class Show(ABC):
    @abstractmethod
    def show(self):
        pass

class Task:
    def __init__(self):
        self.task_name = ""
        self.task_description = ""
        self.task_Manager = ""
        self.task_colaborators = []
        self.task_status = ""
        self.task_priority = ""
        self.task_type = ""
        self.task_arquive = ''

    def add_task(self, db_task, db_users, cuser):
        while True:
            self.task_name = input("Type the task name: ")
            if self.task_name in db_task["Task_Name"].values:
                print("Task name already exists. Try again.")
            else:
                break

        self.task_description = input("Type the task description: ")
        self.task_Manager = cuser["Username"]
        self.task_status = "On_going"
        while True:
            print("Type the task priority, to low type 1, to medium type 2, to high type 3: ")
            self.task_priority = int(input())
            if self.task_priority == 1 or self.task_priority == 2 or self.task_priority == 3:
                break
            else:
                print("Invalid choice. Try again.")

    def delete_task(self, db_task, cuser, db_users):
        print("Type the task name you want to delete: ")
        task_name = input()

        if task_name in db_task["Task_Name"].values:
            task_row = db_task[db_task["Task_Name"] == task_name].iloc[0]
            if task_row["Task_Manager"] == cuser["Username"]:
                
                collaborators = task_row["Task_Colaborators"].split(", ")
                for collaborator in collaborators:
                    collaborator_email = db_users[db_users["Username"] == collaborator]["Email"].iloc[0]
                    collaborator_name = db_users[db_users["Username"] == collaborator]["Name"].iloc[0]
                    collaborator_surname = db_users[db_users["Username"] == collaborator]["Surname"].iloc[0]
                    #task_deleted_email(collaborator_email, collaborator_name, collaborator_surname, task_name)

                
                for user in task_row["Task_Colaborators"].split(", "):
                    db_taskou = find_DB_tasks_C(user)
                    db_taskou = db_taskou[db_taskou["Task_Name"] != task_name]
                    db_taskou.to_csv(f"{user}T.csv", index=False)
                
                
                db_task = db_task[db_task["Task_Name"] != task_name]
                db_task.to_csv(f"{cuser['Username']}T.csv", index=False)
                print("Task deleted successfully!")
            else:
                print("You are not the manager of this task. Cannot delete.")
        else:
            print("Task not found. Try again.")
        
        input("Press enter to continue...")
        clear_terminal
        return db_task

class R_Tasks(Task,Show):
    def __init__(self):
        super().__init__()
        self.recurring = ""
        self.recurring_dates = ""
        self.recurring_time = ""

    def show(self):
        print(self.recurring,self.recurring_dates,self.recurring_time,self.task_type)

    def add_recurring_task(self, db_task, db_users, cuser):
        print("Adding a recurrent task now!")
        super().add_task(db_task, db_users, cuser)
        self.recurring = input("Type the recurring type: ")
        self.recurring_dates = input("Type the recurring dates: ")
        self.recurring_time = input("Type the recurring time: ")
        self.task_type = "Recurring"
        self.task_arquive = input('Arquive for the project')
        self.show()
        print("Do you want to add collaborators to this task? (yes/no)")
        choice = str(input().lower())
        while True:
            if choice == "yes":
                print("Type the collaborators' usernames separated by commas: ")
                colaborators_input = input().strip()
                self.task_colaborators = [colab.strip() for colab in colaborators_input.split(",") if colab.strip()]
                self.task_colaborators.append(cuser["Username"])
                break
            elif choice == "no":
                self.task_colaborators = [cuser["Username"]]
                break
            else:
                print("Invalid choice. Try again.")
                choice = str(input().lower())

        collaborators_str = ", ".join(self.task_colaborators) if self.task_colaborators else ""

        temp_db = pd.DataFrame([{
            "Task_Name": self.task_name,
            "Task_Description": self.task_description,
            "Task_Priority": self.task_priority,
            "Task_Status": self.task_status,
            "Task_Manager": self.task_Manager,
            "Task_Colaborators": collaborators_str,
            "Task_Type": self.task_type,
            "Task_Recurring": self.recurring,
            "Task_Recurring_Dates": self.recurring_dates,
            "Task_Recurring_Time": self.recurring_time,
            "Task_Dini": "",
            "Task_Tini": "",
            "Task_Dend": "",
            "Task_Tend": "",
            "Task_Arquive": self.task_arquive
        }])
        db_task = pd.concat([db_task, temp_db], ignore_index=True)
        db_task.to_csv(f"{cuser['Username']}T.csv", index=False)
        
        # Atualizar banco de dados de cada colaborador
        for collaborator in self.task_colaborators:
            if collaborator != cuser["Username"]:
                db_taskou = find_DB_tasks_C(collaborator)
                db_taskou = pd.concat([db_taskou, temp_db], ignore_index=True)
                db_taskou.to_csv(f"{collaborator}T.csv", index=False)
        
        task_notifier.notify_observers(
            f"Nova tarefa recorrente: {self.task_name}",
            cuser
        )
        
        print("Task added successfully!")
        return db_task


class O_Tasks(Task,Show):
    def __init__(self):
        super().__init__()
        self.task_dini = ""
        self.task_tini = ""
        self.task_dend = ""
        self.task_tend = ""

    def show(self):
        print(self.task_dini,self.task_tini,self.task_dend,self.task_tend, self.task_type)
        
    def add_one_time_task(self, db_task, db_users, cuser):
        print("Adding a one-time task now!")
        super().add_task(db_task, db_users, cuser)
        self.task_dini = input("Type the initial date: ")
        self.task_tini = input("Type the initial time: ")
        self.task_dend = input("Type the end date: ")
        self.task_tend = input("Type the end time: ")
        self.task_arquive = input('Arquive for the project')
        self.task_type = "One_Time"
        self.show()
        print("Do you want to add collaborators to this task? (yes/no)")
        choice = str(input().lower())
        while True:
            if choice == "yes":
                print("Type the collaborators' usernames separated by commas: ")
                colaborators_input = input().strip()
                self.task_colaborators = [colab.strip() for colab in colaborators_input.split(",") if colab.strip()]
                self.task_colaborators.append(cuser["Username"])
                break
            elif choice == "no":
                self.task_colaborators = [cuser["Username"]]
                break
            else:
                print("Invalid choice. Try again.")
                choice = str(input().lower())

        collaborators_str = ", ".join(self.task_colaborators) if self.task_colaborators else ""

        temp_db = pd.DataFrame([{
            "Task_Name": self.task_name,
            "Task_Description": self.task_description,
            "Task_Priority": self.task_priority,
            "Task_Status": self.task_status,
            "Task_Manager": self.task_Manager,
            "Task_Colaborators": collaborators_str,
            "Task_Type": self.task_type,
            "Task_Recurring": "",
            "Task_Recurring_Dates": "",
            "Task_Recurring_Time": "",
            "Task_Dini": self.task_dini,
            "Task_Tini": self.task_tini,
            "Task_Dend": self.task_dend,
            "Task_Tend": self.task_tend,
            "Task_Arquive": self.task_arquive
        }])
        db_task = pd.concat([db_task, temp_db], ignore_index=True)
        db_task.to_csv(f"{cuser['Username']}T.csv", index=False)
        
        # Atualizar banco de dados de cada colaborador
        for collaborator in self.task_colaborators:
            if collaborator != cuser["Username"]:
                db_taskou = find_DB_tasks_C(collaborator)
                db_taskou = pd.concat([db_taskou, temp_db], ignore_index=True)
                db_taskou.to_csv(f"{collaborator}T.csv", index=False)
        
        # Enviar email para o gerente e colaboradores
        #manager_email = db_users[db_users["Username"] == cuser["Username"]]["Email"].iloc[0]
        #manager_name = db_users[db_users["Username"] == cuser["Username"]]["Name"].iloc[0]
        #manager_surname = db_users[db_users["Username"] == cuser["Username"]]["Surname"].iloc[0]
        #task_created_email(manager_email, manager_name, manager_surname, self.task_name)
        
        #for collaborator in self.task_colaborators:
            #if collaborator != cuser["Username"]:
                #collaborator_email = db_users[db_users["Username"] == collaborator]["Email"].iloc[0]
                #collaborator_name = db_users[db_users["Username"] == collaborator]["Name"].iloc[0]
                #collaborator_surname = db_users[db_users["Username"] == collaborator]["Surname"].iloc[0]
                #task_created_email(collaborator_email, collaborator_name, collaborator_surname, self.task_name)
        
        print("Task added successfully!")
        return db_task