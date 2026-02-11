# cli/project_cli.py
import argparse
import requests

API_PROJECT = "http://localhost:8000/api/v1/projects"
API_USER = "http://localhost:8001/api/v1/auth"  

# ====== وظائف CLI ======
def login(email, password):
    response = requests.post(f"{API_USER}/login", json={"email": email, "password": password})
    print(response.json())

def logout():
    response = requests.post(f"{API_USER}/logout")
    print(response.json())

def create_project(title, description, leader):
    response = requests.post(API_PROJECT, json={"title": title, "description": description, "leader": leader})
    print(response.json())

def list_projects():
    response = requests.get(API_PROJECT)
    projects = response.json()
    for pid, p in projects.items():
        print(f"{p['title']} ({len(p['members'])} members)")

def join_project(project_id):
    response = requests.post(f"{API_PROJECT}/{project_id}/members", json={"username": "ayat"})
    print(response.json())

def view_requests(project_id):
    response = requests.get(f"{API_PROJECT}/{project_id}/requests")
    print(response.json())

def approve_request(project_id, username, approve=True):
    response = requests.post(f"{API_PROJECT}/{project_id}/approve", json={"username": username, "approve": approve})
    print(response.json())

def update_project(project_id, title=None, description=None):
    data = {}
    if title: data["title"] = title
    if description: data["description"] = description
    response = requests.put(f"{API_PROJECT}/{project_id}", json=data)
    print(response.json())

# ====== إعداد CLI ======
parser = argparse.ArgumentParser(description="UniCollab Projects CLI")
subparsers = parser.add_subparsers(dest="command")

# ----- User commands -----
login_parser = subparsers.add_parser("login", help="Login user")
login_parser.add_argument("--email", required=True)
login_parser.add_argument("--password", required=True)

logout_parser = subparsers.add_parser("logout", help="Logout user")

# ----- Project commands -----
create_parser = subparsers.add_parser("create-project", help="Create a new project")
create_parser.add_argument("--title", required=True)
create_parser.add_argument("--description", required=True)
create_parser.add_argument("--leader", required=True)

list_parser = subparsers.add_parser("list-projects", help="List all projects")

join_parser = subparsers.add_parser("join-project", help="Join a project")
join_parser.add_argument("--project-id", required=True)

view_req_parser = subparsers.add_parser("view-requests", help="View join requests")
view_req_parser.add_argument("--project-id", required=True)

approve_parser = subparsers.add_parser("approve-request", help="Approve/Reject join request")
approve_parser.add_argument("--project-id", required=True)
approve_parser.add_argument("--username", required=True)
approve_parser.add_argument("--approve", type=bool, default=True, help="True=Approve, False=Reject")

update_parser = subparsers.add_parser("update-project", help="Update project info")
update_parser.add_argument("--project-id", required=True)
update_parser.add_argument("--title")
update_parser.add_argument("--description")

# ====== تنفيذ CLI ======
args = parser.parse_args()

if args.command == "login":
    login(args.email, args.password)
elif args.command == "logout":
    logout()
elif args.command == "create-project":
    create_project(args.title, args.description, args.leader)
elif args.command == "list-projects":
    list_projects()
elif args.command == "join-project":
    join_project(args.project_id)
elif args.command == "view-requests":
    view_requests(args.project_id)
elif args.command == "approve-request":
    approve_request(args.project_id, args.username, args.approve)
elif args.command == "update-project":
    update_project(args.project_id, args.title, args.description)
else:
    parser.print_help()
