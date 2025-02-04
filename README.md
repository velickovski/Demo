
# Task Manager API

This project is a back-end implementation for a Task Manager application. The back-end is responsible for managing data related to users and tasks, providing the foundation for task prioritization, deadlines, visibility, recurrence, and tagging. While this project does not include API endpoints, it provides a robust data management layer through its database schema.

## Database Design

### Tables

#### tbl_Tasks
| Field         | Type             | Description                                     |
|---------------|------------------|-------------------------------------------------|
| ID            | autoIncremented  | Primary key for the tasks table.               |
| taskName      | nonUnique        | Name of the task.                              |
| priority      | Enum (Low, Medium, High) | Priority level of the task.                  |
| deadline      | %YYYY-%MM-%DD    | Deadline for task completion.                  |
| isCompleted   | Boolean (True/False) | Indicates if the task is completed.         |
| isVisible     | Boolean (True/False) | Indicates if the task is visible to the user. |
| userID        | Foreign Key (tbl_Users.userID) | Links the task to a user in tbl_Users. |
| isRecurring   | Boolean (True/False) | Indicates if the task is recurring.          |
| tag           | Text             | Task category (e.g., Work, Personal).          |

#### tbl_Users
| Field         | Type             | Description                                     |
|---------------|------------------|-------------------------------------------------|
| userID        | autoIncremented  | Primary key for the users table.               |
| name          | Text             | Name of the user.                              |
| mail          | Text (Unique)    | Unique email address of the user.              |

## Features

- **User Management**: Create, read, update, and delete (CRUD) operations for users.
- **Task Management**: CRUD operations for tasks, linked to specific users.
- **Task Prioritization**: Assign and update priorities (Low, Medium, High).
- **Deadlines**: Set and manage deadlines for tasks.
- **Completion Status**: Mark tasks as completed or incomplete.
- **Visibility Control**: Control whether a task is visible or hidden.
- **Recurring Tasks**: Mark tasks as recurring for repetitive schedules.
- **Tagging**: Organize tasks by tags (e.g., Work, Personal).