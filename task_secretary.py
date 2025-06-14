import json
import os
import argparse
from collections import defaultdict

TASKS_FILE = 'tasks.json'
KNOWLEDGE_FILE = 'knowledge_base.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def load_knowledge():
    if not os.path.exists(KNOWLEDGE_FILE):
        return defaultdict(list)
    with open(KNOWLEDGE_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return defaultdict(list, data)
        except json.JSONDecodeError:
            return defaultdict(list)

def gather_resources(description, knowledge):
    resources = []
    for keyword, res_list in knowledge.items():
        if keyword.lower() in description.lower():
            resources.extend(res_list)
    return resources

def add_task(description):
    tasks = load_tasks()
    knowledge = load_knowledge()
    new_id = max([t.get('id', 0) for t in tasks] or [0]) + 1
    resources = gather_resources(description, knowledge)
    task = {
        'id': new_id,
        'description': description,
        'status': 'todo',
        'resources': resources
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task {new_id} added.")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print('No tasks found.')
        return
    for t in tasks:
        print(f"ID: {t['id']} | Status: {t['status']} | Description: {t['description']}")
        if t["resources"]:
            print("  Resources:")
            for r in t["resources"]:
                print(f"   - {r}")
        print()
def update_status(task_id, status):
    tasks = load_tasks()
    for t in tasks:
        if t.get('id') == task_id:
            t['status'] = status
            save_tasks(tasks)
            print(f"Task {task_id} updated to {status}.")
            return
    print(f"Task {task_id} not found.")


def main():
    parser = argparse.ArgumentParser(description='Simple Task Secretary')
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', help='Task description')

    list_parser = subparsers.add_parser('list', help='List tasks')

    mark_parser = subparsers.add_parser('mark', help='Update task status')
    mark_parser.add_argument('id', type=int, help='Task ID')
    mark_parser.add_argument('status', choices=['todo', 'in-progress', 'done'], help='New status')

    args = parser.parse_args()

    if args.command == 'add':
        add_task(args.description)
    elif args.command == 'list':
        list_tasks()
    elif args.command == 'mark':
        update_status(args.id, args.status)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
