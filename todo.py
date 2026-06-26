# todo.py - Complete To-Do List Application
# CODSOFT Python Programming Internship - Task 1

import json
import os

# File to store tasks
TASKS_FILE = "tasks.json"

# ========== LOAD AND SAVE ==========

def load_tasks():
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)
    print("Tasks saved!")

# ========== MAIN FUNCTIONS ==========

def add_task(tasks):
    print("\n--- ADD TASK ---")
    description = input("Enter task: ").strip()
    if not description:
        print("Task cannot be empty!")
        return tasks
    
    # Get next ID
    if tasks:
        next_id = max(t["id"] for t in tasks) + 1
    else:
        next_id = 1
    
    tasks.append({
        "id": next_id,
        "description": description,
        "completed": False
    })
    
    save_tasks(tasks)
    print("Task added! ID: " + str(next_id))
    return tasks

def view_tasks(tasks):
    print("\n--- YOUR TASKS ---")
    if not tasks:
        print("No tasks found!")
        return
    
    for t in tasks:
        status = "✓" if t["completed"] else " "
        print("[" + status + "] " + str(t["id"]) + ". " + t["description"])

def mark_completed(tasks):
    print("\n--- MARK COMPLETED ---")
    if not tasks:
        print("No tasks found!")
        return tasks
    
    view_tasks(tasks)
    try:
        task_id = int(input("Enter task ID to mark complete: "))
        for t in tasks:
            if t["id"] == task_id:
                if t["completed"]:
                    print("Already completed!")
                else:
                    t["completed"] = True
                    save_tasks(tasks)
                    print("Task marked as completed!")
                return tasks
        print("Task not found!")
    except:
        print("Invalid ID!")
    return tasks

def delete_task(tasks):
    print("\n--- DELETE TASK ---")
    if not tasks:
        print("No tasks found!")
        return tasks
    
    view_tasks(tasks)
    try:
        task_id = int(input("Enter task ID to delete: "))
        for i, t in enumerate(tasks):
            if t["id"] == task_id:
                confirm = input("Delete '" + t["description"] + "'? (y/n): ")
                if confirm.lower() == 'y':
                    tasks.pop(i)
                    save_tasks(tasks)
                    print("Task deleted!")
                else:
                    print("Cancelled!")
                return tasks
        print("Task not found!")
    except:
        print("Invalid ID!")
    return tasks

def delete_all(tasks):
    print("\n--- DELETE ALL ---")
    if not tasks:
        print("No tasks to delete!")
        return tasks
    
    confirm = input("Delete ALL tasks? (y/n): ")
    if confirm.lower() == 'y':
        tasks = []
        save_tasks(tasks)
        print("All tasks deleted!")
    else:
        print("Cancelled!")
    return tasks

def show_stats(tasks):
    print("\n--- STATISTICS ---")
    if not tasks:
        print("No tasks!")
        return
    
    completed = sum(1 for t in tasks if t["completed"])
    pending = len(tasks) - completed
    
    print("Total tasks: " + str(len(tasks)))
    print("Completed: " + str(completed))
    print("Pending: " + str(pending))
    
    if len(tasks) > 0:
        percent = (completed / len(tasks)) * 100
        print("Completion rate: " + str(round(percent, 1)) + "%")

# ========== MAIN MENU ==========

def main():
    tasks = load_tasks()
    
    while True:
        print("\n" + "="*40)
        print("TO-DO LIST")
        print("="*40)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Completed")
        print("4. Delete Task")
        print("5. Delete All Tasks")
        print("6. Statistics")
        print("7. Exit")
        print("="*40)
        
        choice = input("Choose (1-7): ")
        
        if choice == '1':
            tasks = add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            tasks = mark_completed(tasks)
        elif choice == '4':
            tasks = delete_task(tasks)
        elif choice == '5':
            tasks = delete_all(tasks)
        elif choice == '6':
            show_stats(tasks)
        elif choice == '7':
            save_tasks(tasks)
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()