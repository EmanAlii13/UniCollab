import argparse
import os

from app.services.project_service import ProjectService
from app.storage.json_storage import JSONStorage
from app.storage.storage_interface import RealStorage


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    # create-project
    create = sub.add_parser("create-project")
    create.add_argument("--title", required=True)
    create.add_argument("--desc", required=True)
    create.add_argument("--leader", required=True)

    # join-project
    join = sub.add_parser("join-project")
    join.add_argument("--project-id", required=True)
    join.add_argument("--user-id", required=True)

    # approve-request
    approve = sub.add_parser("approve-request")
    approve.add_argument("--project-id", required=True)
    approve.add_argument("--user-id", required=True)

    args = parser.parse_args()

    # اختيار الـ storage:
    data_file = os.getenv(
        "PROJECTS_DATA_FILE",
        os.path.join(os.path.dirname(__file__), "..", "data", "projects.json"),
    )

    if os.path.exists(data_file):
        storage = JSONStorage(data_file)  # Integration test تستخدم ملف مؤقت
    else:
        storage = RealStorage()  # MongoDB في البيئة الحقيقية

    service = ProjectService(storage=storage)

    if args.command == "create-project":
        project_id = service.create_project(args.title, args.desc, args.leader)
        print(f"Project created successfully with ID: {project_id}")

    elif args.command == "join-project":
        result = service.join_project(args.project_id, args.user_id)
        print(result)

    elif args.command == "approve-request":
        result = service.approve_request(args.project_id, args.user_id)
        print(result)


if __name__ == "__main__":
    main()
