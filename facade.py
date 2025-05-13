import os
from account import *
from first_screen import *
from tasks import *
from projects import *


class TaskManagerFacade:
    def __init__(self, db, current_user):
        self.db = db
        self.current_user = current_user
        self.db_tasks = find_DB_tasks(current_user)
        self.db_projects = finder_DB_projects(current_user)

    # --- Métodos para Tarefas ---
    def add_task(self, task_type, **kwargs):
        """Adiciona uma tarefa (Recurring ou One_Time)."""
        if task_type == "recurring":
            task = R_Tasks()
            return task.add_recurring_task(self.db_tasks, self.db, self.current_user)
        elif task_type == "one_time":
            task = O_Tasks()
            return task.add_one_time_task(self.db_tasks, self.db, self.current_user)
        else:
            raise ValueError("Tipo de tarefa inválido. Use 'recurring' ou 'one_time'.")

    def delete_task(self, task_name):
        """Deleta uma tarefa pelo nome."""
        task = O_Tasks()  # Usamos O_Tasks só para herdar o método delete_task
        self.db_tasks = task.delete_task(self.db_tasks, self.current_user, self.db)
        return self.db_tasks

    # --- Métodos para Projetos ---
    def add_project(self, name, description, start_date, end_date, cuser):
        call_project = Project()
        call_project.Name_project(name)
        call_project.Description_project(description)
        call_project.Begin_project(start_date)
        call_project.End_project(end_date)
        call_project.constroi(self.db_projects) 
        call_project.Manager_project(cuser)
        self.db_projects = call_project.add_project(self.db, self.db_projects, self.db_tasks,cuser)

    def delete_project(self, project_name):
        """Deleta um projeto pelo nome."""
        project = Project()
        self.db_projects = project.delete_project(self.db_projects, self.current_user, self.db)
        return self.db_projects

    # --- Métodos para Conta ---
    def logout(self):
        """Facilita o logout."""
        from account import Conta
        account = Conta()
        return account.logout(self.current_user)