import argparse
import os

from app.services.project_service import ProjectService
from app.services.storage import JSONStorage


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    # -----------------------------
    # create-project
    # -----------------------------
    create = sub.add_parser("create-project")
    create.add_argument("--title", required=True)
    create.add_argument("--desc", required=True)
    create.add_argument("--leader", required=True)

    # -----------------------------
    # join-project
    # -----------------------------
    join = sub.add_parser("join-project")
    join.add_argument("--project-id", required=True)
    join.add_argument("--user-id", required=True)

    # -----------------------------
    # approve-request
    # -----------------------------
    approve = sub.add_parser("approve-request")
    approve.add_argument("--project-id", required=True)
    approve.add_argument("--user-id", required=True)

    args = parser.parse_args()

    # ✅ تخزين JSON فقط (بدون Mongo)
    data_file = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "projects.json"
    )

    storage = JSONStorage(data_file)
    service = ProjectService(storage)

    # -----------------------------
    # Commands
    # -----------------------------
    if args.command == "create-project":
        project_id = service.create_project(
            args.title,
            args.desc,
            args.leader
        )
        print(project_id)  # مهم جداً للـ test

    elif args.command == "join-project":
        result = service.join_project(
            args.project_id,
            args.user_id
        )
        print(result)

    elif args.command == "approve-request":
        result = service.approve_request(
            args.project_id,
            args.user_id
        )
        print(result)


if __name__ == "__main__":
    main()
