# Task - Task and Project Manager

##  How to Run?

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/TaskNico.git
   cd TaskNico
   ```
2. **Install dependencies**
   ```bash
   pip install pandas smtplib
   ```
3. **Run the program**
   ```bash
   python main.py
   ```


## 1. Facade (Estrutural)
**Localização**: facade.py

**Propósito**: Simplificar a complexidade do sistema fornecendo uma interface unificada para um conjunto de interfaces em subsistemas.
Implementação:

A classe TaskManagerFacade fornece métodos simplificados para operações complexas envolvendo tarefas, projetos e conta do usuário.

Esconde a complexidade das classes Task, Project e Conta por trás de uma interface simples.

Exemplo de uso no seccond_screen.py onde o menu principal interage apenas com a fachada.

## 2. Builder (Criacional)
**Localização**: Principalmente em projects.py (classe Project)

**Propósito**: Separar a construção de um objeto complexo de sua representação, permitindo a mesma construção para diferentes representações.
Implementação:

A classe Project usa métodos encadeados (Name_project(), Description_project(), etc.) para construir o objeto projeto passo a passo.

Permite a construção flexível de projetos com diferentes combinações de atributos.

Exemplo de uso no facade.py no método add_project().

## 3. Observer (Comportamental)
**Localização**: account.py (classes Subject e Observer) e tasks.py

**Propósito**: Definir uma dependência um-para-muitos entre objetos, de modo que quando um objeto muda de estado, todos os seus dependentes são notificados e atualizados automaticamente.
Implementação:

Subject mantém uma lista de observadores e notifica sobre mudanças.

Observer define uma interface para objetos que devem ser notificados.

Implementado para notificar sobre:

Criação de novas tarefas (em tasks.py)

Registro de novos usuários (em account.py)

Exemplo: TaskLogger em tasks.py que registra atividades de tarefas.
---
## Funcionalyties

Task Creation and Assignment: Implemented
Deadline and Priority Setting: implemented
Progress Tracking and Updates: Not implemented, 
because I couldn't create a function that when the deadline arrives can tell if it was completed
Collaboration and Communication Tools: Not implemented, becouse needs a cloud data bank, to remote acess
File Sharing and Management: Not implemented, i don't know how to upload a file on code
Calendar Integration: Not implemented, i don't have the knolege of a library that do that
Customizable Workflow: implemented
Notifications and Alerts: implemented
Reporting and Analytics: Not implemented
Access Control and Permissions: Not implemented
