import sqlite3
from datetime import datetime, date
from pathlib import Path

# =====================================
# DATABASE
# =====================================

DB_PATH = Path(__file__).resolve().parent / "ms.sl3"

db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA foreign_keys = ON")


def create_database():
    db.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            deadline TEXT,
            FOREIGN KEY (project_id)
                REFERENCES projects(id)
                ON DELETE CASCADE
        )
    """)

    db.commit()


# =====================================
# PROJECTS
# =====================================

def add_project():
    print("\n--- CREATE PROJECT ---")

    name = input("Project name: ").strip()

    if not name:
        print("Name cannot be empty!")
        return

    description = input("Description: ")

    try:
        db.execute("""
            INSERT INTO projects (name, description)
            VALUES (?, ?)
        """, (name, description))

        db.commit()

        print("\nProject created successfully!")

        show_projects()

    except sqlite3.IntegrityError:
        db.rollback()
        print("Project with this name already exists!")

    except sqlite3.Error as error:
        db.rollback()
        print("Database error:", error)


def show_projects():
    print("\n--- PROJECTS ---")

    try:
        projects = db.execute("""
            SELECT id, name, description
            FROM projects
            ORDER BY id
        """).fetchall()

        if not projects:
            print("No projects found!")
            return

        for project in projects:
            print("\n-----------------------")
            print("ID:", project[0])
            print("Name:", project[1])
            print("Description:", project[2] or "No description")

    except sqlite3.Error as error:
        print("Database error:", error)


def delete_project():
    show_projects()

    try:
        project_id = int(input("\nProject ID to delete: "))

        project = db.execute("""
            SELECT name
            FROM projects
            WHERE id = ?
        """, (project_id,)).fetchone()

        if project is None:
            print("Project not found!")
            return

        confirm = input(
            f"Delete '{project[0]}'? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Deletion cancelled!")
            return

        db.execute("""
            DELETE FROM projects
            WHERE id = ?
        """, (project_id,))

        db.commit()

        print("\nProject deleted successfully!")
        print("Related tasks deleted successfully!")

        show_projects()

    except ValueError:
        print("Invalid project ID!")

    except sqlite3.Error as error:
        db.rollback()
        print("Database error:", error)


# =====================================
# TASKS
# =====================================

def add_task():
    print("\n--- CREATE TASK ---")

    show_projects()

    try:
        project_id = int(input("\nProject ID: "))
    except ValueError:
        print("Invalid project ID!")
        return

    project = db.execute("""
        SELECT id
        FROM projects
        WHERE id = ?
    """, (project_id,)).fetchone()

    if project is None:
        print("Project does not exist!")
        return

    title = input("Task title: ").strip()

    if not title:
        print("Task title cannot be empty!")
        return

    priority = input(
        "Priority (Low/Medium/High): "
    ).strip().capitalize()

    if priority not in ["Low", "Medium", "High"]:
        print("Invalid priority!")
        return

    deadline = input(
        "Deadline (YYYY-MM-DD): "
    ).strip()

    if deadline:
        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            print("Invalid date! Use YYYY-MM-DD.")
            return

    try:
        db.execute("""
            INSERT INTO tasks
            (project_id, title, priority, deadline)
            VALUES (?, ?, ?, ?)
        """, (project_id, title, priority, deadline or None))

        db.commit()

        print("\nTask created successfully!")

    except sqlite3.Error as error:
        db.rollback()
        print("Database error:", error)


def show_tasks():
    print("\n--- ALL TASKS ---")

    try:
        tasks = db.execute("""
            SELECT
                tasks.id,
                tasks.title,
                projects.name,
                tasks.priority,
                tasks.status,
                tasks.deadline
            FROM tasks
            JOIN projects
                ON tasks.project_id = projects.id
            ORDER BY tasks.id DESC
        """).fetchall()

        if not tasks:
            print("No tasks found!")
            return

        for task in tasks:
            print("\n-----------------------")
            print("ID:", task[0])
            print("Task:", task[1])
            print("Project:", task[2])
            print("Priority:", task[3])
            print("Status:", task[4])
            print("Deadline:", task[5] or "Not set")

            if (
                task[5]
                and task[5] < date.today().isoformat()
                and task[4] != "Completed"
            ):
                print("WARNING: OVERDUE!")

    except sqlite3.Error as error:
        print("Database error:", error)


def update_task():
    show_tasks()

    try:
        task_id = int(input("\nTask ID: "))
    except ValueError:
        print("Invalid task ID!")
        return

    task = db.execute("""
        SELECT id
        FROM tasks
        WHERE id = ?
    """, (task_id,)).fetchone()

    if task is None:
        print("Task not found!")
        return

    print("\n1. Pending")
    print("2. In Progress")
    print("3. Completed")

    choice = input("Choose status: ").strip()

    statuses = {
        "1": "Pending",
        "2": "In Progress",
        "3": "Completed"
    }

    if choice not in statuses:
        print("Invalid choice!")
        return

    try:
        db.execute("""
            UPDATE tasks
            SET status = ?
            WHERE id = ?
        """, (statuses[choice], task_id))

        db.commit()

        print("Task updated successfully!")

    except sqlite3.Error as error:
        db.rollback()
        print("Database error:", error)


def delete_task():
    show_tasks()

    try:
        task_id = int(input("\nTask ID to delete: "))
    except ValueError:
        print("Invalid task ID!")
        return

    try:
        cursor = db.execute("""
            DELETE FROM tasks
            WHERE id = ?
        """, (task_id,))

        db.commit()

        if cursor.rowcount > 0:
            print("Task deleted successfully!")
        else:
            print("Task not found!")

    except sqlite3.Error as error:
        db.rollback()
        print("Database error:", error)


# =====================================
# STATISTICS
# =====================================

def show_statistics():
    print("\n--- STATISTICS ---")

    try:
        projects = db.execute("""
            SELECT COUNT(*)
            FROM projects
        """).fetchone()[0]

        tasks = db.execute("""
            SELECT COUNT(*)
            FROM tasks
        """).fetchone()[0]

        statuses = db.execute("""
            SELECT status, COUNT(*)
            FROM tasks
            GROUP BY status
        """).fetchall()

        overdue = db.execute("""
            SELECT COUNT(*)
            FROM tasks
            WHERE deadline IS NOT NULL
            AND deadline < ?
            AND status != 'Completed'
        """, (date.today().isoformat(),)).fetchone()[0]

        print("Total projects:", projects)
        print("Total tasks:", tasks)
        print("Overdue tasks:", overdue)

        print("\nTask statuses:")

        for status, count in statuses:
            print(f"{status}: {count}")

    except sqlite3.Error as error:
        print("Database error:", error)


# =====================================
# MAIN MENU
# =====================================

def main():

    create_database()

    print("Database:", DB_PATH)

    while True:

        print("\n================================")
        print("       PERSONAL MANAGEMENT")
        print("================================")

        print("1. Create project")
        print("2. Show projects")
        print("3. Delete project")
        print("4. Create task")
        print("5. Show tasks")
        print("6. Update task")
        print("7. Delete task")
        print("8. Statistics")
        print("0. Exit")

        choice = input("\nChoose an option: ").strip()

        try:

            if choice == "1":
                add_project()

            elif choice == "2":
                show_projects()

            elif choice == "3":
                delete_project()

            elif choice == "4":
                add_task()

            elif choice == "5":
                show_tasks()

            elif choice == "6":
                update_task()

            elif choice == "7":
                delete_task()

            elif choice == "8":
                show_statistics()

            elif choice == "0":
                print("\nGoodbye!")
                break

            else:
                print("Invalid choice!")

        except sqlite3.Error as error:
            db.rollback()
            print("Database error:", error)


# =====================================
# START PROGRAM
# =====================================

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nProgram interrupted!")

    finally:
        db.close()
        print("Database connection closed.")