# UniCollab - CLI - main.py
from user_client import login, logout, get_me, can_join_project, assign_project, remove_project
from project_client import create_project, get_project, get_all_projects, update_project, add_member, remove_project_by_id

# =========================
# Global current user
# =========================
current_user = None  # Stores dict with email, username, role, project_id

# =========================
# CLI Functions
# =========================
def login_screen():
    global current_user
    print("=== Login ===")
    email = input("Email: ")
    password = input("Password: ")
    try:
        user_data = login(email, password)
        current_user = {
            "email": user_data.get("email", email),
            "username": user_data.get("username", ""),
            "role": user_data.get("role"),
            "project_id": user_data.get("project_id")
        }
        print(f"\n✅ Successfully logged in as: {current_user.get('username')}\n")
        main_menu()
    except Exception as e:
        print(f"❌ Login failed: {e}\n")
        login_screen()

def main_menu():
    while True:
        print("=== Main Menu ===")
        print("1. Create Project")
        print("2. Join Project")
        print("3. Update Project")
        print("4. View Project Details")
        print("5. Leave Project")
        print("6. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_project_flow()
        elif choice == "2":
            join_project_flow()
        elif choice == "3":
            update_project_flow()
        elif choice == "4":
            view_project_flow()
        elif choice == "5":
            leave_project_flow()
        elif choice == "6":
            logout_flow()
            break
        else:
            print("❌ Invalid choice, try again.\n")

# =========================
# Option 1: Create Project
# =========================
def create_project_flow():
    if not can_join_project(current_user.get("email")):
        print("❌ You are already in a project and cannot create another.\n")
        return
    title = input("Project Title: ")
    desc = input("Project Description: ")
    project_id = create_project(title, desc, current_user.get("email"))
    assign_project(current_user.get("email"), project_id, "leader")
    print("✅ Project created successfully!\n")

# =========================
# Option 2: Join Project (تصحيح فقط إرسال العضو)
# =========================
def join_project_flow():
    if not can_join_project(current_user.get("email")):
        print("❌ You are already in a project and cannot join another.\n")
        return
    projects_dict = get_all_projects()
    if not projects_dict:
        print("⚠️ No available projects to join.\n")
        return
    project_ids = list(projects_dict.keys())
    print("\nAvailable Projects:")
    for pid in project_ids:
        project = projects_dict[pid]
        # ⚡ عرض المشروع مع الـID مباشرة
        print(f"{pid}: {project['title']} ({project['desc']})")
    project_id = input("Enter the project ID to join: ")
    try:
        if project_id not in project_ids:
            raise ValueError("Invalid project ID")
        # ⚡ إرسال البريد كمفتاح 'member_name' كما يتطلب السيرفر
        add_member(project_id, current_user.get("email"))
        assign_project(current_user.get("email"), project_id, "member")
        print("✅ Successfully joined the project!\n")
    except Exception as e:
        print(f"❌ Failed to join project: {e}\n")

# =========================
# باقي الخيارات بدون أي تغيير
# =========================
def update_project_flow():
    me = get_me(current_user.get("email"))
    role = me.get("role")
    pid = me.get("project_id")
    if not role or not pid:
        print("❌ You must create/join a project first.\n")
        return
    if role == "member":
        print("❌ Only the project leader can update the project.\n")
        return
    project = get_project(pid)
    while True:
        print("\nUpdate Options:")
        print("1. Update Title")
        print("2. Update Description")
        print("3. Update Title & Description")
        print("4. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            title = input("New Project Title: ")
            update_project(pid, title=title)
            print("✅ Project title updated.\n")
        elif choice == "2":
            desc = input("New Project Description: ")
            update_project(pid, desc=desc)
            print("✅ Project description updated.\n")
        elif choice == "3":
            title = input("New Project Title: ")
            desc = input("New Project Description: ")
            update_project(pid, title=title, desc=desc)
            print("✅ Project updated.\n")
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice.\n")

def view_project_flow():
    me = get_me(current_user.get("email"))
    pid = me.get("project_id")
    if not pid:
        print("❌ You must create/join a project first.\n")
        return
    project = get_project(pid)
    print(f"\nProject Details:\nTitle: {project.get('title')}\nDescription: {project.get('desc')}\n")

def leave_project_flow():
    me = get_me(current_user.get("email"))
    pid = me.get("project_id")
    role = me.get("role")
    if not pid:
        print("❌ You must create/join a project first.\n")
        return
    project = get_project(pid)
    if role == "member":
        remove_project(current_user.get("email"))
        print("✅ You have left the project.\n")
    elif role == "leader":
        if project.get("members"):
            print("❌ You cannot leave the project as leader while members exist.\n")
        else:
            remove_project(current_user.get("email"))
            msg = remove_project_by_id(pid)
            print(f"✅ {msg}\n")

def logout_flow():
    global current_user
    logout(current_user.get("email"))
    print("\n✅ Logged out successfully.\n")
    current_user = None
    login_screen()

# =========================
# Program Start
# =========================
if __name__ == "__main__":
    login_screen()
