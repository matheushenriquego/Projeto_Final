import os
from account import *
from first_screen import *
from tasks import *
from projects import *
from facade import *
import pandas as pd

def menu(db, current_user):
    facade = TaskManagerFacade(db, current_user)

    while True:
        print(f"Olá {current_user['Name']}! O que deseja fazer?")
        print("1. Adicionar tarefa")
        print("2. Ver tarefas")
        print("3. Deletar tarefa")
        print("4. Adicionar projeto")
        print("5. Ver projetos")
        print("6. Deletar projeto")
        print("7. Sair")

        choice = input("Escolha uma opção: ").strip()

        if choice == "1":
            task_type = input("Tipo de tarefa (recurring/one_time): ").lower()
            facade.db_tasks=facade.add_task(task_type)
        
        elif choice == "2":
            print(facade.db_tasks)
        
        elif choice == "3":
            task_name = input("Nome da tarefa a deletar: ")
            facade.delete_task(task_name)
        
        elif choice == "4":
            name = input("Nome do projeto: ")
            description = input("Descrição: ")
            start = input("Data de início: ")
            end = input("Data de término: ")
            facade.add_project(name, description, start, end, current_user)
        
        elif choice == "5":
            print(facade.db_projects)
        
        elif choice == "6":
            project_name = input("Nome do projeto a deletar: ")
            facade.delete_project(project_name)
        
        elif choice == "7":
            facade.logout()
            break

        input("Pressione Enter para continuar...")
        os.system('cls' if os.name == 'nt' else 'clear')

# Ponto de entrada
if __name__ == "__main__":
    db, user = login_register_screen()
    menu(db, user)